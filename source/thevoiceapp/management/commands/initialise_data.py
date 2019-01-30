import random

from django.core.management.base import BaseCommand

from thevoiceapp.models import Candidate, Mentor, User, Team, TeamMember, Performance, PerformanceScore


class Command(BaseCommand):
    help = 'Initialise data for thevoice app'
    requires_system_checks = False

    def handle(self, *args, **options):

        Candidate.objects.all().delete()
        Mentor.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()
        TeamMember.objects.all().delete()
        Performance.objects.all().delete()
        PerformanceScore.objects.all().delete()

        Candidate.objects.bulk_create([
            Candidate(user=User.objects.create(first_name='Contestant', last_name=str(c))) for c in range(6)
        ])
        candidates = Candidate.objects.all()

        Mentor.objects.bulk_create([
            Mentor(user=User.objects.create(first_name='Mentor', last_name=str(m))) for m in range(3)
        ])
        mentors = Mentor.objects.all()

        Team.objects.bulk_create([
            Team(team_name='Team 1', mentor=mentors[0]),
            Team(team_name='Team 2', mentor=mentors[1]),
            Team(team_name='Team 3', mentor=mentors[2]),
            Team(team_name='Team 4', mentor=mentors[0]),
        ])
        teams = Team.objects.all()

        TeamMember.objects.bulk_create([
            TeamMember(team=teams[0], candidate=candidates[0]),
            TeamMember(team=teams[0], candidate=candidates[1]),
            TeamMember(team=teams[1], candidate=candidates[2]),
            TeamMember(team=teams[1], candidate=candidates[3]),
            TeamMember(team=teams[2], candidate=candidates[4]),
            TeamMember(team=teams[3], candidate=candidates[5]),
        ])

        Performance.objects.bulk_create([
            Performance(song_name='Song {}'.format(idx + 1), candidate=candidates[idx]) for idx, val in enumerate(candidates)
        ])
        performances = Performance.objects.all()

        PerformanceScore.objects.bulk_create([
            PerformanceScore(performance=p, mentor=m, score=random.randint(1, 100)) for m in mentors for p in performances
        ])
