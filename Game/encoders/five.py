from .. import Type, Card
import numpy as np

table = Card.CardTable()

class FivePlaneEncoder:
    def encode(self, state, turn):
        onehot = np.zeros((Type.N_PLAYER, Type.NUM_OF_CARD, 5))
        dora = 0, 0
        for card, s in enumerate(state):
            if s == 1: dora = card
            elif s == 2: onehot[turn, card, 0] = 1
            elif s >= 3:
                idx = s - 3
                onehot[idx % 2, card, idx//2] = 1

        onehot[turn, :, 2].fill(1)
        
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
