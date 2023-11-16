# only server can send msgs to the client
# run these files simultaneously to estabish the server to client communication

import socket

client1 = socket.socket()
client1.connect(("localhost",3000))

def startReceivingMsgs():
    while True:
        print(F"Server : {client1.recv(1024).decode()}")

startReceivingMsgs()