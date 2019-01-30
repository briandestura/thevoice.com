from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_jwt.settings import api_settings

from rest_framework_jwt.views import JSONWebTokenAPIView

from thevoiceapp.authentication.jwt_utils import jwt_encode_handler

from thevoiceapp.models import Team, Performance, User, PerformanceScore, Candidate

from thevoiceapp.serializers.candidate import CandidatePerformancesSerializer
from thevoiceapp.view_models.candidate import CandidatePerformancesViewModel

from thevoiceapp.serializers.team import TeamDetailSerializer
from thevoiceapp.view_models.team import TeamDetailViewModel

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class ObtainJwtToken(JSONWebTokenAPIView):
    def post(self, request, *args, **kwargs):

        token = request.data.get('token', False)

        if token:
            user = User.objects.get(id=token)
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response(jwt_response_payload_handler(token, user, request))

        return Response(status=status.HTTP_400_BAD_REQUEST, data="Missing token")


class CandidatePerformancesView(APIView):
    def get(self, request, candidate_id, *args, **kwargs):

        candidate_performance_vm = CandidatePerformancesViewModel(
            candidate_id=candidate_id
        )

        return Response(data=CandidatePerformancesSerializer(candidate_performance_vm).data)


class TeamView(APIView):
    def get(self, request, *args, **kwargs):

        teams_vm = []

        for team in self._get_teams_by_user(request.user):
            teams_vm.append(TeamDetailViewModel(team))

        return Response(data=TeamDetailSerializer(teams_vm, many=True).data)

    def _get_teams_by_user(self, user):

        if hasattr(user, 'admin'):
            return Team.objects.all()

        return Team.objects.filter(mentor_id=user.id)


class TeamDetailsView(APIView):
    def get(self, request, team_id, *args, **kwargs):
        team = Team.objects.get(id=team_id)
        team_vm = TeamDetailViewModel(team)

        return Response(data=TeamDetailSerializer(team_vm).data)