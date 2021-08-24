"""
client-server calculator
based on code from https://pythontic.com/modules/socket/udp-client-server-example

Client side
"""

import re
import socket

print("Input calculation request in the form 'operator operand operand', e.g. '- 13 8' for '13 - 8'")

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 1024

while True:
    try:
        clientMsg = input()
        if clientMsg == "QUIT" or clientMsg == "quit" or clientMsg == "Quit":
            raise KeyboardInterrupt
        elif bool(re.fullmatch("(\*|/|-|\+|>|<|>=|<=) -?[0-9]+(\.[0-9]+)? -?[0-9]+(\.[0-9]+)?", clientMsg)):
            bytesToSend = str.encode(clientMsg)
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)

            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
            serverMsg = msgFromServer[0].decode()
            print(serverMsg)
        else:
            print("Input is malformed (expected form is 'operator operand operand'), try again or enter 'QUIT' to quit")

    except KeyboardInterrupt:
        print("Closing calculator...")
        break
