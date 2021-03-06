import numpy as np
import tensorflow as tf

from Game.nn.base import Network
from .. import Type

class SmallNetwork(Network):
    def network(self, state_dim):
        input_state = tf.keras.layers.Input(shape=state_dim, name='input_state')
        x1 = tf.keras.layers.Conv2D(32,
                                    kernel_size=(Type.N_PLAYER, Type.NUM_OF_SET), 
                                    strides=(Type.N_PLAYER, Type.NUM_OF_SET),
                                    padding='valid',
                                    activation='relu'
                                    )(input_state)
        x1 = tf.keras.layers.Conv2D(32,
                                    kernel_size=(1, 3),
                                    padding='same',
                                    activation='relu'
                                    )(x1)

        x = tf.keras.layers.Flatten()(x1)
        pi = tf.keras.layers.Dense(256, activation='relu')(x)
        pi = tf.keras.layers.Dense(256, activation='relu')(pi)
        policy = tf.keras.layers.Dense(Type.NUM_OF_CARD + 1, activation='softmax')(pi)

        v = tf.keras.layers.Dense(256, activation='relu')(x)
        v = tf.keras.layers.Dense(256, activation='relu')(v)
        value = tf.keras.layers.Dense(1, activation='tanh')(v)
        model = tf.keras.Model(inputs=[input_state], outputs=[policy, value])
        
        # model.summary()
        return model

    def name(self):
        return 'small'
