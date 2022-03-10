from .base import Encoder
from .. import Type, Card
import numpy as np

table = Card.CardTable()

class FivePlaneEncoder(Encoder):
    ## Plane
    ## 0: Hand
    ## 1: Discard
    ## 2: Turn
    ## 3: Red
    ## 4: Dora
    def encode(self, state, idx):
        onehot = np.zeros((Type.N_PLAYER, Type.NUM_OF_CARD, 5))
        dora = 0
        for card, s in enumerate(state):
            if s == 1: dora = card
            elif s == 2:
                if idx == 0: onehot[idx, card, 0] = 1
                else: onehot[idx, card, 1] = 1
            elif s >= 3:
                idx = s - 3
                onehot[idx % Type.N_PLAYER, card, idx // Type.N_PLAYER] = 1

        onehot[idx, :, 2].fill(1)
        
        dora = table.get(dora).num
        for card in range(Type.NUM_OF_CARD):
            if table.get(card).red:
                onehot[:, card, 3].fill(1)
            if table.get(card) == dora:
                onehot[:, card, 4].fill(1)

        return onehot

    def size(self):
        return (Type.N_PLAYER, Type.NUM_OF_CARD, 5)
        
    @staticmethod
    def name():
        return 'five'
