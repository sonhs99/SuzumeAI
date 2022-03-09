class Agent:
    def __init__(self):
        self._tsumo_collector = None
        self._ron_collector = None

    def set_collector(self, tsumo, ron):
        self._tsumo_collector = tsumo
        self._ron_collector = ron

    def select_tsumo(self, state, draw):
        raise NotImplementedError()

    def select_ron(self, state, discard, turn):
        raise NotImplementedError()

    @staticmethod
    def name():
        return 'Not Implemented'