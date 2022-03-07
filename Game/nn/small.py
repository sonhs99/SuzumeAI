import numpy as np
import tensorflow as tf
from .. import Type

class SmallNetwork():
    def tsumo(self, input_dim):
        input_state = tf.keras.layers.Input(shape=input_dim, name='input_state')
        input_action = tf.keras.layers.Input(shape=(Type.NUM_OF_CARD + 1,), name='input_action')
        x1 = tf.keras.layers.Conv2D(16,
                                    kernel_size=(Type.N_PLAYER, Type.NUM_OF_SET), 
                                    strides=(Type.N_PLAYER, Type.NUM_OF_SET),
                                    padding='valid',
                                    activation='relu'
                                    )(input_state)
        x1 = tf.keras.layers.Conv2D(16,
                                    kernel_size=(1, 3),
                                    padding='valid',
                                    activation='relu'
                                    )(x1)
        x2 = tf.keras.layers.Dense(256, activation='relu')(input_action)
        x2 = tf.keras.layers.Dense(Type.NUM_OF_TYPE - 2, activation='relu')(x2)
        x2 = tf.keras.layers.Reshape((1, Type.NUM_OF_TYPE - 2, 1))(x2)
        x = tf.keras.layers.Concatenate()([x1, x2])
        x = tf.keras.layers.Flatten()(x)
        x = tf.keras.layers.Dense(256, activation='relu')(x)
        x = tf.keras.layers.Dense(256, activation='relu')(x)
        output = tf.keras.layers.Dense(1, activation='linear')(x)
        model = tf.keras.Model(inputs=[input_state, input_action], outputs=output)
        model.summary()
        return model
    
    def ron(self, input_dim):
        None

    def name(self):
        return 'small'
