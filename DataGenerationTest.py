import random
from Game import Board, Experience
from Game.agents import Random
from tqdm import trange
import h5py

iteration = 100

print(f'=== Generate {iteration} Data Test ===')

collector = Experience.ExperienceCollector()
players = [
    Random.RandomAgent() for i in range(4)
]
for _ in trange(iteration):
    board = Board.Board(players, collector)
    board.play()
buffer = Experience.combine_experience([collector])
buffer.serialize('test.h5')

file = h5py.File('test.h5')

sample = random.randint(0, file['experience']['State'].shape[0])
print('sample:', sample)
print('size:', file['experience']['State'].shape)
print('state:', file['experience']['State'][sample])
print('action:', file['experience']['Action'][sample])
print('reward:', file['experience']['Reward'][sample])