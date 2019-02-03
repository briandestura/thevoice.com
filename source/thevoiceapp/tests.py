import json

from django.db.models import Avg

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from thevoiceapp.models import User, Mentor, TeamMember, Admin, Team, PerformanceScore
from thevoiceapp.views import CandidatePerformancesView, TeamView, TeamDetailsView

from thevoiceapp.management.commands.initialise_data import initialise_data


class CandidatePerformancesViewTest(APITestCase):
    def setUp(self):
        initialise_data()

        self.candidate = TeamMember.objects.first()
        self.mentor = Mentor.objects.first()

        self.request_factory = APIRequestFactory()
        self.view = CandidatePerformancesView
        self.url = reverse('v1.candidate-performances', kwargs={'candidate_id': self.candidate.pk})
        self.request = self.request_factory.get(self.url)

    def test_returns_200(self):

        PerformanceScore.objects.filter(
            performance__team_member__team=self.candidate.team
        ).update(score=20)

        PerformanceScore.objects.filter(
            performance__team_member=self.candidate
        ).update(score=10)

        force_authenticate(self.request, self.mentor.user)
        response = self.view.as_view()(self.request, candidate_id=self.candidate.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['performances']), 1)
        self.assertEqual(response.data['average_score'], 10)
        self.assertEqual(response.data['team_average_score'], 15)

    def test_user_no_perms_returns_401(self):
        force_authenticate(self.request, self.candidate.user)
        response = self.view.as_view()(self.request, candidate_id=self.candidate.pk)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TeamViewTest(APITestCase):
    def setUp(self):
        initialise_data()

        self.candidate = TeamMember.objects.first()
        self.mentor = Mentor.objects.first()
        self.admin = Admin.objects.first()

        self.request_factory = APIRequestFactory()
        self.view = TeamView
        self.url = reverse('v1.team')
        self.request = self.request_factory.get(self.url)

    def test_mentor_returns_own_team_returns_200(self):

        force_authenticate(self.request, self.mentor.user)
        response = self.view.as_view()(self.request)

        teams = Team.objects.filter(mentor=self.mentor)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        self.assertEqual(response.data[0]['team_name'], teams[0].team_name)
        self.assertEqual(response.data[0]['average_score'], int(PerformanceScore.objects.filter(
            performance__team_member__team=teams[0]
        ).aggregate(Avg('score')).get('score__avg', 0)))

        self.assertEqual(response.data[1]['team_name'], teams[1].team_name)
        self.assertEqual(response.data[1]['average_score'], int(PerformanceScore.objects.filter(
            performance__team_member__team=teams[1]
        ).aggregate(Avg('score')).get('score__avg', 0)))

    def test_admin_returns_all_teams_returns_200(self):
        force_authenticate(self.request, self.admin.user)
        response = self.view.as_view()(self.request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        for idx, team in enumerate(Team.objects.all()):
            self.assertEqual(response.data[idx]['team_name'], team.team_name)
            self.assertEqual(response.data[idx]['average_score'], int(PerformanceScore.objects.filter(
                performance__team_member__team=team
            ).aggregate(Avg('score')).get('score__avg', 0)))

    def test_user_no_perms_returns_401(self):
        force_authenticate(self.request, self.candidate.user)
        response = self.view.as_view()(self.request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TeamDetailsViewTest(APITestCase):
    def setUp(self):
        initialise_data()

        self.candidate = TeamMember.objects.first()
        self.mentor = Mentor.objects.first()
        self.team = Team.objects.first()

        self.request_factory = APIRequestFactory()
        self.view = TeamDetailsView
        self.url = reverse('v1.team-details', kwargs={'team_id': self.team.id})
        self.request = self.request_factory.get(self.url)

    def test_returns_valid_data_returns_200(self):

        force_authenticate(self.request, self.mentor.user)
        response = self.view.as_view()(self.request, team_id=self.team.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.team.id)
        self.assertEqual(response.data['team_name'], self.team.team_name)

        self.assertEqual(response.data['average_score'], int(PerformanceScore.objects.filter(
            performance__team_member__team=self.team
        ).aggregate(Avg('score')).get('score__avg', 0)))

        self.assertEqual(response.data['members'], [
            {
                'first_name': member.user.first_name,
                'last_name': member.user.last_name
            } for member in self.team.teammember_set.all()
        ])

    def test_user_no_perms_returns_401(self):
        force_authenticate(self.request, self.candidate.user)
        response = self.view.as_view()(self.request, team_id=self.team.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)