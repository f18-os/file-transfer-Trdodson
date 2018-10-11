#! /usr/bin/env python3

import socket, sys, re, os

sys.path.append("../lib")       # for params

from threading import Thread, Lock

import params

from framedSock import framedReceive, framedSend

#Manage initial parameters for server.
switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "fileServer"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

global sLock
sLock = Lock()        # Lock to handle concurrency.

while True:
    sock, addr = lsock.accept()   # Accept connection.
    print("connection rec'd from", addr)
    Thread().start()

# Worker class. Based on threads_v1.py.
class Worker(Thread):
    def _init_(self):
        global threadNum
        Thread._init_(self, name="Thread-%d" % threadNum)
        threadNum += 1
    def run(self):
        print(threadNum)
        global sLock
        sLock.acquire()
        checkRecv = framedReceive(sock, debug)             # Check the first thing the server sends!
        if checkRecv == b"ERROR":                          # Client sent an error message - stop!
            print("Something went wrong client-side. No files recieved.")
            sock.close()
            sys.exit(0)

        if checkRecv == b"exit":                           # Check for server terminate command. NON-FUNCTIONAL.
            print("Client terminated server. Shutting down...")
            sock.close()
            sys.exit(0)

        while checkRecv != b'':
            fileName = checkRecv.decode("utf-8")            # Pull out the file name!
            checkRecv = framedReceive(sock, debug)                

        filePath = os.getcwd() + "/server/" + fileName      # Get path; server uploads fle to server folder.

        if os.path.isfile(filePath):                        # Don't let user overwrite files already on the server.
            print("ERROR: File already exists. %s not recieved." % fileName)
            framedSend(sock, b"exists", debug)
            sock.close()
            sys.exit(0)
        else:
            framedSend(sock,b"accept", debug)                # Tell client that everything is fine!
            
        data = framedReceive(sock,debug)                     # Check out the data client sent.
        isZeroLen = False
        
        if (data == b"ERROR"):                               # Client sent an error - stop!
           print("ERROR: Something went wrong client-side. File not recieved.")
           sock.close()
           sys.exit(0)
            
        if data is None:                                     # Check if file is zero length, and handle.
           print("WARNING: Zero-length file.")
           with open(filePath, 'w') as myFile:
               myFile.write("")
               isZeroLen = True
            
        if not isZeroLen:
           with open(filePath, 'wb') as myFile:        # Otherwise, open a file to copy payload to.
               while True:
                   myFile.write(data)                  # Read the data sent by the client and copy to the file.
                   data = framedReceive(sock, debug)
               if not data:                        # When there's nothing more, stop taking payload.
                   sys.exit(0)
                
        myFile.close()
        print("%s received. Exiting..." % fileName)
        sock.close()
        print("Closed connection", addr)
        sLock.release()
