# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
import socket

class Receiver(QtCore.QThread):
    dataReceived = QtCore.Signal(str)
    dataSent = QtCore.Signal()
    def __init__(self):
        super().__init__(None)
        self.host = '127.0.0.1'
        self.port = 9999
        self.buffersize = 1024


    def run(self):
        print("Receiver: run method started")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            print("Receiver: connecting to server...")
            client.connect((self.host, self.port))
            print("Receiver: Connected")
            while True:
                if self.isInterruptionRequested:
                    return
                print("Receiver: receiving...")
                data = client.recv(self.buffersize)
                print("Receiver: sending...")
                client.sendall(bytes(data))
                self.dataSent.emit()
                self.sleep(0.5)

