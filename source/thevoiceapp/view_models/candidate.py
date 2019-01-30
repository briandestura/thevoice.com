from django.db.models import Avg

from thevoiceapp.models import Performance, PerformanceScore, Candidate


class CandidatePerformancesViewModel(object):
    def __init__(self, candidate_id):

        candidate = Candidate.objects.prefetch_related('teammember_set').get(user_id=candidate_id)

        self.performances = Performance.objects.filter(candidate=candidate)

        self.average_score = PerformanceScore.objects.filter(
            performance__candidate=candidate
        ).aggregate(Avg('score')).get('score__avg', 0)

        self.team_average_score = PerformanceScore.objects.select_related('mentor__team').filter(
            mentor__team=candidate.teammember_set.all()[0].team
        ).aggregate(Avg('score')).get('score__avg', 0)