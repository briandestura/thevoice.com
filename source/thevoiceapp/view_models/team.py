class TeamDetailViewModel(object):
    def __init__(self, team, members, average_score):
        self.id = team.id
        self.team_name = team.team_name
        self.mentor = team.mentor.user
        self.members = members
        self.average_score = average_score