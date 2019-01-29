from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True, db_column='user_id')
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'user'


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
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    class Meta:
        db_table = 'team_member'
        unique_together = ('team', 'candidate')


class Performance(models.Model):
    id = models.AutoField(primary_key=True)
    song_name = models.CharField(max_length=255)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    class Meta:
        db_table = 'performance'


class PerformanceScore(models.Model):
    id = models.AutoField(primary_key=True)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        db_table = 'performance_score'
        unique_together = ('performance', 'mentor')
