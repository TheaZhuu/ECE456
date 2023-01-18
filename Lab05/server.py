####server
import socket
import sys
import os

#create an object here
s = socket.socket()
#get hostname
hostName = socket.gethostname()
#get locap ip
localIp = socket.gethostbyname(hostName)
#buffer size
bufferSize = 1024
#create empty message
msg = ""

#check arguement
if(len(sys.argv)==1 or len(sys.argv)>2):
    print("Please enter port number correctly!")
    exit()
else:
    ans = input("Do you want to clean received messages?(y/n)")
    # Get port number from argument
    localPort = sys.argv[1]
if(ans == 'n'):
    print("Message not found")
elif(ans == 'y'):
    pass
else:
    print("ERROR")
    exit()
print(hostName)

#print hostname and port number
print("Host name: "+hostName[:6]+", Port number: "+localPort)

#Bine the hostName and the localPort  to a socket
s.bind((hostName,int(localPort)))
#wait for client
s.listen(5)

while True:
    print("Waiting for client...")
    #connect with client
    c, addr = s.accept()
    print("Connect to client!")
    filename = (c.recv(bufferSize)).decode().strip("0")
    fileSize = (c.recv(bufferSize)).decode().strip("0")
    print("Client "+str(addr)+" requests to send a file, name: "+filename+", size: "+fileSize+"bytes")
    ans = input("Accept this file?(y/n)")
    if(ans == 'n'):
        print("A file is not accepted")
        c.send(b"A file is not accepted")
    elif(ans == 'y'):
        newFileName = input("Please rename received file: ")
        num = 1
        msg = "Sending file, size: "+fileSize
        c.send(msg.encode())
        t = True
        temp = int(int(fileSize)/bufferSize)
        if(int(fileSize)%bufferSize!=0):
            temp+=1
        print(temp)
        while(num<=temp):
            print("Receiving piece "+str(num))
            num+=1
            data = c.recv(bufferSize)
            if data:
                with open(newFileName,'ab+') as newfile:
                    newfile.write(data)
        print("All pieces received!")
        print("File saved to "+newFileName)
        print()
        c.send(b"File sent to server.")
#    else:
#        print("Invalid input! Please enter y or n!")
        
    
