# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6.QtQml import QmlElement
import socket

QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class Sender(QtCore.QThread):
    dataReceived = QtCore.Signal(str)
    dataSent = QtCore.Signal()
    bound = QtCore.Signal()
    def __init__(self):
        super().__init__(None)
        self.host = '0.0.0.0'
        self.port = 9999
        self.buffersize = 1024
        self.data_to_send = None
        self.ready_to_send = False
        print("Sender: initialization finished")


    def run(self):
        print("Sender: run started")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            print("Sender: server created")
            server.bind((self.host, self.port))
            print("Sender: server bound")
            self.bound.emit()
            print("Sender: server listening")
            server.listen()
            print("Sender: server accepting")
            client, addr = server.accept()
            while True:
                if self.isInterruptionRequested():
                    print("Sender: interruption requested, breaking loop")
                    return
                print("Sender: receiving data")
                data = client.recv(self.buffersize).decode('utf-8')
                self.dataReceived.emit(data)
                if self.ready_to_send:
                    print(f"Sender: sending data: {self.data_to_send}")
                    client.sendall(bytes(self.data_to_send, 'utf-8'))
                    self.data_to_send = None
                    self.ready_to_send = False
                    print("Sender: data sent")
                    self.dataSent.emit()
                self.sleep(2)

    QtCore.Slot(str)
    def handle_new_message(self, msg:str):
        print(f"Sender: Slot handle_new_message called with: {msg}")
        self.data_to_send = msg
        self.ready_to_send = True
