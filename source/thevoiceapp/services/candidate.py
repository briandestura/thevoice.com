from . import TheVoiceError

from django.db.models import Avg

from thevoiceapp.models import Performance, PerformanceScore


class CandidateService(object):
    def __init__(self, team_member):
        self.team_member = team_member
        self.performances = []
        self.average_score = 0
        self.team_average_score = 0

    def get_performances(self):

        self.performances = Performance.objects.filter(team_member=self.team_member)

        return self.performances

    def get_average_score(self):

        self.average_score = PerformanceScore.objects.filter(
            performance__team_member=self.team_member
        ).aggregate(Avg('score')).get('score__avg', 0)

        return self.average_score

    def get_team_average_score(self):

        self.team_average_score = PerformanceScore.objects.filter(
            performance__team_member__team=self.team_member.team
        ).aggregate(Avg('score')).get('score__avg', 0)

        return self.team_average_score