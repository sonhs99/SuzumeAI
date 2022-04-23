from .base import Encoder
from .. import Type, Card
import numpy as np

table = Card.CardTable()

class FivePlaneEncoder(Encoder):
    ## Plane
    ## 0: Hand
    ## 1: Draw/Discard
    ## 2: Turn
    ## 3: Red
    ## 4: Dora
    def encode(self, state, index):
        onehot = np.zeros(self.size())
        dora = 0
        for card, s in enumerate(state):
            if s == 1: dora = card
            elif s == 2:
                if index == 0: onehot[index, card, 0] = 1
                else: onehot[index, card, 1] = 1
            elif s >= 3:
                idx = s - 3
                onehot[idx // 2, card, idx % 2] = 1

        onehot[index, :, 2].fill(1)
        
        dora = table[dora].num
        for card in range(Type.NUM_OF_CARD):
            if table[card].red:
                onehot[:, card, 3].fill(1)
            if table[card].num == dora:
                onehot[:, card, 4].fill(1)

        return onehot

    def size(self):
        return (Type.N_PLAYER, Type.NUM_OF_CARD, 5)
        
    @staticmethod
    def name():
        return 'five'
