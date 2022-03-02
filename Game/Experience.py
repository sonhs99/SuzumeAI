from . import Type
import numpy as np
import h5py

class ExperienceCollector:
    def __init__(self):
        self.state = []
        self.action = []
        self.reward = []
        self.episode_state = []
        self.episode_action = []

    def record_episode(self, state, action):
        self.episode_state.append(state)
        self.episode_action.append(action)

    def complete_episode(self, reward):
        self.state += self.episode_state
        self.action += self.episode_action
        self.reward += [reward] * len(self.episode_state)

        self.episode_state = []
        self.episode_action = []


    def get(self, idx):
        return (self.state[idx], self.action[idx], self.reward[idx])

    def len(self):
        return len(self.state)

class ExperienceBuffer:
    def __init__(self, state, action, reward):
        self.state = state
        self.action = action
        self.reward = reward

    def serialize(self, file_name):
        file = h5py.File(file_name, 'w')
        file.create_group('experience')
        file['experience'].create_dataset('State', data=self.state)
        file['experience'].create_dataset('Action', data=self.action)
        file['experience'].create_dataset('Reward', data=self.reward)

def combine_experience(collectors):
    states = np.concatenate([
        np.array([state.toArray() for state in c.state]) for c in collectors
    ])
    actions = np.concatenate([
        [np.array([action.Encode() for action in actions])
            for actions in c.action] for c in collectors
    ])
    rewards = np.concatenate([np.array(c.reward) for c in collectors])

    return ExperienceBuffer(
        states,
        actions,
        rewards
    )
