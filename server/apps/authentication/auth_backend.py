from models import Login

from rest_framework import authentication
from rest_framework import exceptions


class FafAuthBackend(object):
    """
    Provides authentication for FAF accounts
    """
    def authenticate(self, login=None, password=None):
        return Login(login=login, password=password)

    def get_user(self, user_id):
        return None

