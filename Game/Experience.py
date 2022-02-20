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
