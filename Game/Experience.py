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
        self.advantage = []
        self.sub_episode_state = []
        self.sub_episode_action = []
        self.sub_episode_estimated = []
        self.episode_state = []
        self.episode_action = []
        self.episode_reward = []
        self.episode_estimated = []

    def record_episode(self, state, action, estimate=0):
        self.sub_episode_state.append(state)
        self.sub_episode_action.append(action)
        self.sub_episode_estimated.append(estimate)

    def complete_sub_episode(self, reward):
        self.episode_state += self.sub_episode_state
        self.episode_action += self.sub_episode_action
        self.episode_reward += [reward] * len(self.sub_episode_state)
        self.episode_estimated += self.sub_episode_estimated

        self.sub_episode_state = []
        self.sub_episode_action = []
        self.sub_episode_estimated = []

    def complete_episode(self, reward):
        self.state += self.episode_state
        self.action += self.episode_action
        self.reward += [(reward + r) for r in self.episode_reward]
        self.advantage += [(reward - estimate) for estimate in self.episode_estimated]

        self.episode_state = []
        self.episode_action = []
        self.episode_reward = []
        self.episode_estimated =[]

    def get(self, idx):
        return (self.state[idx], self.action[idx], self.reward[idx], self.episode_estimated[idx])

    def len(self):
        return len(self.state)

class ExperienceBuffer:
    def __init__(self, state, action, reward, advantage):
        self.state = state
        self.action = action
        self.reward = reward
        self.advantage = advantage

    def serialize(self, h5file, group_name):
        h5file.create_group(group_name)
        h5file[group_name].create_dataset('State', data=self.state)
        h5file[group_name].create_dataset('Action', data=self.action)
        h5file[group_name].create_dataset('Reward', data=self.reward)
        h5file[group_name].create_dataset('Advantage', data=self.advantage)

    @staticmethod
    def load(h5file, group_name):
        return ExperienceBuffer(
            state=h5file[group_name]['State'],
            action=h5file[group_name]['Action'],
            reward=h5file[group_name]['Reward'],
            advantage=h5file[group_name]['Advantage']
        )

def combine_experience(collectors):
    states, actions, rewards, advantage = [], [], []
    for collector in collectors:
        states += collector.state
        actions += collector.action
        rewards += collector.reward
        advantage += collector.advantage

    return ExperienceBuffer(
        state=np.array(states),
        action=np.array(actions),
        reward=np.array(rewards),
        advantage=np.array(advantage)
    )
