from .. import Board
import random
import numpy as np

class SuzumeAgent:
    def __init__(self):
        pass

    def select_action(self, state, card, turn):
        actions = state.action(turn, card)
        if Board.Action.Tsumo() in actions: return Board.Action.Tsumo()
        if Board.Action.Ron() in actions: return Board.Action.Ron()
        return random.choice(state.action(turn, card))

    @staticmethod
    def encode(state, action):
        pass