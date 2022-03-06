import numpy as np
import tensorflow as tf
from .. import Type

class SmallNetwork():
    def tsumo(self, input_dim):
        input1 = tf.keras.layers.Input(shape=input_dim, name='input_state')
        input2 = tf.keras.layers.Input(shape=(Type.NUM_OF_CARD + 1,), name='input_action')
        x1 = tf.keras.layers.Conv2D(16,
                                    kernel_size=(Type.N_PLAYER, 1), 
                                    strides=(Type.N_PLAYER, 1), 
                                    activation='relu'
                                    )(input1)
        x1 = tf.keras.layers.Conv2D(16,
                                    kernel_size=(1, Type.NUM_OF_SET),
                                    strides=(1, Type.NUM_OF_SET),
                                    activation='relu'
                                    )(x1)
        x2 = tf.keras.layers.Conv2D(16,
                                    kernel_size=(1, Type.NUM_OF_SET),
                                    strides=(1, Type.NUM_OF_SET),
                                    activation='relu'
                                    )(input1)
        x2 = tf.keras.layers.Conv2D(16,
                                    kernel_size=(Type.N_PLAYER, 1),
                                    strides=(Type.N_PLAYER, 1),
                                    activation='relu'
                                    )(x2)
        x3 = tf.keras.layers.Dense(256, activation='relu')(input2)
        x3 = tf.keras.layers.Dense(Type.NUM_OF_TYPE, activation='relu')(x3)
        x3 = tf.keras.layers.Reshape((1, 1, Type.NUM_OF_TYPE))(x3)
        x = tf.keras.layers.Concatenate()([x1, x2, x3])
        x = tf.keras.layers.Flatten()(x)
        x = tf.keras.layers.Dense(256, activation='relu')(x)
        x = tf.keras.layers.Dense(256, activation='relu')(x)
        output = tf.keras.layers.Dense(1, activation='linear')(x)
        model = tf.keras.Model(inputs=[input1, input2], outputs=output)
        model.summary()
        return model
    
    def ron(self, input_dim):
        None

    def name(self):
        return 'small'
