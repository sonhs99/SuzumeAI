from .. import Action
import random

class RandomAgent():
    def __init__(self):
        self._tsumo_collector = None
        self._ron_collector = None

    def set_collector(self, tsumo, ron):
        self._tsumo_collector = tsumo
        self._ron_collector = ron

    def select_tsumo(self, state, draw):
        actions = state.legal_tsumo_action(draw)
        if Action.Tsumo() in actions: selection = Action.Tsumo()
        else:
            selection = random.choice(actions)
            if self._tsumo_collector is not None:
                self._tsumo_collector.record_episode(state, selection.encode())
        return selection

    def select_ron(self, state, discard, turn):
        actions = state.legal_ron_action(turn, discard)
        if Action.Ron() in actions:
            selection = Action.Ron()
            if self._ron_collector is not None:
                self._ron_collector.record_episode(state, selection.encode())
        else: selection = Action.Pass()
        return selection

    @staticmethod
    def name():
        return 'random'
