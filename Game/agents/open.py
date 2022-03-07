from .. import Action, NUM_OF_CARD
from .. import encoders, nn
import numpy as np
import h5py

class OpenAgent:
    def __init__(self, encoder, network):
        self.encoder = encoder
        self.network = network

        self.nn_tsumo = network.tsumo(encoder.size())
        self.nn_ron = network.ron(encoder.size())

    def select_action(self, state, card, turn):
        actions = state.action(turn, card)
        if Action.Ron() in actions:
            return Action.Ron()
        if Action.Pass() in actions:
            return Action.Pass()
        state_array = state.toArray()
        encoded_state = self.encoder.encode(state_array, turn)
        action = np.array([action.encode() for action in actions])
        encoded_action = np.eye(NUM_OF_CARD + 1)[action]
        result = self.nn_tsumo.predict([encoded_state, encoded_action])
        return actions[result.argmax()]

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
                file['model/tsumo'].create_dataset(f'level {idx}', data=layer)

            file.attrs['encoder'] = self.encoder.name()
            file.attrs['network'] = self.network.name()

    @staticmethod
    def load(filename):
        with h5py.File(filename, 'r') as file:
            encoder = encoders.selector(file.attrs['encoder'])
            network = nn.selector(file.attrs['network'])
            agent = OpenAgent(encoder, network)

            tsumo_layers = [
                file['model/tsumo'][f'level {idx}'] for idx in range(file['model/tsumo'].attrs['len'])
            ]
            agent.nn_tsumo.set_weights(tsumo_layers)
        return agent
