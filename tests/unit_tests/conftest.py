import pytest
from PySide import QtSql
from flexmock import flexmock
import mock


@pytest.fixture()
def sqlquery():
    return flexmock(
        exec_=lambda s=None: None,
        size=lambda: 0,
        lastInsertId=lambda: 1,
        prepare=lambda q: None,
        addBindValue=lambda v: None
    )

@pytest.fixture()
def lobbythread():
    return flexmock(
        sendJSON=lambda obj: None
    )

@pytest.fixture()
def db():
    db = QtSql.QSqlDatabase()
    db.isOpen = mock.Mock(return_value=True)
    return db

