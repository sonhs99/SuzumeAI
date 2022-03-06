from .. import Type, Card
import numpy as np

table = Card.CardTable()

class FivePlaneEncoder:
    def encode(self, state, turn):
        onehot = np.zeros((5, Type.N_PLAYER, Type.NUM_OF_CARD))
        dora = 0, 0
        for card, s in enumerate(state):
            if s == 1: dora = card
            elif s == 2: onehot[0, turn, card] = 1
            elif s >= 3:
                idx = s - 3
                onehot[idx//2, idx % 2, card] = 1

        onehot[2, turn, :].fill(1)
        
        dora = table.get(dora).num
        for card in range(Type.NUM_OF_CARD):
            if table.get(card).red:
                onehot[3, :, card].fill(1)
            if table.get(card) == dora:
                onehot[4, :, card].fill(1)

        return onehot

    def size(self):
        return (5, Type.N_PLAYER, Type.NUM_OF_CARD)
        
    @staticmethod
    def name():
        return 'five'
