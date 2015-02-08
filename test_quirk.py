import asyncio
from PySide.QtCore import QObject, Signal, Slot
from PySide.QtNetwork import QUdpSocket
from quamash import QApplication
import quamash
from src.connectivity import UdpMessage
from src.with_logger import with_logger


@with_logger
class NatPacketServer(QObject):
    datagram_received = Signal(object, object, object)
    def __init__(self, port, parent=None):
        QObject.__init__(self, parent)
        socket = QUdpSocket(self)
        socket.bind(port)
        self._logger.debug("Listening on {port}".format(port=port))
        socket.readyRead.connect(self._on_ready_read)
        socket.error.connect(self._on_error)
        self._socket = socket
        self._subscribers = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._socket.abort()

    def _on_error(self):
        pass

    @Slot()
    def _on_ready_read(self):
        while self._socket.hasPendingDatagrams():
            data, host, port = self._socket.readDatagram(self._socket.pendingDatagramSize())
            self._logger.debug('Received {data} from {host}:{port}'.format(data=data, host=host, port=port))
            if data.startsWith(b'\x08'):  # GPG NAT packets start with this byte
                # Doing anything interesting with data
                # will apparently cause a full deep copy
                # of all objects the signal
                # gets propagated to.
                # We don't want that.
                self.datagram_received.emit("Hello 2", host.toString(), port)

if __name__ == '__main__':
    app = QApplication([])
    loop = quamash.QEventLoop(app)
    server = NatPacketServer(51123)
    def test_receiver(message, host, port):
        print(id(server))
        print(message, host, port)
    server.datagram_received.connect(test_receiver)
    with UdpMessage('127.0.0.1', 51123, "\x08Test") as msg:
        msg.send_payload()
    loop.set_debug(True)
    asyncio.set_event_loop(loop)
    app.exec_()