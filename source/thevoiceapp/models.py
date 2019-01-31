from datetime import datetime

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(models.Model):
    id = models.AutoField(primary_key=True, db_column='user_id')
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'user'

    def is_authenticated(self):
        return True


class Admin(models.Model):
    user = models.OneToOneField(User, primary_key=True, db_column='user_id', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_admin'


class Mentor(models.Model):
    user = models.OneToOneField(User, primary_key=True, db_column='user_id', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_mentor'


class Candidate(models.Model):
    user = models.OneToOneField(User, primary_key=True, db_column='user_id', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_candidate'


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=255)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)

    class Meta:
        db_table = 'team'


class TeamMember(models.Model):
    candidate = models.OneToOneField(Candidate, primary_key=True, db_column='candidate_id', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        db_table = 'team_member'


class Performance(models.Model):
    id = models.AutoField(primary_key=True)
    song_name = models.CharField(max_length=255)
    candidate = models.OneToOneField(Candidate, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'performance'


class PerformanceScore(models.Model):
    id = models.AutoField(primary_key=True)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        db_table = 'performance_score'
        unique_together = ('performance', 'mentor')
