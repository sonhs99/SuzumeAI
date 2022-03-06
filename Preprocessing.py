import Game
from Game import encoders
from tqdm import tqdm
import argparse
import h5py
import numpy as np

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data Preprocessing for SuzumeAI')
    parser.add_argument('src', help='Source Experience Data to Convert')
    parser.add_argument('dest', help='Destination of Converted Train/Test Data')
    args = parser.parse_args()

    encoder = encoders.FivePlaneEncoder()
    with h5py.File(args.src, 'r') as src:
        states = src['experience']['State']
        actions = src['experience']['Action']
        rewards = src['experience']['Reward']

        tsumo_state, ron_state = [], []
        tsumo_action, ron_action = [], []
        tsumo_y, ron_y = [], []

        template = np.eye(Game.NUM_OF_CARD + 1)

        for state, action, reward in tqdm(zip(states, actions, rewards)):
            turn = (action <= Game.NUM_OF_CARD).argmax()
            for player in range(Game.N_PLAYER):
                encoded_state = encoder.encode(state, turn)
                if player == turn:
                    tsumo_state.append(encoded_state)
                    tsumo_action.append(template[action[player]])
                    tsumo_y.append([reward[player]])
                else:
                    pass

    with h5py.File(args.dest, 'w') as dest:
        dest.create_group('tsumo')
        dest['tsumo'].create_dataset('state', data=np.array(tsumo_state))
        dest['tsumo'].create_dataset('action', data=np.array(tsumo_action))
        dest['tsumo'].create_dataset('y', data=np.array(tsumo_y))
