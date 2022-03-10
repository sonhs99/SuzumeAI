from .. import Action
from .base import Agent
import random

class RandomAgent(Agent):
    def __init__(self, encode):
        super().__init__()
        self._encode = encode

    def select_tsumo(self, state, draw):
        actions = state.legal_tsumo_action(draw)
        if Action.Tsumo() in actions: selection = Action.Tsumo()
        else:selection = random.choice(actions)

        if self._tsumo_collector is not None:
            encoded_state = self._encode.encode(state.to_array(), 0)
            self._tsumo_collector.record_episode(
                encoded_state, selection.Encode())
        return selection

    def select_ron(self, state, discard, idx):
        ron_able = state.legal_ron_action(idx, discard)
        if ron_able:
            selection = Action.Ron()
            if self._ron_collector is not None:
                encoded_state = self._encode.encode(state.to_array(discard), idx)
                self._ron_collector.record_episode(
                    encoded_state, ron_able)
        else:
            selection = Action.Pass()
        return selection

    @staticmethod
    def name():
        return 'random'
