"""
Lab 4, Distributed & Network Programming
TCP Client-Server Game

Server side
"""
# python 4number-guessing-game/client.py 127.0.0.1 1234

import sys
import socket
import re

CLIENT_BUFFER_SIZE = 100

if __name__ == '__main__':
    TCPClientSocket = socket.socket(type=socket.SOCK_STREAM)
    try:
        if len(sys.argv) != 3:
            raise ValueError()
        ip = sys.argv[1]
        port = int(sys.argv[2])
        TCPClientSocket.connect((ip, port))
    except ValueError as e:
        sys.exit("Usage example: python ./client.py <address> <port>")
    except socket.error as e:
        sys.exit("Server is unavailable")

    port_msg = TCPClientSocket.recv(CLIENT_BUFFER_SIZE)

    if port_msg == b'Server is full':
        sys.exit(port_msg.decode())

    port = int.from_bytes(port_msg, byteorder='big')

    TCPClientSocket.close()

    TCPClientSocket = socket.socket(type=socket.SOCK_STREAM)

    TCPClientSocket.connect((ip, port))

    welcome_msg = TCPClientSocket.recv(CLIENT_BUFFER_SIZE)
    print(welcome_msg.decode())

    numbers_range = input()

    while not re.fullmatch("[0-9]+ [0-9]+", numbers_range):
        numbers_range = input("Enter the range, e.g. \"0 42\": ")

    TCPClientSocket.sendall(numbers_range.encode())

    while True:
        message = TCPClientSocket.recv(CLIENT_BUFFER_SIZE).decode()
        print(message)
        if message == "You lose":
            break

        guess = input()
        TCPClientSocket.sendall(guess.encode())

        message = TCPClientSocket.recv(CLIENT_BUFFER_SIZE).decode()
        print(message)
        if message == "You win!":
            break

    TCPClientSocket.close()
