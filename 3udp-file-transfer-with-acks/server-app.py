"""
UDP File transfer client-server application
more reliable due to ACKs
Server side
"""
import logging
import socket
import traceback
from time import time

logging.basicConfig(level=logging.NOTSET)

localIP = "127.0.0.1"
localPort = 12345
SERVER_BUFFER_SIZE = 100

START_TIME = time()

# (IP addr && port number) : {next_seqno, last reception timestamp, expected size, extension}
sessions = {}

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
logging.info("UDP file server is up and listening")

while True:
    try:
        # receive message
        bytesAddressPair = UDPServerSocket.recvfrom(SERVER_BUFFER_SIZE)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        type_of_msg, clientMsg = message.split(b'|', 1)
        # match message type
        if type_of_msg == b's':
            # if it is a 'start' message,
            seqno, file_extension, file_size = clientMsg.decode().split('|')
            # send ack with max_size
            serverMsg = f"a|{int(seqno)+1}|{SERVER_BUFFER_SIZE}"
            UDPServerSocket.sendto(serverMsg.encode(), address)
            # and record a session
            sessions[address] = {'seqno': int(seqno)+1,
                                 'timestamp': time(),
                                 'file_size': file_size,
                                 'file_extension': file_extension,
                                 'file_contents': b''}
            logging.info(f"Initialized a new session '{sessions[address]} with {address}")
        elif type_of_msg == b'd':
            # if it is a 'data' message,
            seqno, file_fragment = clientMsg.split(b'|', 1)
            # check its sequence number
            seqno = int(seqno.decode())
            session = sessions[address]
            if seqno == session['seqno']: # if it is as expected,
                # update session information, save data
                session['file_contents'] += file_fragment
                session['seqno'] += 1
                session['timestamp'] = time()
                serverMsg = f"a|{int(seqno)+1}"
                # and send an acknowledgement
                UDPServerSocket.sendto(serverMsg.encode(), address)
            else:
                pass  # discarding duplicates
        else:
            logging.error("received unsupported type of datagram")

        # probably should have done it in a separate thread...
        # check active sessions
        garbage_bin = []
        for client in sessions:
            session = sessions[client]
            # if server has received what it was expecting, save the file contents to file
            # (named as timestamp to be identified uniquely)
            if int(session['file_size']) == len(session['file_contents']):
                server_fname = "server_files/" + str(time() - START_TIME) + session['file_extension']
                image_result = open(server_fname, 'wb')
                image_result.write(session['file_contents'])
                logging.info(f"Saved a file {server_fname} from {client}")
            # if client was unactive for 3 seconds,
            if session['timestamp'] < time() - 3:
                garbage_bin.append(client)
        for client in garbage_bin:
            sessions.pop(client)  # delete information on this session
            logging.info(f"Deleted session of {client} because it stopped to send anything")

    except Exception as e:
        logging.error(traceback.format_exc())
        continue
