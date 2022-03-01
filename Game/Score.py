from .Card import CardTable, RED, GREEN
from collections import namedtuple
import numpy as np

table = CardTable()
info = namedtuple('TripleInfo', 'type red green dora noble')

def count_triple(triple, dora):
    card = [table.get(c) for c in triple]
    dora = table.get(dora).num
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
    delta = np.zeros(6)
    index = [0, 1, 2, 3, 4, 5]
    for idx in range(1, 6):
        delta[idx] = table.get(hand[idx]).num - table.get(hand[idx - 1]).num
    for i in range(3):
        if (delta[index[:3]] >= 2).any():
            break # Not Ready
        elif delta[index[:3]].sum() == 2 or delta[:3].sum() == 0:
            break # Body Recognized
        else:  # Possibility of Existance of Body
            swap_idx = 1 if delta[index[1]] == 0 else 2
            index[swap_idx], index[3 + i] = index[3 + i], index[swap_idx]
    return sorted(index[:3]), sorted(index[3:])

    