from . import TheVoiceError
from django.db.models import Avg

from thevoiceapp.models import TeamMember, PerformanceScore


class TeamService(object):
    def __init__(self, team):
        self.team = team
        self.members = []
        self.average_score = 0

    def get_team_members(self):

        self.members = [
            member.user for member in TeamMember.objects.select_related('user').filter(team_id=self.team.id)
        ]

        return self.members

    def get_team_average_score(self):

        self.average_score = PerformanceScore.objects.filter(
            performance__team_member__user__in=self.get_team_members()
        ).aggregate(Avg('score')).get('score__avg', 0)

        return self.average_score
