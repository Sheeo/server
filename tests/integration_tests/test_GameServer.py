from asyncio import coroutine, sleep
import asyncio
import json
import logging
import time
from PySide.QtCore import QThread, QCoreApplication

from PySide.QtNetwork import QHostAddress, QUdpSocket
from mock import call

from FaGamesServer import FAServer
from .testclient import TestGPGClient
import config

from quamash import QThreadExecutor


@coroutine
def wait_call(mock, call, timeout=0.5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if call in mock.mock_calls:
            return True
        yield from sleep(0.1)
    assert call in mock.mock_calls

@coroutine
def run_server(address, loop, player_service, games):
    with FAServer(loop, player_service, games, [], []) as server:
        server.run(QHostAddress(address))
        for i in range(1,5):
            print("processEvents")
            yield from asyncio.wait_for(server.done, 2)

def test_public_host(loop, players, player_service, games):
    @coroutine
    def test():
        player = players.hosting
        with TestGPGClient('127.0.0.1', 8000, 6112) as client:
            client.send_GameState(['Idle'])
            client.send_GameState(['Lobby'])
            yield from wait_call(client.udp_messages,
                                  call("\x08Are you public? %s" % player.getId()))
            client.send_ProcessNatPacket(["%s:%s" % (player.getIp(), player.getGamePort()),
                                          "Are you public? %s" % player.getId()])
            yield from wait_call(client.messages,
                        call(json.dumps({"key": "ConnectivityState",
                        "commands": [player.getId(), "PUBLIC"]})))
    loop.run_until_complete(asyncio.wait_for(test(), timeout=2))


def test_stun_host(loop, players, player_service, games):
    @asyncio.coroutine
    def test():
        player = players.hosting
        with TestGPGClient('127.0.0.1', 8000, 6114) as client:
            client.send_GameState(['Idle'])
            client.send_GameState(['Lobby'])
            yield from wait_call(client.messages,
                          call(json.dumps({"key": "SendNatPacket",
                                "commands": ["%s:%s" % (config.LOBBY_IP, config.LOBBY_UDP_PORT),
                                             "Hello %s" % player.getId()]})), 2)
            logging.getLogger().debug("Sending udp")
            client.udp_socket.writeDatagram('\x08Hello 2'.encode(), QHostAddress('127.0.0.1'), config.LOBBY_UDP_PORT)
            logging.getLogger().debug("Sending udp")
            client.udp_socket.writeDatagram('\x08Hello 2'.encode(), QHostAddress('127.0.0.1'), config.LOBBY_UDP_PORT)
            yield from wait_call(client.messages,
                          call(json.dumps({"key": "ConnectivityState",
                                           "commands": [player.getId(), "STUN"]})), 2)
    loop.run_until_complete(asyncio.wait_for(test(), timeout=5))
