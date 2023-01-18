####client
import socket
import time
import sys

# key2 = "asdfghjk"  from lab1
key = "asdfghjk";
localPort = sys.argv[1]

odd = False 
hostName = socket.gethostname()
#print('hosthame', hostName)
localIP = socket.gethostbyname(hostName)
print("IP address: ",localIP)

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
    clientMsg = input("Message:")

    #clientMsg_hex = str_to_hex(clientMsg)
    #print('client msg',clientMsg_hex)

    '''
    if(len(clientMsg_hex)%4 != 0):
      odd = True
      clientMsg_hex += '00'
      clientMsg = hex_to_str(clientMsg_hex)
      if(len(clientMsg_hex)%4 !=0):
         clientMsg_hex += '00'
         clientMsg = hex_to_str(clientMsg_hex)
    '''

    clientMsg = [ord(i) for i in clientMsg]
    #print("client msg1", clientMsg)

    if len(clientMsg) % 2 == 1:
        clientMsg.append(0)

    #print("client msg2", clientMsg)
    en_Msg = en(clientMsg,key)
    #bytesToSend = str.encode(en_Msg)i
    bytesToSend = str.encode(''.join([chr(i) for i in en_Msg]))
    #print("bytes to send", bytesToSend)
    serverAddressPort = ("172.17.3.1", int(localPort))
    bufferSize = 1024

# Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg_str = msgFromServer[0].decode()
    msg_str = [ord(i) for i in msg_str]
    msg = de(msg_str,key)
    msg = ''.join([chr(i) for i in msg])
    print(msg)
