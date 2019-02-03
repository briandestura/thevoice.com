import sys, traceback

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_jwt.settings import api_settings

from rest_framework_jwt.views import JSONWebTokenAPIView

from thevoiceapp.authentication.jwt_utils import jwt_encode_handler

from thevoiceapp.models import Team, TeamMember, User

from thevoiceapp.serializers.candidate import CandidatePerformancesSerializer
from thevoiceapp.view_models.candidate import CandidatePerformancesViewModel

from thevoiceapp.serializers.team import TeamDetailSerializer
from thevoiceapp.view_models.team import TeamDetailViewModel

from thevoiceapp.services import TheVoiceError
from thevoiceapp.services.candidate import CandidateService
from thevoiceapp.services.team import TeamService

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class ObtainJwtToken(JSONWebTokenAPIView):
    def post(self, request, *args, **kwargs):

        token = request.data.get('token', False)

        if token:
            user = get_object_or_404(User, id=token)
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response(jwt_response_payload_handler(token, user, request))

        return Response(status=status.HTTP_400_BAD_REQUEST, data="Missing token")


class CandidatePerformancesView(APIView):
    def get(self, request, candidate_id, *args, **kwargs):

        try:
            teammember = get_object_or_404(TeamMember, user_id=candidate_id)

            candidate_service = CandidateService(teammember)

            candidate_performance_vm = CandidatePerformancesViewModel(
                performances=candidate_service.get_performances(),
                average_score=candidate_service.get_average_score(),
                team_average_score=candidate_service.get_team_average_score(),
            )

        except TheVoiceError:
            exception = "".join(traceback.format_exception(*sys.exc_info()))
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(exception))

        return Response(data=CandidatePerformancesSerializer(candidate_performance_vm).data)


class TeamView(APIView):
    def get(self, request, *args, **kwargs):

        teams_vm = []

        try:
            for team in self._get_teams_by_user(request.user):
                team_service = TeamService(team=team)
                teams_vm.append(
                    TeamDetailViewModel(
                        team=team,
                        members=team_service.get_team_members(),
                        average_score=team_service.get_team_average_score()
                    )
                )

        except TheVoiceError:
            exception = "".join(traceback.format_exception(*sys.exc_info()))
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(exception))

        return Response(data=TeamDetailSerializer(teams_vm, many=True).data)

    def _get_teams_by_user(self, user):

        if hasattr(user, 'admin'):
            return Team.objects.all()

        return Team.objects.filter(mentor_id=user.id)


class TeamDetailsView(APIView):
    def get(self, request, team_id, *args, **kwargs):

        try:
            team = get_object_or_404(Team, id=team_id)
            team_service = TeamService(team=team)
            team_vm = TeamDetailViewModel(
                team=team,
                members=team_service.get_team_members(),
                average_score=team_service.get_team_average_score()
            )

        except TheVoiceError:
            exception = "".join(traceback.format_exception(*sys.exc_info()))
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(exception))

        return Response(data=TeamDetailSerializer(team_vm).data)