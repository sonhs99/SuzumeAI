import math
import Game
from Game import agents, encoders
from tqdm import trange
import argparse, ray, os, h5py

@ray.remote
class Simulator():
    def __init__(self, agent_file, temperature):
        if agent_file is None:
            self.agent = agents.RandomAgent(encoders.FivePlaneEncoder())
        else:
            with h5py.File(agent_file, 'r') as file:
                agent_obj = agents.selector(file.attrs['agent'])
            self.agent = agent_obj.load(agent_file)
            self.agent.set_temperature(temperature)

    def simulate_game(self, iteration):
        tsumo_collector = [Game.ExperienceCollector() for _ in range(4)]
        ron_collector = [Game.ExperienceCollector() for _ in range(4)]
        players = [self.agent.dup() for _ in range(4)]
        for player, tsumo, ron in zip(players, tsumo_collector, ron_collector):
            player.set_collector(tsumo, ron)
        for _ in trange(iteration):
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
    parser.add_argument('--agent-file', help='File Name of Agent')
    parser.add_argument('--temperature', type=float,
                        default=0.0, help='Epsilon Value of e-greedy Policy')
    parser.add_argument('--n-workers', type=int,
                        default=os.cpu_count(), help='Number of Workers')
    args = parser.parse_args()

    iter_per_worker = math.ceil(args.iter / args.n_workers)
    ray.init(num_cpus=args.n_workers)

    workers = [
        Simulator.remote(args.agent_file, args.temperature) \
            for _ in range(args.n_workers)
    ]
    collectors = ray.get([
        w.simulate_game.remote(iter_per_worker) for w in workers
    ])
    tsumo_collector, ron_collector = [], []
    for collector in collectors:
        tsumo_collector += collector[0]
        ron_collector += collector[1]

    tsumo_buffer = Game.combine_experience(tsumo_collector)
    ron_buffer = Game.combine_experience(ron_collector)
    with h5py.File(args.file, 'w') as h5file:
        tsumo_buffer.serialize(h5file, 'tsumo')
        ron_buffer.serialize(h5file, 'ron')
