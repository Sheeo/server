from PySide.QtNetwork import QTcpSocket
import pytest

from gameModes import Game
from FAGamesServerThread import FAGameThread

@pytest.fixture()
def game_thread():
    return FAGameThread(QTcpSocket())


class TestClientProtocol(object):
    """
    Test how the GpgNetSend commands affect state of a game
    """
    def test_is_initially_disconnected(self, game_thread):
        assert game_thread.game is None
