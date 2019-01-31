from django.db.models import Avg

from thevoiceapp.models import Performance, PerformanceScore, Candidate, Team, TeamMember


class CandidatePerformancesViewModel(object):
    def __init__(self, candidate_id):

        teammember = TeamMember.objects.get(candidate_id=candidate_id)

        self.performances = Performance.objects.filter(candidate=teammember.candidate)

        self.average_score = PerformanceScore.objects.filter(
            performance__candidate=teammember.candidate
        ).aggregate(Avg('score')).get('score__avg', 0)

        self.team_average_score = PerformanceScore.objects.filter(
            performance__candidate__teammember__team=teammember.team
        ).aggregate(Avg('score')).get('score__avg', 0)