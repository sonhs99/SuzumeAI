from Game import Board, Experience
from Game.agents import Random
from tqdm import tqdm
import argparse
import ray
import os

@ray.remote
def generate_data():
    collector = Experience.ExperienceCollector()
    players = [
        Random.RandomAgent() for i in range(4)
    ]
    board = Board.Board(players, collector)
    board.play()
    return collector

if __name__ == '__main__':
    ray.init(num_cpus=os.cpu_count())

    parser = argparse.ArgumentParser(description='Data Generator for SuzumeAI')
    parser.add_argument('iter', type=int, help='Iteration Count')
    parser.add_argument('file', help='File Name to Save Data')
    args = parser.parse_args()

    result_ids = [generate_data.remote() for i in range(args.iter)]
    collector = []
    with tqdm(total=args.iter) as pbar:
        while len(result_ids):
            done_id, result_ids = ray.wait(result_ids)
            pbar.update(len(done_id))
            collector.append(ray.get(done_id[0]))
    
    buffer = Experience.combine_experience(collector)
    buffer.serialize(args.file)
