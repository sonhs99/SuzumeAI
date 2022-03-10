import Game
from Game import agents, encoders, nn
import argparse
import h5py
from tqdm import trange

from Game.Experience import ExperienceBuffer

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data Preprocessing for SuzumeAI')
    parser.add_argument('train', help='Source Experience Data to Convert')
    parser.add_argument('epoch', type=int, help='Destination of Converted Train/Test Data')
    parser.add_argument('save', help='File Name of Trained Agent')
    parser.add_argument('--file', help='Pre-trained Agent file')
    args = parser.parse_args()

    if args.file is None:
        agent = agents.OpenAgent(
            encoders.FivePlaneEncoder(),
            nn.SmallNetwork()
        )
    else: agent = agents.OpenAgent.load(args.file)
    with h5py.File(args.train) as train:
        tsumo_exp = ExperienceBuffer.load(train, 'tsumo')
        ron_exp = ExperienceBuffer.load(train, 'ron')
        agent.train_tsumo(tsumo_exp)
        agent.train_ron(ron_exp)
    
    agent.save(args.save)
