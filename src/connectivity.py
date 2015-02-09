from concurrent.futures import CancelledError, TimeoutError
from PySide.QtNetwork import QUdpSocket, QHostAddress
import asyncio
import logging
from enum import Enum
import config
from .subscribable import Subscribable
from .with_logger import with_logger

logger = logging.getLogger(__name__)

class Connectivity(Enum):
    """
    Describes the connectivity level of a peer
    Three levels are defined:
        - PUBLIC:
        The peer is publicly accessible without prior communication
        - STUN:
            The peer must first send an outbound packet
            before being able to receive on the inbound port
        - PROXY:
            The peer is unable to connect by other means than proxy
    """
    PUBLIC = "PUBLIC"
    STUN = "STUN"
    PROXY = "PROXY"


@with_logger
class UdpMessage():
    """
    UDP datagram sender using QUdpSocket

    Usage:
    >>> with UdpMessage('127.0.0.1', 6112, "Hello there") as msg:
    >>>     msg.send_payload()
    >>>     # Optionally change message and send more
    >>>     msg.message = "New hello"
    >>>     msg.send_payload()

    """
    def __init__(self, remote_addr, remote_port, message=None):
        self.message = message
        if isinstance(remote_addr, QHostAddress):
            self.remote_addr = remote_addr
        else:
            self.remote_addr = QHostAddress(remote_addr)
        self.remote_port = remote_port
        self.socket = QUdpSocket()
        self.socket.connectToHost(remote_addr, remote_port)
        self.socket.error.connect(self._on_error)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.socket.abort()
        except:
            pass

    def send_payload(self):
        self._logger.debug("UDP(%s:%s)>> %s" % (self.remote_addr.toString(), self.remote_port, self.message))
        self.socket.writeDatagram(self.message.encode(), self.remote_addr, self.remote_port)

    def _on_error(self):
        self._logger.debug("UDP socket error %s" % self.socket.errorString)


from PySide.QtCore import Qt, QThread, QCoreApplication




@with_logger
class TestPeer():
    """
    Determine the connectivity state of a peer.
    """
    def __init__(self,
                 connection: Subscribable,
                 host: str,
                 port: int,
                 identifier: str):
        """
        :return: None
        """
        super(TestPeer, self).__init__()
        self.connection = connection
        self.connectivity_state = None
        self.remote_addr = (host, port)
        self.identifier = identifier
        self.connection.log.debug("Testing peer connectivity")
        self.client_packets = []
        self.server_packets = []

    def __enter__(self):
        self._logger.warn("Subscribing!")
        self.connection.subscribe(self, ['ProcessNatPacket', 'ProcessServerNatPacket'])
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._logger.warn("Unsubscribing!")
        self.connection.unsubscribe(self, ['ProcessNatPacket', 'ProcessServerNatPacket'])


    @asyncio.coroutine
    def determine_connectivity(self):
        try:
            if (yield from self.test_public()):
                return Connectivity.PUBLIC
            elif (yield from self.test_stun()):
                return Connectivity.STUN
            else:
                return Connectivity.PROXY
        except (TimeoutError, CancelledError):
            pass
        return Connectivity.PROXY

    def handle_ProcessNatPacket(self, arguments):
        self._logger.debug("Got ProcessNatPacket")
        self.client_packets.append(arguments)

    def handle_ProcessServerNatPacket(self, arguments):
        self._logger.debug("Got ProcessServerNatPacket {}".format(arguments))
        self.server_packets.append(arguments)
        self._logger.debug("id(self):{}".format(id(self)))
        self._logger.debug("Self.server_packets: {}".format(self.server_packets))

    @asyncio.coroutine
    def test_public(self):
        self._logger.debug("Testing PUBLIC")
        self._logger.debug("All subs now: {}".format(self.connection._subscriptions))
        for i in range(0, 3):
            with UdpMessage(QHostAddress(self.remote_addr[0]),
                            self.remote_addr[1],
                            "\x08Are you public? %s" % self.identifier) as msg:
                msg.send_payload()
                yield from asyncio.sleep(0.2)
        return any(map(lambda args: "Are you public? %s" % self.identifier in args,
                       self.client_packets))

    def received_server_packet(self, msg):
        for packet in self.server_packets:
            if msg in packet:
                return True

    @asyncio.coroutine
    def test_stun(self):
        self._logger.debug("Testing STUN")
        self._logger.debug("id(self):{}".format(id(self)))
        self._logger.debug("All subs now: {}".format(self.connection._subscriptions))
        for i in range(0, 3):
            self.connection.sendToRelay('SendNatPacket', ["%s:%s" % (config.LOBBY_IP,
                                                                     config.LOBBY_UDP_PORT),
                                                          "Hello %s" % self.identifier])
            self._logger.debug(self.received_server_packet("Hello {}".format(self.identifier)))
            if self.received_server_packet("\x08Hello {}".format(self.identifier)):
                return True
            yield from asyncio.sleep(0.1)
        return any(map(lambda args: '\x08Hello {}'.format(self.identifier) in args,
                   self.server_packets))
