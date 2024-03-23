import random
from constants import TRUTH_PROMPTS, DARE_PROMPTS

class Game:
    def __init__(self):
        self.players = []
        self.current_player_index = 0

    def add_player(self, player):
        self.players.append(player)

    def get_current_player(self):
        return self.players[self.current_player_index]

    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def get_truth_prompt(self):
        return random.choice(TRUTH_PROMPTS)

    def get_dare_prompt(self):
        return random.choice(DARE_PROMPTS)
