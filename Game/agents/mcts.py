from Game.Board import Action
from .base import *
from .. import NUM_OF_CARD, N_PLAYER
import random
import numpy as np

class MCTSNode:
    def __init__(self, state, draw, action=None, parent=None):
        self.state = state
        self.draw = draw
        self.wall = [x for x in range(NUM_OF_CARD) if state.to_array()[x] == 0]
        self.action = action

        self.child = dict()
        self.parent = parent

        self.num = 0
        self.value = np.zeros(N_PLAYER)
        self.unvisited_actions = [] if self.is_terminal() else state.legal_tsumo_action(draw)

    def add_random_child(self):
        index = random.randint(0, len(self.unvisited_actions) - 1)
        action = self.unvisited_actions.pop(index)
        ron = [Action.Pass() for _ in range(N_PLAYER - 1)]
        winner = []
        if not action.isTsumo():
            turn = self.state.get_turn()
            discard = action.encode()
            for idx in range(N_PLAYER - 1):
                ron_turn = (turn + idx + 1) % N_PLAYER
                if self.state.legal_ron_action(idx, discard):
                    winner.append(ron_turn)
                    ron[idx] = Action.Ron()
        else: winner.append(self.state.get_turn())
        new_state = self.state.apply_action(action, ron)
        if winner or not self.wall:
            draw = None
            new_node = MCTSNode(new_state, tuple(winner), action, self)
        else:
            draw = random.choice(self.wall)
            new_state.set_draw(draw)
            new_node = MCTSNode(new_state, draw, action, self)
        if draw in self.child:
            self.child[draw].append(new_node)
        else: self.child[draw] = [new_node]
        return new_node        

    def apply_result(self, value):
        self.num += 1
        self.value += value

    def is_terminal(self):
        return isinstance(self.draw, tuple)

    def can_add_child(self):
        return len(self.unvisited_actions) > 0

    def average_point(self):
        if self.num == 0: return self.value
        return self.value / self.num

class MCTSAgent(Agent):
    def __init__(self, encoder, rounds = 128):
        super().__init__()
        self.num_round = rounds
        self.temperature = 0
        self.encoder = encoder

    def set_temperature(self, temperature):
        self.temperature = temperature

    def select_tsumo(self, state, draw):
        root = MCTSNode(state, draw)
        for _ in range(self.num_round):
            node = root
            while not (node.can_add_child() or node.is_terminal()):
                node = self.select_child(node)

            if node.can_add_child():
                node = node.add_random_child()

            node, result = self.simulate_game(node)
            while node is not None:
                node.apply_result(result)
                node = node.parent

        best_action = None
        best_pct = -1.0
        turn = state.get_turn()
        for childs in root.child.values():
            for child in childs:
                child_pct = child.average_point()[turn]
                if child_pct > best_pct:
                    best_pct = child_pct
                    best_action = child.action

        if self._tsumo_collector is not None:
            encoded_state = self.encoder.encode(state.to_array(), 0)
            self._tsumo_collector.record_episode(
                encoded_state, best_action.encode())
        return best_action

    def select_ron(self, state, discard, idx):
        ron_able = state.legal_ron_action(idx, discard)
        if ron_able:
            selection = Action.Ron()
            if self._ron_collector is not None:
                encoded_state = self.encoder.encode(state.to_array(discard), idx)
                self._ron_collector.record_episode(
                    encoded_state, ron_able)
        else:
            selection = Action.Pass()
        return selection

    def _score(self, parent_rollouts, child_rollouts, average_point):
        assert child_rollouts
        exploration = np.sqrt(np.log(parent_rollouts) / child_rollouts)
        return average_point + self.temperature * exploration

    def simulate_game(self, node):
        if node.is_terminal():
            return node, node.value

        while not node.is_terminal():
            node = node.add_random_child()

        result = np.zeros(4)
        parent = node.parent
        for w in node.draw:
            turn = parent.state.get_turn()
            if w == turn:
                card, dora = parent.draw, parent.state.dora
                point = parent.state.hand[turn].point(card, dora)
                point //= N_PLAYER - 1
                result = -point * np.ones(N_PLAYER, dtype='int')
                result[turn] = point * (N_PLAYER - 1)
            else:
                card = parent.action.encode()
                dora = parent.state.dora
                point = parent.state.hand[w].point(card, dora) 
                result[w] += point
                result[turn] -= point
        return node, result
    
    def select_child(self, node):
        best_score = -1
        best_child = None
        turn = node.state.get_turn()
        for childs in node.child.values():
            for child in childs:
                score = self._score(
                    node.num,
                    child.num,
                    child.average_point()[turn]
                )
                if score > best_score:
                    best_score = score
                    best_child = child
        return best_child

    def dup(self):
        return MCTSAgent(self.encoder, self.num_round)

    @staticmethod
    def name():
        return 'mcts'

