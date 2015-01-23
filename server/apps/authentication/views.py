from .models import Login, NameHistory
from rest_framework import viewsets
from .serializers import LoginSerializer, NameHistorySerializer


class LoginViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows logins to be viewed or edited
    """
    queryset = Login.objects.all()
    serializer_class = LoginSerializer


class NameHistoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows name history to be viewed or edited
    """
    queryset = NameHistory.objects.all()
    serializer_class = NameHistorySerializer
