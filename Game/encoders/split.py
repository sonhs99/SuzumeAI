from .base import Encoder
from .. import Type, Card
import numpy as np

table = Card.CardTable()

class SplitEncoder(Encoder):
    def encode(self, state, idx):
        onehot = np.zeros(self.size())
        dora = (state == 1).argmax()
        target = (state == 2).argmax()
        for p in range(Type.N_PLAYER):
            draw = (state == (3 + 2*p)).reshape((4, 11), dtype=float)
            discard = (state == (4 + 2*p)).reshape((4, 11), dtype=float)
            onehot[:, :, 2&p + 1] = np.tile(draw[3, :], reps=[1, Type.NUM_OF_SET])
            onehot[:, :, 2*p + 3] = np.tile(discard[3, :], reps=[1, Type.NUM_OF_SET])
            # purification need
            onehot[:, :, 2*p] = draw
            onehot[:, :, 2*p + 2] = discard

        onehot[:, table[target].num, 16].fill(1)
        onehot[:, table[dora].num, 17].fill(1)

        return onehot

    def size(self):
        return (Type.NUM_OF_SET, Type.NUM_OF_TYPE, Type.N_PLAYER*4 + 2)

    @staticmethod
    def name():
        return 'split'
