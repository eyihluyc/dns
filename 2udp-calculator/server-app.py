"""
client-server calculator
based on code from https://pythontic.com/modules/socket/udp-client-server-example

Server side
"""


import socket
import operator
from math import floor

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
    ans = ops[operation](float(op1), float(op2))
    if isinstance(ans, float) and ans == floor(ans):
        ans = int(ans)
    return ans


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

    message = message.decode()
    try:
        msgFromServer = calculate(*message.split())
    except ZeroDivisionError:
        msgFromServer = "Division by zero exception! Try again with valid input :)"

    bytesToSend = str.encode(str(msgFromServer))

    print(f"client's address: {address}\nclient's request: {message}\nserver's response: {msgFromServer}\n")
    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)
