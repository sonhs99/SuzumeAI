from . import Score
from .Card import NUM_OF_CARD, CardTable
import numpy as np

table = CardTable()

class Hand:
    def __init__(self, hand):
        self._hand = np.zeros(NUM_OF_CARD, dtype='int')
        for card in hand:
            self._hand[card] = 1

    def point(self, draw, dora):
        self._hand[draw] = True
        hand = self.toArray()
        self._hand[draw] = False
        index = Score.split(hand)
        triple = Score.count_triple(hand[index[0]], dora), \
            Score.count_triple(hand[index[1]], dora)
        if triple[0].type * triple[1].type == 0: return 0
        point = triple[0].type + triple[1].type
        
        if triple[0].red + triple[1].red == 6:
            return point + 20
        if triple[0].green + triple[1].green == 6:
            return point + 10
        if triple[0].noble and triple[1].noble:
            if triple[0].type == 2 and triple[1].type == 2:
                return point + 15
            else: point += 2
        elif not (triple[0].noble or triple[1].noble):
            point += 1
        
        point += triple[0].red + triple[1].red
        point += triple[0].dora + triple[1].dora
        return point

    def change(self, draw, discard):
        self._hand[draw] = 1
        self._hand[discard] = 2

    def toArray(self):
        return np.arange(44)[self._hand == 1]

    def __str__(self):
        return f'Hand({self.toArray()})'

class DiscardZone:
    def __init__(self):
        self._discard = []

    def collect(self, card):
        self._discard.append(card)

    def isDiscarded(self, card):
        cards = table.getid(table.get(card).num)
        for c in cards:
            if c in self._discard: return True
        return False

    def toArray(self):
        return self._discard

    def __str__(self):
        return f'Hand({self._discard})'