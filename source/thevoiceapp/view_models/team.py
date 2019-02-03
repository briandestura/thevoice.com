from django.db.models import Avg

from thevoiceapp.models import TeamMember, PerformanceScore


class TeamDetailViewModel(object):
    def __init__(self, team):
        self.id = team.id
        self.team_name = team.team_name
        self.mentor = team.mentor.user

        members = TeamMember.objects.select_related('user').filter(team_id=team.id)
        self.members = [
            member.user for member in members
        ]
        self.average_score = PerformanceScore.objects.filter(
            performance__team_member__user__in=self.members
        ).aggregate(Avg('score')).get('score__avg', 0)