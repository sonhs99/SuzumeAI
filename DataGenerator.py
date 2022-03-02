from Game import Board, Experience
from Game import agents
from tqdm import trange

import argparse

parser = argparse.ArgumentParser(description='SuzumeAi Data Generator')
parser.add_argument('--iter', '-I', type=int, help='')
parser.add_argument('--agent', '-A', help='')
parser.add_argument('--weight', '-W', help='')


iteration = 100

buffer = Experience.ExperienceBuffer()
players = [
    agents.Random.RandomAgent() for i in range(4)
]
for _ in trange(iteration):
    board = Board.Board(players, buffer)
    board.play()
buffer.save('test.h5')