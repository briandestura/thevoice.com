import random

from django.core.management.base import BaseCommand

from thevoiceapp.models import Admin, Mentor, User, Team, TeamMember, Performance, PerformanceScore


def initialise_data():

    Admin.objects.all().delete()
    Mentor.objects.all().delete()
    User.objects.all().delete()
    Team.objects.all().delete()
    TeamMember.objects.all().delete()
    Performance.objects.all().delete()
    PerformanceScore.objects.all().delete()

    Admin.objects.create(
        user=User.objects.create(first_name='Admin', last_name='1')
    )

    User.objects.bulk_create([
        User(first_name='Contestant', last_name=str(c)) for c in range(1,7)
    ])
    candidates = User.objects.filter(first_name='Contestant')

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
        TeamMember(team=teams[0], user=candidates[0]),
        TeamMember(team=teams[0], user=candidates[1]),
        TeamMember(team=teams[1], user=candidates[2]),
        TeamMember(team=teams[1], user=candidates[3]),
        TeamMember(team=teams[2], user=candidates[4]),
        TeamMember(team=teams[3], user=candidates[5]),
    ])
    team_members = TeamMember.objects.all()

    Performance.objects.bulk_create([
        Performance(song_name='Song {}'.format(idx + 1), team_member=team_members[idx]) for idx, val in enumerate(team_members)
    ])
    performances = Performance.objects.all()

    PerformanceScore.objects.bulk_create([
        PerformanceScore(performance=p, mentor=m, score=random.randint(1, 100)) for m in mentors for p in performances
    ])


class Command(BaseCommand):
    help = 'Initialise data for thevoice app'
    requires_system_checks = False

    def handle(self, *args, **options):
        initialise_data()
