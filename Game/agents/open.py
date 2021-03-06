from .base import Agent
from .. import Action, Type
from .. import encoders, nn
import numpy as np
import tensorflow as tf
import random, h5py

class OpenAgent(Agent):
    def __init__(self, encoder, network=None):
        self.encoder = encoder
        self.network = network

        self.nn_tsumo = network.network(encoder.size(), Type.NUM_OF_CARD + 1) \
            if network is not None else None
        self.nn_ron = network.network(encoder.size(), 2) \
            if network is not None else None

        self.temperature = 0

    def set_temperature(self, temperature):
        self.temperature = temperature

    def select_tsumo(self, state, draw):
        actions = state.legal_tsumo_action(draw)
        if random.uniform(0, 1) > self.temperature:
            mask = np.zeros(Type.NUM_OF_CARD + 1)
            for a in actions: mask[a.encode()] = 1
            state_array = state.to_array()
            encoded_state = self.encoder.encode(state_array, 0)
            policy, value = self.nn_tsumo.predict(encoded_state[np.newaxis, :])
            selection = Action((policy[0]*mask).argmax())
            estimate = value[0][0]
        else:
            selection = random.choice(actions)
            estimate = 0
            
        if self._tsumo_collector is not None:
            self._tsumo_collector.record_episode(
                encoded_state, selection.encode(), estimate)
        return selection

    def select_ron(self, state, discard, turn):
        ron_able = state.legal_ron_action(turn, discard)
        if ron_able:
            state_array = state.to_array()
            encoded_state = np.array([self.encoder.encode(state_array, turn)] * 2)
            if random.uniform(0, 1) > self.temperature:
                policy, value = self.nn_ron.predict(encoded_state[np.newaxis, :])
                if policy[0][0] > policy[0][1]:
                    selection = Action.Ron()
                else: selection = Action.Pass()
                estimate = value[0][0]
            else: 
                selection = random.choice([Action.ron(), Action.Pass()])
                estimate = 0

            if self._ron_collector is not None:
                self._ron_collector.record_episode(
                    encoded_state[0], selection.isRon(), estimate)

        else: selection = Action.Pass()
        return selection

    def train_tsumo(self, experience, lr=0.1, batch_size=128):
        self.nn_tsumo.compile(
            optimizer=tf.optimizers.SGD(learning_rate=lr),
            loss=['categorical_crossentropy', 'mse'],
            loss_weight=[1, 0.5]
        )

        n = experience.state.shape[0]
        policy_target = np.zeros((n, Type.NUM_OF_TYPE))
        value_target = np.zeros((n,))
        for i in range(n):
            policy_target[i, experience.action[i]] = experience.advantage[i]
            value_target[i] = experience.reward[i]

        return self.nn_tsumo.fit(
            experience.state,
            [policy_target, value_target],
            batch_size=batch_size,
            epochs=1, shuffle=False)

    def train_ron(self, experience, lr=0.1, batch_size=128):
        self.nn_ron.compile(
            optimizer=tf.optimizers.SGD(learning_rate=lr),
            loss=['categorical_crossentropy', 'mse'],
            loss_weight=[1, 0.5]
        )
        
        n = experience.state.shape[0]
        policy_target = np.zeros((n, Type.NUM_OF_TYPE))
        value_target = np.zeros((n,))
        for i in range(n):
            policy_target[i, experience.action[i]] = experience.advantage[i]
            value_target[i] = experience.reward[i]

        return self.nn_ron.fit(
            experience.state,
            [policy_target, value_target],
            batch_size=batch_size,
            epochs=1, shuffle=False)

    def save(self, file_name):
        tsumo_weights = self.nn_tsumo.get_weights()
        ron_weights = self.nn_ron.get_weights()

        with h5py.File(file_name, 'w') as file:
            file.create_group('model')

            file['model'].create_group('tsumo')
            file['model/tsumo'].attrs['len'] = len(tsumo_weights)
            for idx, layer in enumerate(tsumo_weights):
                file['model/tsumo'].create_dataset(str(idx), data=layer)

            file['model'].create_group('ron')
            file['model/ron'].attrs['len'] = len(ron_weights)
            for idx, layer in enumerate(ron_weights):
                file['model/ron'].create_dataset(str(idx), data=layer)

            file.attrs['encoder'] = self.encoder.name()
            file.attrs['network'] = self.network.name()
            file.attrs['agent'] = self.name()

    @staticmethod
    def load(file):
        encoder = encoders.selector(file.attrs['encoder'])
        network = nn.selector(file.attrs['network'])
        agent = OpenAgent(encoder, network)

        tsumo_layers = [
            file['model/tsumo'][str(idx)] for idx in range(file['model/tsumo'].attrs['len'])
        ]
        agent.nn_tsumo.set_weights(tsumo_layers)

        ron_layers = [
            file['model/ron'][str(idx)] for idx in range(file['model/ron'].attrs['len'])
        ]
        agent.nn_ron.set_weights(ron_layers)
        return agent

    def dup(self):
        dup_agent = OpenAgent(self.encoder)
        dup_agent.network = self.network
        dup_agent.nn_tsumo = self.nn_tsumo
        dup_agent.nn_ron = self.nn_ron
        return dup_agent

    @staticmethod
    def name():
        return 'open'