# Collaborations

* https://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php:
this sample code in the first example given on this page allowed me to realize
that, when sending a file to the server, you're (in layman's terms) sending
the file line by line: hence, I understand that the client reads a line, sends
that to the server, and the server then writes that payload to its own
file. After iterating over every line, this results in an exact copy on the
server's side.

* Dr. Fruedenthal's framed-echo demo files, including framedClient.py,
  framedServer.py, and framedSock.py, were the baseline for these
  programs. Few modifications were made as far as opening and connecting the
  sockets, management of parameters (framedClient), and the framing of sending
  and recieving and sending data (framedSock). framedForkServer was also a
  help in implementing the loop that allows for multiple client support.

* Jake Lasley and Jorge Ramirez helped with the client sending and the server
  recieving only 100 bytes at a time - specifically, with the lines
  sock.recv(100) and line = myFile.read(100).

* Discussed multiple client support with Noa Dodson by explaining
  framedForkServer.py. Discussed how to send and recieve file contents line by
  line.

* Based threadServer.py on code from threads.v1,py by Dr. Freudenthal; still non-functional!
