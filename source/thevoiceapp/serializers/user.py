from rest_framework import serializers
from rest_framework.serializers import Serializer

class UserSerializer(Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
