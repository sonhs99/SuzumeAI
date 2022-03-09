from .Card import CardTable
from .Hand import Hand, DiscardZone
from . import Type
import random
import numpy as np

__all__ = [
    'Action',
    'State',
    'Board'
]

table = CardTable()

class Action:
    _tsumo = Type.NUM_OF_CARD
    _ron = Type.NUM_OF_CARD + 1
    _pass = Type.NUM_OF_CARD + 2
    def __init__(self, idx):
        self._idx = idx

    @staticmethod
    def Discard(num):
        return Action(num)

    @staticmethod
    def Tsumo():
        return Action(Action._tsumo)

    @staticmethod
    def Ron():
        return Action(Action._ron)

    @staticmethod
    def Pass():
        return Action(Action._pass)

    def Encode(self):
        return self._idx

    def isTsumo(self):
        return self._idx == Action._tsumo

    def isRon(self):
        return self._idx == Action._ron

    def isPass(self):
        return self._idx == Action._pass

    def __str__(self):
        string = None
        if self.isTsumo(): string = 'Tsumo'
        elif self.isRon(): string = 'Ron'
        elif self.isPass(): string = 'Pass'
        else: string = f'Discard:{self._idx}'
        return 'Action(' + string + ')'

class State:
    def __init__(self, turn, dora, hand, discard):
        self.turn = turn
        self.dora = dora
        self.hand = hand
        self.discard = discard
        self.draw = None

    @staticmethod
    def init(deck, turn):
        hand = [Hand(deck[i*5:(i + 1)*5]) for i in range(Type.N_PLAYER)]
        discard = [DiscardZone() for _ in range(Type.N_PLAYER)]
        return (
            State(turn, deck[Type.N_PLAYER*5], hand, discard),
            deck[Type.N_PLAYER*5 + 1:])

    def apply_action(self, draw, tsumo, ron):
        self.draw = draw
        if tsumo.isTsumo() or Action.Ron() in ron:
            return self

        from copy import deepcopy
        hand = deepcopy(self.hand)
        discard = deepcopy(self.discard)
        discarded_card = tsumo.Encode()
        hand[self.turn].change(draw, discarded_card)
        discard[self.turn].collect(discarded_card)
        return State(
            (self.turn + 1) % Type.N_PLAYER,
            self.dora,
            hand, 
            discard)

    def legal_tsumo_action(self, card):
        actions = []
        for c in self.hand[self.turn].toArray():
            actions.append(Action.Discard(c))
        actions.append(Action.Discard(card))
        if self.hand[self.turn].point(card, self.dora) >= 5:
            actions.append(Action.Tsumo())
        return actions

    def legal_ron_action(self, turn, card):
        if self.hand[turn].point(card, self.dora) >= 5 and \
            not self.hand[turn].isDiscarded(card):
            return True
        else: return False

    def getTurn(self):
        return self.turn
        
    # Index of State Array
    # 0 : Deck
    # 1 : Dora
    # 2 : Draw / Discard
    # 3 ~ N + 2 : Hand
    # N + 3 ~ 2N + 2 : Discard

    def to_array(self, discard=None, turn=None):
        state = np.zeros(Type.NUM_OF_CARD, dtype=int)

        state[self.dora] = 1
        state[self.draw] = 2
        if turn is None: turn = self.turn
        for i in range(Type.N_PLAYER):
            _turn = (turn + i) % Type.N_PLAYER
            state += (self.hand[_turn]._hand == 1).astype('int') * (_turn + 3)
            state += (self.hand[_turn]._hand == 2).astype('int') * (_turn + 3 + Type.N_PLAYER)
        
        if discard is not None:
            state[self.draw] = self.turn + 3
            state[discard] = 2

        return state

class Board:
    def __init__(self, players, tsumo_collector=None, ron_collector=None, start_turn=0):
        deck = list(range(Type.NUM_OF_CARD))
        random.shuffle(deck)
        self.players = players
        self.state, self.deck = State.init(deck, start_turn)
        self.tsumo_collector = tsumo_collector
        self.ron_collector = ron_collector
        self.start_turn = start_turn
        self.point = np.zeros(len(self.players), dtype='int')

    def init(self):
        deck = list(range(Type.NUM_OF_CARD))
        random.shuffle(deck)
        self.state, self.deck = State.init(deck, self.start_turn)

    def prepare(self):
        self.start_turn = (self.start_turn + 1) % len(self.players) 
        self.init()

    def play(self):
        n_player = len(self.players)
        result = np.zeros(n_player, dtype='int')
        winner = []
        for draw in self.deck:
            turn = self.state.getTurn()
            ron = [Action.Pass() for _ in range(n_player - 1)]
            tsumo = self.players[turn].select_tsumo(self.state, draw)

            if not tsumo.isTsumo():
                discard = tsumo.Encode()
                for idx in range(n_player - 1):
                    ron_turn = (turn + idx + 1) % n_player
                    ron[idx] = self.players[ron_turn].select_ron(self.state, discard, ron_turn)
                    if ron[idx].isRon(): winner.append(ron_turn)
            else: winner.append(turn)
            if winner: break
            self.state = self.state.apply_action(draw, tsumo, ron)

        for w in winner:
            if w == turn:
                card = self.state.draw
                dora = self.state.dora
                point = self.state.hand[w].point(card, dora) +\
                    2 if w == self.start_turn else 0
                point //= n_player - 1
                result = -point * np.ones(n_player, dtype='int')
                result[w] = point * (n_player - 1)
            else:
                card = tsumo.Encode()
                dora = self.state.dora
                point = self.state.hand[w].point(card, dora) +\
                    2 if w == self.start_turn else 0
                result[w] += point
                result[turn] -= point

        self.point += result

        if self.tsumo_collector is not None:
            for collector, r in zip(self.tsumo_collector, result):
                collector.complete_sub_episode(r)
        if self.ron_collector is not None:
            for collector, r in zip(self.ron_collector, result):
                collector.complete_sub_episode(r)

    def rank(self):
        ranking = np.array(self.point).argsort()
        result = np.zeros(len(self.players))
        result[0] == -10
        result[-1] == 10

        if self.tsumo_collector is not None:
            for collector, r in zip(self.tsumo_collector, result[ranking]):
                collector.complete_episode(r)
        if self.ron_collector is not None:
            for collector, r in zip(self.ron_collector, result[ranking]):
                collector.complete_episode(r)
        