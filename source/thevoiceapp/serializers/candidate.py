from rest_framework.serializers import Serializer
from rest_framework import serializers


class PerformanceDetailsSerializer(Serializer):
    song_name = serializers.CharField()
    date = serializers.DateTimeField()


class CandidatePerformancesSerializer(Serializer):
    performances = PerformanceDetailsSerializer(many=True)
    average_score = serializers.IntegerField()
    team_average_score = serializers.IntegerField()