from PySide.QtCore import QCoreApplication, QTimer
from PySide.QtNetwork import QUdpSocket, QHostAddress
import time

socket = QUdpSocket()

def send_payload():
    print("Sending payload")
    socket.writeDatagram('\x08Hello 2', QHostAddress('127.0.0.1'), 30351)

def main():
    #socket.connectToHost('127.0.0.1', 30351)
    socket.bind(6666)
    print("Connected?")
    send_payload()
    socket.connected.connect(send_payload)

    app = QCoreApplication([])
    timer = QTimer()
    timer.timeout.connect(app.exit)
    timer.setInterval(100)
    timer.start()
    app.exec_()

if __name__ == "__main__":
    main()
