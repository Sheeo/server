from .models import Login, NameHistory
from rest_framework import serializers


class LoginSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Login
        fields = ('login', 'password')


class NameHistorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NameHistory
        fields = ('user', 'previous_name')
