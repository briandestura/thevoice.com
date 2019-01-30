from rest_framework.response import Response
from rest_framework.views import APIView

from thevoiceapp.models import Team
from thevoiceapp.serializers.team import TeamDetailSerializer
from thevoiceapp.view_models.team import TeamDetailViewModel


class CandidatePerformancesView(APIView):
    def get(self, request, candidate_id, *args, **kwargs):

        data = {
            "performances": [
                {
                    "song_name": "song",
                    "date": "date"
                }
            ],
            "average_score": 100,
            "team_average_score": 100
        }


        return Response()


class TeamView(APIView):
    def get(self, request, *args, **kwargs):

        teams_vm = []

        for team in self._get_teams_by_user():
            teams_vm.append(TeamDetailViewModel(team))

        return Response(data=TeamDetailSerializer(teams_vm, many=True).data)

    def _get_teams_by_user(self):

        if True:
            return Team.objects.all()
        return Team.objects.filter(mentor_id=1)


class TeamDetailsView(APIView):
    def get(self, request, team_id, *args, **kwargs):
        team = Team.objects.get(id=team_id)
        team_vm = TeamDetailViewModel(team)

        return Response(data=TeamDetailSerializer(team_vm).data)