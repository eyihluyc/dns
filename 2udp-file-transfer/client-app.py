"""
UDP File transfer client-server application

Client side
"""
import socket
import binascii
import os
import json
import logging


logging.basicConfig(level=logging.NOTSET)

#  checksum calculation
def get_crc_checksum(file_contents):
    file_contents = (binascii.crc32(file_contents) & 0xFFFFFFFF)
    return "%08X" % file_contents


def send(path_to_file):
    with open(path_to_file, "rb") as file:
        file_contents = file.read()

    logging.info("Opened file")

    file_info = {'checksum': get_crc_checksum(file_contents),
                 'size': os.path.getsize(path_to_file),
                 'name': os.path.basename(path_to_file)}

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.settimeout(1)
    serverAddressPort = ("127.0.0.1", 12345)
    bufferSize = 4096

    string_to_send = json.dumps(file_info)
    UDPClientSocket.sendto(string_to_send.encode(), serverAddressPort)
    logging.info("Sent file info")

    try:
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        server_buffer_size = int.from_bytes(msgFromServer[0], byteorder='little')
        logging.info(f"Received server buffer size: {server_buffer_size}")
    except socket.timeout:
        return "Server is not available"

    UDPClientSocket.settimeout(None)
    logging.info(f"Started file transmission")
    for i in range(file_info['size']//server_buffer_size + 1):
        UDPClientSocket.sendto(file_contents[i*server_buffer_size:min((i+1)*server_buffer_size, len(file_contents))], serverAddressPort)

    logging.info(f"Finished file transmission")
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)[0].decode()
    logging.info(f"received message: {msgFromServer}")
    if msgFromServer == "OK":
        return f"Server received {file_info['name']}"
    else:
        return f"Server did not receive {file_info['name']}"


if __name__ == '__main__':
    # path_to_file = input("path to file to transfer: ")
    path_to_file = "client_files/innopolis.jpg"
    status = send(path_to_file)
    logging.info(f"Result of sending: {status}")
