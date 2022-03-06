import Game
from Game import agents, encoders, nn
import argparse
import h5py
from tqdm import trange

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data Preprocessing for SuzumeAI')
    parser.add_argument('train', help='Source Experience Data to Convert')
    parser.add_argument('epoch', type=int, help='Destination of Converted Train/Test Data')
    parser.add_argument('save', help='File Name of Trained Agent')
    parser.add_argument('--file', help='Pre-trained Agent file')
    args = parser.parse_args()

    batch_size = 64

    if args.file is None:
        agent = agents.OpenAgent(
            encoders.FivePlaneEncoder(),
            nn.SmallNetwork()
        )
    else: agent = agents.OpenAgent.load(args.file)
    with h5py.File(args.train) as train:
        tsumo_state = train['tsumo']['state']
        tsumo_action = train['tsumo']['action']
        tsumo_y = train['tsumo']['y']

        for i in range(args.epoch):
            pbar = trange(0, len(tsumo_state), batch_size)
            pbar.set_description(f'epoch {i}/{args.epoch}')
            for idx in pbar:
                train_state = tsumo_state[idx:idx + batch_size]
                train_action = tsumo_action[idx:idx + batch_size]
                train_y = tsumo_y[idx:idx + batch_size]
                loss = agent.train_tsumo((train_state, train_action), train_y)
                pbar.set_postfix({
                    'loss':loss
                })
    
    agent.save(args.save)
