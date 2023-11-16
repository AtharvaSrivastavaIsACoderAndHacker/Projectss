# only server can send msgs to the client
# run these files simultaneously to estabish the server to client communication

import socket

server = socket.socket() # by default no args so (ipv4,tcp)
print("Socket Created Server !")

server.bind(("localhost", 3000))
server.listen(1)
print("Waiting...")

def startSendingMsgs():
    while True:
        msg = input("You : ")
        client.send(bytes(f"{msg}","utf-8"))



while True:
    client,addr = server.accept()
    print("Connected To :",addr)
    
    startSendingMsgs()   