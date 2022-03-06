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

    def apply(self, draw, actions):
        self.draw = draw
        for action in actions:
            if action.isTsumo() or action.isRon():
                return self

        from copy import deepcopy
        hand = deepcopy(self.hand)
        discard = deepcopy(self.discard)
        discarded_card = actions[self.turn].Encode()
        hand[self.turn].change(draw, discarded_card)
        discard[self.turn].collect(discarded_card)
        return State(
            (self.turn + 1) % Type.N_PLAYER,
            self.dora,
            hand, 
            discard)

    def action(self, turn, card):
        actions = []
        if turn == self.turn:
            for c in self.hand[turn].toArray():
                actions.append(Action.Discard(c))
            actions.append(Action.Discard(card))
            if self.hand[turn].point(card, self.dora) >= 5:
                actions.append(Action.Tsumo())
        else:
            if self.hand[turn].point(card, self.dora) >= 5 and \
                not self.hand[turn].isDiscarded(card):
                actions.append(Action.Ron())
            else: actions.append(Action.Pass())
        return actions

    def getTurn(self):
        return self.turn
        
    # Index of State Array
    # 0 : Deck
    # 1 : Dora
    # 2 : Draw
    # 3 ~ N + 2 : Hand
    # N + 3 ~ 2N + 2 : Discard

    def toArray(self):
        state = np.zeros(Type.NUM_OF_CARD, dtype=int)

        state[self.dora] = 1
        state[self.draw] = 2
        for i in range(Type.N_PLAYER):
            state += (self.hand[i]._hand == 1).astype('int') * (i + 3)
            state += (self.hand[i]._hand == 2).astype('int') * (i + 3 + Type.N_PLAYER)

        return state

    def __str__(self):
        string = 'State(\n\tturn: ' + str(self.turn) + \
                '\n\tdora: ' + str(self.dora)

        string += '\n\thand: ['
        for hand in self.hand:
            string += '\n\t\t' + str(hand)
        string += '\n\t\t]'

        string += '\n\tdiscard: ['
        for discard in self.discard:
            string += '\n\t\t' + str(discard)
        string += '\n\t\t]\n)'

        return string

class Board:
    def __init__(self, players, collector=None, start_turn=0):
        deck = list(range(Type.NUM_OF_CARD))
        random.shuffle(deck)
        self.players = players
        self.state, self.deck = State.init(deck, start_turn)
        self.collector = collector
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
            actions = [Action.Pass() for _ in range(n_player)]
            actions[turn] = self.players[turn].select_action(self.state, draw, turn)

            if not actions[turn].isTsumo():
                discard = actions[turn].Encode()
                for ron_turn in range(turn + 1, turn + 4):
                    ron_turn %= n_player
                    actions[ron_turn] = self.players[ron_turn].select_action(self.state, discard, ron_turn)
                    if actions[ron_turn].isRon(): winner.append(ron_turn)
            else: winner.append(turn)

            if self.collector is not None:
                self.collector.record_episode(self.state, actions)

            next_state = self.state.apply(draw, actions)
            if id(next_state) == id(self.state): break
            self.state = next_state

        for w in winner:
            if actions[w].isTsumo():
                card = self.state.draw
                dora = self.state.dora
                point = self.state.hand[w].point(card, dora)
                point += 2 if w == self.start_turn else 0
                point //= n_player - 1
                result = -point * np.ones(n_player, dtype='int')
                result[w] = point * (n_player - 1)
            else:
                card = actions[turn].Encode()
                dora = self.state.dora
                point = self.state.hand[w].point(card, dora)
                point += 2 if w == self.start_turn else 0
                result[w] += point
                result[turn] -= point

        for dest, src in zip(self.point, result):
            dest += src

        if self.collector is not None:
            self.collector.complete_sub_episode(result)

    def rank(self):
        ranking = np.array(self.point).argsort()
        result = np.zeros(len(self.players))
        result[0] == -10
        result[-1] == 10
        
        if self.collector is not None:
            self.collector.complete_episode(result[ranking])
        