from .. import Action
import random

class RandomAgent:
    def __init__(self):
        pass

    def select_action(self, state, card, turn):
        actions = state.action(turn, card)
        if Action.Tsumo() in actions: return Action.Tsumo()
        if Action.Ron() in actions: return Action.Ron()
        return random.choice(actions)
