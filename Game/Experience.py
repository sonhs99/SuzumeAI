from . import Board
import numpy as np

class ExperienceBuffer:
    def __init__(self):
        self.state = []
        self.action = []
        self.reward = []

    def collect(self, state, action, reward):
        self.state.append(state)
        self.action.append(action)
        self.reward.append(reward)

    def get(self, idx):
        return (self.state[idx], self.action[idx], self.reward[idx])

    def len(self):
        return len(self.state)
