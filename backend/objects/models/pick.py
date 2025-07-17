class Pick:
    def __init__(self, pick):
        self.draft_id = pick[0]
        self.player_id = pick[1]
        self.round_num = pick[2]
        self.pick_num = pick[3]