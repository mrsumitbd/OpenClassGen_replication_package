class LeaderboardEntry(object):
    def __init__(self, init_dict):
        self.name = init_dict.get('name', '')
        self.score = init_dict.get('score', 0)
        self.rank = init_dict.get('rank', 0)

    def __repr__(self):
        return f"LeaderboardEntry(name='{self.name}', score={self.score}, rank={self.rank})"