from .Card import CardTable, RED, GREEN
from collections import namedtuple
import numpy as np

__all__ = ['count_triple', 'split', 'point_condition']

table = CardTable()
info = namedtuple('TripleInfo', 'type red green dora noble')

card_index = [
    [[0, 1, 2], [3, 4, 5]],
    [[0, 1, 5], [2, 3, 4]],
    [[0, 2, 4], [1, 3, 5]]
]

point_condition = [
    lambda f, s: np.array([(f.type != 0 and s.type != 0)*(f.type + s.type), 0, 0]),  # Body
    lambda f, s: np.array([0, (f.red + s.red == 6) * 20, 0]), # Super Red
    lambda f, s: np.array([0, (f.green + s.green == 6) * 10, 0]), # All Green
    lambda f, s: np.array([0, (f.type + s.type == 4 and f.noble and s.noble) * 15, 0]), # All Noble
    lambda f, s: np.array([0, 0, f.dora + s.dora + f.red + s.red]), # Dora, Red
    lambda f, s: np.array([0, 0, (not f.noble and not s.noble) * 1]), # All Simple
    lambda f, s: np.array([0, 0, (f.noble and s.noble) * 2]) # Noble in each set
]

def count_triple(triple, dora):
    card = [table[c] for c in triple]
    dora = table[dora].num
    type = 0
    if card[0].num + 1 == card[1].num and \
            card[1].num + 1 == card[2].num:
        if card[2].num != RED and card[2].num != GREEN:
            type = 1 # Sequence Body
    if card[0].num == card[1].num and \
            card[1].num == card[2].num:
        type = 2 # Three Of The Kind Body
    if type == 0: # None
        return info(0, 0, 0, 0, False)

    noble = card[0].noble or card[2].noble
    red, green, dora_count = 0, 0, 0
    for c in card:
        if c.red:
            red += 1
        elif c.green:
            green += 1
        if c.num == dora:
            dora_count += 1

    return info(type, red, green, dora_count, noble)

def split(hand):
    card = [table[c].num for c in hand]
    for triple in card_index:
        # Three of Kind
        if card[triple[0][0]] == card[triple[0][1]] and \
            card[triple[0][1]] == card[triple[0][2]]:
            return triple
        # Sequence
        if card[triple[0][0]] + 1 == card[triple[0][1]] and \
            card[triple[0][1]] + 1 == card[triple[0][2]]:
            if card[triple[0][2]] != RED and card[triple[0][2]] != GREEN:
                return triple
    return card_index[0] # Not Recognize