from .. import Board

class UserAgent:
    def __init__(self):
        pass

    def render(self, state, turn):
        pass

    def render_action(self, actions):
        pass

    def selector(self):
        return 0

    def select_action(self, state, card, turn):
        actions = state.action(turn, card)
        self.render(state, turn)
        self.render_action(actions)
        return actions[self.selector()]
        