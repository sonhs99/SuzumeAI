from .base import Agent
from .. import Action, NUM_OF_CARD
from .. import encoders, nn
import numpy as np
import random
import h5py

class OpenAgent(Agent):
    def __init__(self, encoder, network):
        self.encoder = encoder
        self.network = network

        self.nn_tsumo = network.network(encoder.size(), NUM_OF_CARD + 1)
        self.nn_ron = network.network(encoder.size(), 1)

    def select_tsumo(self, state, draw):
        actions = state.legal_tsumo_action(draw)
        state_array = state.array()
        encoded_state = np.array([self.encoder.encode(state_array)] * len(actions))
        action = np.array([action.encode() for action in actions])
        encoded_action = np.eye(NUM_OF_CARD + 1)[action]
        result = self.nn_tsumo.predict([encoded_state, encoded_action])
        selection = actions[result.argmax()]
        if self._tsumo_collector is not None:
            self._tsumo_collector.record_episode(
                state_array, selection.Encode())
        return actions[result.argmax()]

    def select_ron(self, state, discard, turn):
        ron_able = state.legal_ron_action(turn, discard)
        if ron_able:
            state_array = state.to_array()
            encoded_state = np.array([self.encoder.encode(state_array, turn)] * 2)
            action = np.array([[0], [1]])
            result = self.nn_tsumo.predict([encoded_state, action])
            if self._ron_collector is not None:
                self._ron_collector.record_episode(
                    state_array, result[1] > result[0])
            if result[1] > result[0]:
                selection = Action.Ron()
            else: selection = Action.Pass()
            return selection
        else: return Action.Pass()

    def train_tsumo(self, X, y):
        self.nn_tsumo.compile(
            optimizer='adam',
            loss='mse'
        )
        return self.nn_tsumo.train_on_batch(X, y)

    def save(self, file_name):
        tsumo_weights = self.nn_tsumo.get_weights()

        with h5py.File(file_name, 'w') as file:
            file.create_group('model')

            file['model'].create_group('tsumo')
            file['model/tsumo'].attrs['len'] = len(tsumo_weights)
            for idx, layer in enumerate(tsumo_weights):
                file['model/tsumo'].create_dataset(str(idx), data=layer)

            file['model'].create_group('ron')
            file['model/ron'].attrs['len'] = len(tsumo_weights)
            for idx, layer in enumerate(tsumo_weights):
                file['model/ron'].create_dataset(str(idx), data=layer)

            file.attrs['encoder'] = self.encoder.name()
            file.attrs['network'] = self.network.name()
            file.attrs['agent'] = self.name()

    @staticmethod
    def load(filename):
        with h5py.File(filename, 'r') as file:
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

    @staticmethod
    def name():
        return 'open'