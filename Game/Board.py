from .Card import CardTable, NUM_OF_CARD
from .Hand import Hand, DiscardZone
import random

table = CardTable()

class Action:
    _tsumo = 45
    _ron = 46
    _pass = 47
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
    def __init__(self, n_player, turn, dora, hand, discard):
        self.n_player = n_player
        self.turn = turn
        self.dora = dora
        self.hand = hand
        self.discard = discard
        self.draw = None

    @staticmethod
    def init(n_player, deck):
        hand = []
        discard = [DiscardZone() for i in range(n_player)]
        for i in range(n_player):
            hand.append(Hand(deck[i*5:(i + 1)*5]))
        return (
            State(n_player, 0, deck[n_player*5], hand, discard),
            deck[n_player*5 + 1:])

    def apply(self, draw, actions):
        self.draw = draw
        for action in actions:
            if action.isTsumo() or action.isRon():
                return None

        from copy import deepcopy
        hand = deepcopy(self.hand)
        discard = deepcopy(self.discard)
        discarded_card = actions[self.turn].Encode()
        hand[self.turn].change(draw, discarded_card)
        discard[self.turn].collect(discarded_card)
        return State(
            self.n_player,
            (self.turn + 1) % self.n_player,
            self.dora,
            hand, 
            discard)

    def action(self, turn, card):
        actions = []
        if turn == self.turn:
            for c in self.hand[turn].toArray():
                actions.append(Action.Discard(c))
            if self.hand[turn].point(card, self.dora) >= 5:
                actions.append(Action.Tsumo())
        else:
            if self.hand[turn].point(card, self.dora) >= 5:
                actions.append(Action.Ron())
            else: actions.append(Action.Pass())
        return actions

    def getTurn(self):
        return self.turn

    def __str__(self):
        string = 'State(\n\tn_players: ' + str(self.n_player) + \
                '\n\tturn: ' + str(self.turn) + \
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
    def __init__(self, players, collector=None):
        deck = list(range(NUM_OF_CARD))
        random.shuffle(deck)
        self.players = players
        self.state, self.deck = State.init(len(players), deck)
        self.collector = collector

    def play(self):
        n_player = len(self.players)
        for draw in self.deck:
            if self.state is None: break
            turn = self.state.getTurn()
            actions = [Action.Pass() for i in range(n_player)]
            actions[turn] = self.players[turn].select_action(self.state, draw, turn)

            if not actions[turn].isTsumo():
                discard = actions[turn].Encode()
                for ron_turn in range(turn + 1, turn + 4):
                    ron_turn %= n_player
                    actions[ron_turn] = self.players[ron_turn].select_action(self.state, discard, ron_turn)

            if self.collector is not None:
                self.collector.collect(self.state, actions, None)

            self.state = self.state.apply(draw, actions)