# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6.QtQml import QmlElement
from Sender import Sender
from Receiver import Receiver

QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class Controller(QtCore.QObject):

    toSender = QtCore.Signal(str)
    senderSent = QtCore.Signal()
    toReceiver = QtCore.Signal(str)
    newMessage = QtCore.Signal(str)


    def __init__(self):
        super().__init__(None)
        self.sender = Sender()
        self.receiver = Receiver()
        self.sender.dataSent.connect(self.senderSent)
        self.sender.dataReceived.connect(self.toSender)
        self.sender.bound.connect(self.start_receiver)
        self.newMessage.connect(self.sender.handle_new_message)
        self.receiver.dataReceived.connect(self.toReceiver)
        print("Controller: initialization finished")

    @QtCore.Slot()
    def notify(self):
        print("started")
        self.toSender.emit( "program started")
        self.toReceiver.emit( "program started")

    @QtCore.Slot()
    def test(self):
        print("test")

    @QtCore.Slot()
    def start(self):
        print("Controller: start called")
        self.sender.start()

    @QtCore.Slot()
    def start_receiver(self):
        print("Controller: start_receiver called")
        self.receiver.start()

    @QtCore.Slot(str)
    def sendMessage(self, msg:str):
        print(f"Controller: sendMessage called with: {msg}")
        self.newMessage.emit(msg)
