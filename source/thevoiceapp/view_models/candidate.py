from django.db.models import Avg

from thevoiceapp.models import Performance, PerformanceScore, Team, TeamMember


class CandidatePerformancesViewModel(object):
    def __init__(self, candidate_id):

        teammember = TeamMember.objects.get(user_id=candidate_id)

        self.performances = Performance.objects.filter(team_member=teammember)

        self.average_score = PerformanceScore.objects.filter(
            performance__team_member=teammember
        ).aggregate(Avg('score')).get('score__avg', 0)

        self.team_average_score = PerformanceScore.objects.filter(
            performance__team_member__team=teammember.team
        ).aggregate(Avg('score')).get('score__avg', 0)