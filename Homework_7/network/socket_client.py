import socket
from furl import furl

import exceptions


class SocketClient:
    BUFF_SIZE = 4096

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        if self.sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def disconnect(self):
        self.sock.close()
        self.sock = None

    def send_data(self, msg):
        total_sent = 0
        msg_encoded = msg.encode()
        while total_sent < len(msg_encoded):
            sent = self.sock.send(msg_encoded[total_sent:])
            if sent == 0:
                raise exceptions.ClientConnectionBrokenException("Connection broken")
            total_sent = total_sent + sent

    def receive_data(self):
        data = b''
        while True:
            part = self.sock.recv(self.BUFF_SIZE)
            data += part
            if len(part) == 0:
                break
        return data.decode()
