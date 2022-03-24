from Game.Board import Action
from .base import *
from .. import NUM_OF_CARD, N_PLAYER
import random
import numpy as np

class MCTSNode:
    def __init__(self, state, action=None, parent=None):
        self.state = state
        self.wall = np.arange(NUM_OF_CARD)[state.to_array() == 0]
        self.action = action
        self.child = dict()
        self.parent = parent

        self.num = 0
        self.value = 0
        self.unvisited_actions = state.legal_tsumo_action(state.draw)

    def add_random_child(self):
        index = random.randint(0, len(self.unvisited_actions) - 1)
        action = self.unvisited_actions.pop(index)
        ron = [Action.Pass() for _ in range(N_PLAYER - 1)]
        if not action.isTsumo():
            turn = self.state.getTurn()
            discard = action.encode()
            for idx in range(1, N_PLAYER):
                ron_turn = (turn + idx + 1) % N_PLAYER
                ron[ron_turn] = self.players[ron_turn].select_ron(self.state, discard, idx)
        new_state = self.state.apply_action(self, action, ron)
        draw = np.random.choice(self.wall, 1)
        new_state.set_draw(draw)
        new_node = MCTSNode(new_state, action, self)
        self.child[draw] = new_node
        return new_node        

    def apply_result(self, value):
        self.num += 1
        self.value += value
        if self.parent is not None:
            self.parent.apply(value)

    def is_terminal(self):
        for a in self.action:
            if a == Action.Tsumo() or a == Action.Ron():
                return True
        return False

    def can_add_child(self):
        return len(self.unvisited_actions) > 0

class MCTSAgent(Agent):
    def __init__(self, rounds):
        super().__init__()
        self.num_round = rounds
        self.temperature = 0

    def set_temperature(self, temperature):
        self.temperature = temperature

    def select_tsumo(self, state, draw):
        root = MCTSNode(state)
        for _ in range(self.num_round):
            node = root
            while not (node.can_add_child() or node.is_terminal()):
                node = self.select_child(node)

            if node.can_add_child():
                node = node.add_random_child()

            result = self.simulate_game(node.game_state)
            node.apply_result(result)

        best_action = None
        best_pct = -1.0
        for child in root.child:
            if child.value > best_pct:
                best_pct = child.value
                best_action = child.action
        return best_action

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

    def dup(self):
        return MCTSAgent(self.num_round)

    @staticmethod
    def name():
        return 'mcts'

