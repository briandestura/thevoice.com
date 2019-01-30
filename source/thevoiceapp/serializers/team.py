from rest_framework import serializers
from rest_framework.serializers import Serializer

from thevoiceapp.serializers.user import UserSerializer


class TeamDetailSerializer(Serializer):
    id = serializers.IntegerField()
    team_name = serializers.CharField()
    average_score = serializers.IntegerField()
    members = UserSerializer(many=True)
