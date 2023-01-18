####client
import socket
import sys
import os
 
#create an object here
s = socket.socket()
#hostName of server (node-0.lab5.ch-geni-net.instageni.colorado.edu)   
hostName = "node-0.lab5.ch-geni-net.instageni.colorado.edu"        
#buffer size                 
bufferSize = 1024
#create empty message            
msg = ""

#check arguement                   
if(len(sys.argv)!=4):
    print("Please enter data file name, destination IP(or domain name), destination port number correctly!")
    exit()
else:
    filename = sys.argv[1]
    destinationIP = sys.argv[2]
    destinationPort = sys.argv[3]

#open file
file = open(filename,'rb')
#get file size
fileSize = str(os.path.getsize(filename))

#connect to server                                                 
s.connect((hostName,int(destinationPort)))
#wait for server                                                    
print("Waiting for server permission...")
#send filename
s.send(filename.encode().zfill(bufferSize))
#send file size
s.send(fileSize.encode().zfill(bufferSize))
msg = s.recv(bufferSize)
print(msg.decode())
#read in chunks and send if not rejected
if('not' in msg.decode()):
    exit()
t = True
while t:
    chunk = file.read(bufferSize)
    s.send(chunk)
    if not chunk:
        t = False
        break
#print("Done with sending")
msg = s.recv(bufferSize)
print(msg.decode())
s.close()
