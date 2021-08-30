"""
UDP File transfer client-server application
more reliable due to ACKs
Client side
"""
import socket
import os
import logging


logging.basicConfig(level=logging.NOTSET)


UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.settimeout(0.5)
serverAddressPort = ("127.0.0.1", 12345)
bufferSize = 4096

# sends message no more than 5 times, until it receives an ACK
def await_ACK_for(msgFromClient):
    msgFromServer = None
    for i in range(5):
        try:
            UDPClientSocket.sendto(msgFromClient, serverAddressPort)
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
            break
        except socket.timeout:
            pass
    if msgFromServer is not None:
        return msgFromServer[0]
    else:
        raise Exception("Server is not available")


def send_file(path_to_file):
    try:
        with open(path_to_file, "rb") as file:
            file_contents = file.read()

        logging.info("Read file")
        _, file_extension = os.path.splitext(path_to_file)
        file_size = os.path.getsize(path_to_file)
        seqno = 0

        # gather info for start message:
        start_msg = f"s|{seqno}|{file_extension}|{file_size}"
        # send it and receive an ACK with max  size
        _, next_seqno, maxsize = await_ACK_for(start_msg.encode()).split(b'|')
        maxsize = int(maxsize.decode())

        # let this iterator go through file contents:
        iterator = 0
        while iterator != file_size:
            data_msg = b'd|' + next_seqno + b'|'
            end_of_fragment = min(iterator + maxsize - len(data_msg), file_size)
            data_bytes = file_contents[iterator: end_of_fragment]
            iterator = end_of_fragment
            data_msg += data_bytes
            # send datagram, and receive an ACK with next_seqno
            _, next_seqno = await_ACK_for(data_msg).split(b'|')

        logging.info("Finished file transmission")
    except Exception as e:
        logging.info("Unable to send file")
        logging.error(e)
        return


if __name__ == '__main__':
    # path_to_file = input("path to file to transfer: ")
    path_to_file = "client_files/innopolis.jpg"
    send_file(path_to_file)
