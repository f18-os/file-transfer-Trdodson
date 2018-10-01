#! /usr/bin/env python3

import socket, sys, re

sys.path.append("../lib")       # for params

import params

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

sock, addr = lsock.accept()

print("connection rec'd from", addr)

data = sock.recv(100)                                           # Check out the data client sent.
if (data == b"ERROR"):                                          # Client sent an error - stop!
    print("ERROR: Something went wrong client-side. Exiting...")
    sock.close()
    exit()

with open('payload.txt', 'wb') as myFile:                       # Otherwise, open a file to copy payload to.
    while True:                                                  
        myFile.write(data)                                      # Read the data sent by the client and copy to the file.
        data = sock.recv(100)                                   
        if not data:                                            # When there's nothing more, stop taking payload.
            break
myFile.close()
print("File recieved. Exiting...")
sock.close()
print("Closed connection.")

