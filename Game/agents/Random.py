from .. import Action
from .base import Agent
import random

class RandomAgent(Agent):
    def __init__(self):
        super().__init__()

    def select_tsumo(self, state, draw):
        actions = state.legal_tsumo_action(draw)
        if Action.Tsumo() in actions: selection = Action.Tsumo()
        else:selection = random.choice(actions)

        if self._tsumo_collector is not None:
            self._tsumo_collector.record_episode(
                state.to_array(), selection.Encode())
        return selection

    def select_ron(self, state, discard, turn):
        ron_able = state.legal_ron_action(turn, discard)
        if ron_able:
            selection = Action.Ron()
            if self._ron_collector is not None:
                self._ron_collector.record_episode(
                    state.to_array(discard, turn), ron_able)
        else:
            selection = Action.Pass()
        return selection

    @staticmethod
    def name():
        return 'random'
