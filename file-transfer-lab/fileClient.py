#! /usr/bin/env python3

# Client file transfer program. The client takes a file name as input and
# sends the corresponding file to the server.

import socket, sys, re
sys.path.append("../lib")       # for params
import params

# Pairs for parameters.
switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    (('-f', '--file'), "file", "default.txt"),
    )

progname = "fileClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug, fileName  = paramMap["server"], paramMap["usage"], paramMap["debug"], paramMap["file"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

print("Connected. Trying to open file...")
    
from framedSock import framedSend, framedReceive

try:                                                # Try to open the file.
    myFile = open(fileName, 'rb')
except FileNotFoundError:                           # Let the user know if it fails and exit.
    print("ERROR: File doesn't exist! Exiting...")
    framedSend(s, b"ERROR", debug)
    s.close()
    exit()

try:
    framedSend(s, fileName.encode(), debug)              # Send the server the file's name.
    framedSend(s,b"", debug)                             # Server knows to stop getting name when it gets empty byte array

    checkRecv = framedReceive(s,debug)
    
    if checkRecv == b"exists":             # Server tells client file is already uploaded. Stop!
        print("ERROR: File already on server. Exiting...")
        s.close()
        exit()
    else:                                  # Otherwise, continiue.
        print("Success! Sending file.")
    
    line = myFile.read(100)
    while(line):                                         # Start reading
        framedSend(s, line, debug)                       # Send each line to the server.
        line = myFile.read(100)
    print("Sent %s." % fileName)
    myFile.close()
    print("Closing connection." %s)
except BrokenPipeError:                                 # If something server-side stops or breaks, fail gracefully
    print("Server broke connection. Exiting...")
s.close()
exit()
