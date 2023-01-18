
####server
import socket
import sys
import os
import time
from datetime import datetime

#print("sssssssss")
#get hostname
hostName = socket.gethostname()
#print(hostName)
#print("yyyyyy yyyyy")

#get local ip 
localIP = socket.gethostbyname(hostName)
#buffer size 
bufferSize = 1024

# key2 = "asdfghjk"  from lab1
key = "asdfghjk";

empty_msg = "---------------------------------------------------\nMessage from Client:\n00/00/0000 00:00\:00 IP:000.00.0.00\n"
data = [empty_msg,empty_msg,empty_msg,empty_msg,empty_msg]

#
if(len(sys.argv)==1 or len(sys.argv)>2):
      print("Please enter port number correctly!")
      exit()
else:
    ans = input("Do you want to clean received message?(y/n)")
    # Get port number from argument
    localPort = sys.argv[1]

if(ans == 'n'):
    print(''.join(map(str.data)))

elif(ans == 'y'):
    print("Messages are cleared")

else: 
  print("Invalid Answer")
  

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, int(localPort))) 

# Print hostname and port number                                                                         
print("hostname: ",hostName[:6],",listening to port: ",localPort)
  


#------------------- encrption part----------------------
def str_to_hex(str):
  s = str.encode('latin-1')
  return s.hex()

# swap L & R and then do xor between L and key
def res_Lxor(L,R,KeyC):
  L_prime = R
  R_prime = L^KeyC
  return L_prime,R_prime
  

# key_str: list of ascii number of keys
def en(data,key_list):
  #print("Key List:", key_list)
  if len(data) %2 == 1:
    data.append(0)
  ans = []
  for i in range(0,len(data),2):
    tmpL, tmpR = data[i], data[i+1]
    for key in key_list:
      tmpL,tmpR = res_Lxor(tmpL,tmpR,key)
    ans.extend([tmpL,tmpR])
  return ans

#----------------Decryption----------------------------
#decrption

#convert hex to string 
def hex_to_str(hex):
  s = (bytes.fromhex(hex)).decode("latin-1")
  return s
# swap L & R and then do xor between L and key
def res_Lxor(L,R,KeyC):
  L_prime = R
  R_prime = L^KeyC
  return L_prime,R_prime
  
# key_str: list of ascii number of keys
def de(data,key_list):
  #print("Key List:", key_list)
  if len(data) %2 == 1:
    data.append(0)
  ans = []
  for i in range(0,len(data),2):
    tmpL, tmpR = data[i], data[i+1]
    for key in key_list:
      tmpL,tmpR = res_Lxor(tmpL,tmpR,key)
    ans.extend([tmpL,tmpR])
  return ans

#------------------done-------------------------------
key = [ord(i) for i in key]
while(True):
      odd = False
      print("\nWaiting for client...\n")
  
      # Receive from client
      bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
      # Get message from client 
      message = bytesAddressPair[0]
      # Get tuple of IP address from client
      address = bytesAddressPair[1]
      #change tuple IP address to str
      empty = ""
      str_address = empty.join(str(str_address) for str_address in address)
      #after it is random number 
      ip_address = str_address[:11]

      print("Connect to client!")
      print("Running decryption, please wait!")
      print("ReceiveData:")
      message = list(message)
      #print("message", message)

      mes = de(message,key)
      mes = ''.join([chr(i) for i in mes])
      #print('mes',mes)
      clientMsg = "Message from Client:{}".format(mes)
      clientIP  = "Client IP Address:{}".format(address)

      # using now() to get current time
      current_time = datetime.now()
      time = current_time.strftime("%b %d %Y %H:%M:%S")

      whole_str = "---------------------------------------------------\n"+clientMsg+"\n"+time+" IP:"+ip_address 
      if(ip_address =="172.17.3.4"):
            whole_str +="\nThis is from node-1\n"
      elif(ip_address == "172.17.3.5"):
            whole_str +="\nThis is from node-2\n"
      else:
            if(ip_address == "172.17.3.6"):
                  whole_str+="\nThis is from node-3\n"
      
      data.pop(0)
      data.append(whole_str)
      print("data,", data)
      print(''.join(map(str,data)))
      whole_str =""

      ServerMsg= ''.join(map(str,data))
      ServerMsg_hex = str_to_hex(ServerMsg)
      if(len(ServerMsg_hex)%4 !=0):
            odd = True
            ServerMsg_hex += '00'
      #message from client
            ClientMsg = hex_to_str(ServerMsg_hex)
            if(len(ServerMsg_hex)%4 != 0):
                  ServerMsg_hex += '00'
                  ServerMsg = hex_to_str(ServerMsg_hex)
    
      #print('clientmessage',clientMsg)
      clientMsg = [ord(i) for i in clientMsg]
      de_Msg = en(clientMsg,key)
      de_Msg = ''.join([chr(i) for i in de_Msg])
      bytesToSend = str.encode(de_Msg)

      # Sending a reply to client
      UDPServerSocket.sendto(bytesToSend, address)

                            

 
