from .. import Board
import random

class RandomAgent:
    def __init__(self):
        pass

    def select_action(self, state, card, turn):
        return random.choice(state.action(turn, card))
