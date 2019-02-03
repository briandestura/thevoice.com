from django.test import TestCase

from thevoiceapp.models import User, Mentor, TeamMember, Admin, Team, PerformanceScore
from thevoiceapp.management.commands.initialise_data import initialise_data
from thevoiceapp.services.candidate import CandidateService
from thevoiceapp.services.team import TeamService


class CandidateServiceTestCase(TestCase):
    def setUp(self):
        initialise_data()
        self.candidate = TeamMember.objects.first()

    def test_candidate_get_performances_returns_correct_data(self):
        performances = CandidateService(team_member=self.candidate).get_performances()
        self.assertEqual(1, len(performances))
        self.assertEqual(performances[0].song_name, 'Song 1')
        self.assertEqual(performances[0].team_member, self.candidate)

    def test_candidate_get_average_score_returns_correct_data(self):
        PerformanceScore.objects.filter(
            performance__team_member=self.candidate
        ).update(score=10)

        # 10 10 10
        self.assertEqual(10, CandidateService(team_member=self.candidate).get_average_score())

    def test_candidate_get_team_average_score_returns_correct_data(self):
        PerformanceScore.objects.filter(
            performance__team_member__team=self.candidate.team
        ).update(score=20)

        PerformanceScore.objects.filter(
            performance__team_member=self.candidate
        ).update(score=10)

        # 10 10 10 20 20 20
        self.assertEqual(15, CandidateService(team_member=self.candidate).get_team_average_score())


class TeamServiceTestCase(TestCase):
    def setUp(self):
        initialise_data()
        self.mentor = Mentor.objects.first()
        self.teams = Team.objects.filter(mentor=self.mentor)

    def test_get_team_members_returns_correct_data(self):
        members = TeamService(self.teams[0]).get_team_members()
        self.assertEqual(2, len(members))
        self.assertEqual('1', members[0].last_name)
        self.assertEqual('2', members[1].last_name)

    def test_get_team_average_score_returns_correct_data(self):
        PerformanceScore.objects.filter(
            performance__team_member__team=self.teams[0]
        ).update(score=45)

        self.assertEqual(45, int(TeamService(self.teams[0]).get_team_average_score()))

