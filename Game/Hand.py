from . import Score, Type
from .Card import CardTable
import numpy as np

table = CardTable()

class Hand:
    def __init__(self, hand):
        self._hand = np.zeros(Type.NUM_OF_CARD, dtype='int')
        for card in hand:
            self._hand[card] = 1

    def point(self, draw, dora):
        assert not self._hand[draw] == 1
        self._hand[draw] = 1
        hand = self.to_array()
        self._hand[draw] = 0
        index = Score.split(hand)
        triple = Score.count_triple(hand[index[0]], dora), \
            Score.count_triple(hand[index[1]], dora)
        points = np.sum([
            condition(triple[0], triple[1]) for condition in Score.point_condition
        ], axis=0)
        # print(points)
        return (points[0] + (points[1] if points[1] != 0 else points[2])) \
            if points[0] != 0 else 0

    def change(self, draw, discard):
        self._hand[draw] = 1
        self._hand[discard] = 2

    def to_array(self):
        return np.arange(44)[self._hand == 1]

    def isDiscarded(self, card):
        cards = table.getid(table[card].num)
        for c in cards:
            if self._hand[c] == 2:
                True
        return False

    def __str__(self):
        return f'Hand({self.to_array()})'

class DiscardZone:
    def __init__(self):
        self._discard = []

    def collect(self, card):
        self._discard.append(card)

    def to_array(self):
        return self._discard

    def __str__(self):
        return f'DiscardZone({self._discard})'