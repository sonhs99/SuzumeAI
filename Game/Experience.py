import numpy as np
import h5py

__all__ = [
    'ExperienceCollector',
    'ExperienceBuffer',
    'combine_experience'
]

class ExperienceCollector:
    def __init__(self):
        self.state = []
        self.action = []
        self.reward = []
        self.sub_episode_state = []
        self.sub_episode_action = []
        self.episode_state = []
        self.episode_action = []
        self.episode_reward = []

    def record_episode(self, state, action):
        self.sub_episode_state.append(state)
        self.sub_episode_action.append(action)

    def complete_sub_episode(self, reward):
        self.episode_state += self.sub_episode_state
        self.episode_action += self.sub_episode_action
        self.episode_reward += [reward] * len(self.sub_episode_state)

        self.sub_episode_state = []
        self.sub_episode_action = []

    def complete_episode(self, reward):
        self.state += self.episode_state
        self.action += self.episode_action
        self.reward += [reward + r for r in self.episode_reward]

        self.episode_state = []
        self.episode_action = []
        self.episode_reward = []

    def get(self, idx):
        return (self.state[idx], self.action[idx], self.reward[idx])

    def len(self):
        return len(self.state)

class ExperienceBuffer:
    def __init__(self, state, action, reward):
        self.state = state
        self.action = action
        self.reward = reward

    def serialize(self, h5file, group_name):
        h5file.create_group(group_name)
        h5file[group_name].create_dataset('State', data=self.state)
        h5file[group_name].create_dataset('Action', data=self.action)
        h5file[group_name].create_dataset('Reward', data=self.reward)

    @staticmethod
    def load(h5file, group_name):
        return ExperienceBuffer(
            state=h5file[group_name]['state'],
            action=h5file[group_name]['action'],
            reward=h5file[group_name]['reward']
        )

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
