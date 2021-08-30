"""
UDP File transfer client-server application

Server side
"""
import binascii
import logging
import socket
import json
import traceback


def get_crc_checksum(file_contents):
    file_contents = (binascii.crc32(file_contents) & 0xFFFFFFFF)
    return "%08X" % file_contents


logging.basicConfig(level=logging.NOTSET)

localIP = "127.0.0.1"
localPort = 12345
SERVER_BUFFER_SIZE = 100

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPServerSocket.bind((localIP, localPort))

logging.info("UDP file server is up and listening")

while True:
    try:
        bytesAddressPair = UDPServerSocket.recvfrom(SERVER_BUFFER_SIZE)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        file_info = json.loads(message.decode())
    except Exception as e:
        logging.error(traceback.format_exc())
        continue

    logging.info(f"Client's address: {address}")
    logging.info(f"File metas: {file_info}")

    UDPServerSocket.sendto(SERVER_BUFFER_SIZE.to_bytes(length=2, byteorder='little'), address)

    try:
        file_contents = b''
        while True:
            bytesAddressPair = UDPServerSocket.recvfrom(SERVER_BUFFER_SIZE)
            assert address == bytesAddressPair[1]
            file_contents += bytesAddressPair[0]
            if len(file_contents) == file_info['size']:
                break
    except Exception as e:
        logging.error(traceback.format_exc())
        continue

    logging.info(f"finished receiving")
    if get_crc_checksum(file_contents) == file_info['checksum']:
        image_result = open("server_files/new" + file_info['name'], 'wb')
        image_result.write(file_contents)

        UDPServerSocket.sendto(str.encode("OK"), address)
        logging.info(f"Successfully reveived {file_info['name']} and saved it. Waiting for new connections...")
    else:
        logging.info(f"Failed to reveive {file_info.name}. Waiting for new connections...")
