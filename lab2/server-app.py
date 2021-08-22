"""
client-server calculator
based on code from https://pythontic.com/modules/socket/udp-client-server-example

Server side
"""


import socket
import operator

ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '>': operator.gt,
    ">=": operator.ge,
    '<': operator.lt,
    "<=": operator.le
}


def calculate(operation, op1, op2):
    return ops[operation](op1, op2)


localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP calculator server is up and listening")

# Listen for incoming datagrams
while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)

    msgFromServer = calculate(*clientMsg.split())
    bytesToSend = str.encode(msgFromServer)

    print(clientMsg)
    print(clientIP)

    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)
