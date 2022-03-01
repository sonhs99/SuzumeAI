from . import Board
import numpy as np
import h5py

class ExperienceBuffer:
    def __init__(self):
        self.state = []
        self.action = []
        self.reward = []
        self.episode_state = []
        self.episode_action = []

    def collect(self, state, action):
        self.episode_state.append(state)
        self.episode_action.append(action)

    def end(self, reward):
        self.state += self.episode_state
        self.action += self.episode_action
        self.reward += [reward] * len(self.episode_state)

        self.episode_state = []
        self.episode_action = []

    def get(self, idx):
        return (self.state[idx], self.action[idx], self.reward[idx])

    def len(self):
        return len(self.state)

    # 0 : Deck
    # 1 : Dora
    # 2 : Draw
    # 3 ~ N + 2 : Hand
    # N + 3 ~ 2N + 2 : Discard 

    def save(self, file_name):
        file = h5py.File(file_name, 'w')

        states = np.zeros((len(self.state), 44), dtype='int')
        actions = np.zeros((len(self.state), 4), dtype='int')
        n_player = np.zeros(len(self.state), dtype='int')

        for idx, state in enumerate(self.state):
            n_player[idx] = state.n_player
            states[idx, state.dora] = 1
            states[idx, state.draw] = 2
            for i in range(n_player[idx]):
                states[idx] += (state.hand[i]._hand == 1).astype('int') * (i + 3)
                states[idx] += (state.hand[i]._hand == 2).astype('int') * (i + 3 + n_player[idx])
                actions[idx, i] = self.action[idx][i].Encode()
                
        file.create_dataset('State', data=states)
        file.create_dataset('Action', data=actions)
        file.create_dataset('Reward', data=np.array(self.reward))
        file.create_dataset('n_player', data=n_player)