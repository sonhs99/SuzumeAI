from .. import Action
import random
import numpy as np

class OpenAgent:
    def __init__(self, encoder, nn_tsumo):
        self.encoder = encoder
        self.nn_tsumo = nn_tsumo

    def select_action(self, state, card, turn):
        actions = state.action(turn, card)
        if Action.Pass() in actions:
            return Action.Pass()
        if Action.Ron() in actions:
            return Action.Ron()
        return random.choice(state.action(turn, card))

    @staticmethod
    def encode(state, action):
        pass