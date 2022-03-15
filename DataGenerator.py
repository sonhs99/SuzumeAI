import Game
from Game import agents, encoders
from tqdm import tqdm
import argparse, ray, os, h5py

@ray.remote
def generate_data(agent):
    import tensorflow as tf
    tsumo_collector = [Game.ExperienceCollector() for _ in range(4)]
    ron_collector = [Game.ExperienceCollector() for _ in range(4)]
    players = [agent.dup() for _ in range(4)]
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
    parser.add_argument('--agent-file', help='File Name of Agent')
    parser.add_argument('--temperature', type=float, default=0.0, help='Epsilon Value of e-greedy Policy')
    args = parser.parse_args()

    if args.agent_file is None:
        agent = agents.RandomAgent(encoders.FivePlaneEncoder())
    else:
        with h5py.File(args.agent_file, 'r') as agent_file:
            agent_obj = agents.selector(agent_file.attrs['agent'])
        agent = agent_obj.load(args.agent_file)
        agent.set_temperature(args.temperature)

    ray.init(num_cpus=os.cpu_count())
    agent = ray.put(agent)

    result_ids = [generate_data.remote(agent) for i in range(args.iter)]
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
