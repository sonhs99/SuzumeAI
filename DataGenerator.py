import Game
from Game import agents
from tqdm import tqdm
import argparse
import ray
import os
import h5py

@ray.remote
def generate_data():
    tsumo_collector = [Game.ExperienceCollector() for _ in range(4)]
    ron_collector = [Game.ExperienceCollector() for _ in range(4)]
    players = [agents.RandomAgent() for _ in range(4)]
    for player, tsumo, ron in zip(players, tsumo_collector, ron_collector):
        player.set_collector(tsumo, ron)
    board = Game.Board(players,
                        tsumo_collector=tsumo_collector,
                        ron_collector=ron_collector)
    for _ in range(len(players)):
        board.play()
        board.prepare()
    board.rank()
    return tsumo_collector, ron_collector

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data Generator for SuzumeAI')
    parser.add_argument('iter', type=int, help='Iteration Count')
    parser.add_argument('file', help='File Name to Save Data')
    args = parser.parse_args()

    ray.init(num_cpus=os.cpu_count())

    result_ids = [generate_data.remote() for i in range(args.iter)]
    tsumo_collector, ron_collector = [], []
    with tqdm(total=args.iter) as pbar:
        while len(result_ids):
            done_id, result_ids = ray.wait(result_ids)
            pbar.update(len(done_id))
            collectors = ray.get(done_id)
            for collector in collectors:
                tsumo_collector += collector[0]
                ron_collector += collector[1]

    tsumo_buffer = Game.combine_experience(tsumo_collector)
    ron_buffer = Game.combine_experience(ron_collector)
    with h5py.File(args.file, 'w') as h5file:
        tsumo_buffer.serialize(h5file, 'tsumo')
        ron_buffer.serialize(h5file, 'ron')
