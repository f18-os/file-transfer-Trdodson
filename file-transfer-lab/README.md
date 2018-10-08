# Simple TCP File Transfer

This directory contains the implementation for a simple file transfer.

To transfer a file:
* Start the server. This is done by typing ./fileServer into the terminal.
* Start the client upload. To upload a certain file, enter "./fileClient.py -f
FILENAME" into the terminal. In order for the upload to commence, the file
must already exist.
~~~
* To change the socket, use -s addr:socket
* The client should still be able to upload through the given stammer proxy.
* To terminate the server, enter Ctr-C Ctrl-C into the server's terminal.
~~~
* The file will be uploaded to the /server folder by the server. If the file
already exists in this folder, the client will be notified and the file will
not upload.

## Refrences

This assignment was prepared in a manner consistent with the instructor's
requirements. All significant collaboration or guidance from external sources
is clearly documented.

This README is tailored for grading anonymity. For full attributions, see
COLLABORATORS.md.
