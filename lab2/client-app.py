"""
client-server calculator
based on code from https://pythontic.com/modules/socket/udp-client-server-example

Client side
"""

import re
import socket

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 1024

while True:
    try:
        clientMsg = input()
        if clientMsg == 'q' or clientMsg == "quit":
            raise KeyboardInterrupt
        elif bool(re.fullmatch("(\*|/|-|\+|>|<|>=|<=) [0-9]+(\.[0-9]+)? [0-9]+(\.[0-9]+)?", clientMsg)):
            bytesToSend = str.encode(clientMsg)
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)

            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
            serverMsg = "Message from Server {}".format(msgFromServer[0])
            print(serverMsg)
        else:
            print("Input is malformed, try again or press 'q' to quit")

    except KeyboardInterrupt:
        print("Closing calculator...")
        break

