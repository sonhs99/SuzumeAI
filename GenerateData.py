import random
from Game import Board, Experience
from Game.agents import Random
from tqdm import trange
import h5py

iteration = 100

print(f'=== Generate {iteration} Data Test ===')

buffer = Experience.ExperienceBuffer()
players = [
    Random.RandomAgent() for i in range(4)
]
for _ in trange(iteration):
    board = Board.Board(players, buffer)
    board.play()
buffer.save('test.h5')

file = h5py.File('test.h5')

sample = random.randint(0, file['State'].shape[0])
print('sample:', sample)
print('size:', file['State'].shape)
print('state:', file['State'][sample])
print('action:', file['Action'][sample])
print('reward:', file['Reward'][sample])
print('player:', file['n_player'][sample])