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

    def encode(self):
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
    def __init__(self, turn, dora, hand):
        self.turn = turn
        self.dora = dora
        self.hand = hand
        self.draw = None

    @staticmethod
    def init(deck, turn):
        hand = [Hand(deck[i*5:(i + 1)*5]) for i in range(Type.N_PLAYER)]
        return (
            State(turn, deck[Type.N_PLAYER*5], hand),
            deck[Type.N_PLAYER*5 + 1:])

    def set_draw(self, draw):
        self.draw = draw

    def apply_action(self, tsumo, ron):
        if tsumo.isTsumo() or Action.Ron() in ron:
            return self

        from copy import deepcopy
        hand = deepcopy(self.hand)
        discarded_card = tsumo.encode()
        hand[self.turn].change(self.draw, discarded_card)
        return State(
            (self.turn + 1) % Type.N_PLAYER,
            self.dora,
            hand)

    def legal_tsumo_action(self, card):
        actions = []
        for c in self.hand[self.turn].to_array():
            actions.append(Action.Discard(c))
        actions.append(Action.Discard(card))
        if self.hand[self.turn].point(card, self.dora) >= 5:
            actions.append(Action.Tsumo())
        return actions

    def legal_ron_action(self, idx, card):
        turn = (idx + self.turn + 1) % Type.N_PLAYER
        if self.hand[turn].point(card, self.dora) >= 5 and \
            not self.hand[turn].isDiscarded(card):
            return True
        else: return False

    def get_turn(self):
        return self.turn
        
    # Index of State Array
    # 0 : Deck
    # 1 : Dora
    # 2 : Draw / Discard
    # 3 ~ N + 2 : Hand
    # N + 3 ~ 2N + 2 : Discard

    def to_array(self, discard=None):
        state = np.zeros(Type.NUM_OF_CARD, dtype=int)

        state[self.dora] = 1
        state[self.draw] = 2
        for i in range(Type.N_PLAYER):
            _turn = (self.turn + i) % Type.N_PLAYER
            for card, idx in enumerate(self.hand[_turn]._hand):
                if idx == 1: state[card] = i * 2 + 3
                elif idx == 2: state[card] = i * 2 + 4
        
        if discard is not None:
            state[self.draw] = 4
            state[discard] = 2
        return state

class Board:
    def __init__(self, players, logger=None, start_turn=0):
        deck = list(range(Type.NUM_OF_CARD))
        random.shuffle(deck)
        self.players = players
        self.state, self.deck = State.init(deck, start_turn)
        self.logger = logger
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
        turn = self.state.get_turn()
        self.logger.apply_init(
            [hand.to_array() for hand in self.state.hand],
            self.state.dora,
            turn
        )
        for draw in self.deck:
            self.state.set_draw(draw)
            turn = self.state.get_turn()
            ron = [Action.Pass() for _ in range(n_player - 1)]
            tsumo = self.players[turn].select_tsumo(self.state, draw)

            if not tsumo.isTsumo():
                discard = tsumo.encode()
                for idx in range(n_player - 1):
                    ron_turn = (turn + idx + 1) % n_player
                    ron[idx] = self.players[ron_turn].select_ron(self.state, discard, idx)
                    if ron[idx].isRon(): winner.append(ron_turn)
            else: winner.append(turn)
            self.state = self.state.apply_action(tsumo, ron)
            if self.logger is not None:
                self.logger.apply_turn(draw, tsumo.encode(), [
                    (turn + idx + 1) % n_player
                    for idx in range(n_player - 1) if ron[idx].isRon()
                ])
            if winner: break

        for w in winner:
            if w == turn:
                card = self.state.draw
                dora = self.state.dora
                assert self.state.hand[w].point(card, dora) >= 5, str(
                    self.state.hand[w]._hand)
                point = self.state.hand[w].point(card, dora) +\
                    (2 if w == self.start_turn else 0)
                point //= n_player - 1
                result = -point * np.ones(n_player, dtype='int')
                result[w] = point * (n_player - 1)
            else:
                card = tsumo.encode()
                dora = self.state.dora
                point = self.state.hand[w].point(card, dora) +\
                    (2 if w == self.start_turn else 0)
                result[w] += point
                result[turn] -= point

        self.point += result
        if self.logger is not None:
            self.logger.apply_result(result)

    def rank(self):
        ranking = np.array(self.point).argsort()
        result = np.zeros(len(self.players), dtype='int')
        result[0] = -10
        result[-1] = 10
        if self.logger is not None:
            self.logger.apply_uma(result[ranking])
