import Game
from Game import encoders, Log, Hand
from tqdm import tqdm
import argparse, h5py, os, ray

@ray.remote
class Simulator():
    def __init__(self, encoder, n_player):
        self.encoder = encoder
        self.n_player = n_player

    def simulate_game(self, games):
        tsumo_collector = [Game.ExperienceCollector() for _ in range(self.n_player)]
        ron_collector = [Game.ExperienceCollector() for _ in range(self.n_player)]
        state = None
        for game in tqdm(games):
            for action in game:
                if isinstance(action, Log.InitState):
                    state = Game.State(
                        action.start_player,
                        action.dora,
                        [Hand.Hand(hand) for hand in action.init_hand])

                elif isinstance(action, Log.Turn):
                    turn = state.get_turn()
                    tsumo = Game.Action(action.tsumo)
                    ron = [Game.Action.Pass() for _ in range(self.n_player - 1)]
                    for w in action.ron:
                        ron[(w-turn-1+self.n_player) % self.n_player] = Game.Action.Ron()
                    state.set_draw(action.draw)
                    tsumo_collector[turn].record_episode(
                        self.encoder.encode(state.to_array(), 0), 
                        action.tsumo)
                    if not tsumo.isTsumo():
                        discard = action.tsumo
                        for idx in range(self.n_player - 1):
                            ron_turn = (idx+turn+1) % self.n_player
                            if state.legal_ron_action(idx, discard):
                                ron_collector[ron_turn].record_episode(
                                    self.encoder.encode(state.to_array(discard), idx),
                                    ron[idx].isRon()
                                )
                    state = state.apply_action(tsumo, ron)
                        
                elif isinstance(action, Log.Result):
                    for t_c, r_c, r in zip(tsumo_collector, ron_collector, action.result):
                        t_c.complete_sub_episode(r)
                        r_c.complete_sub_episode(r)

                elif isinstance(action, Log.Uma):
                    for t_c, r_c, r in zip(tsumo_collector, ron_collector, action.rank):
                        t_c.complete_episode(r)
                        r_c.complete_episode(r)
        return tsumo_collector, ron_collector

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data Preprocessing for SuzumeAI')
    parser.add_argument('src', help='Source Experience Data to Convert')
    parser.add_argument('dest', help='Destination of Converted Train/Test Data')
    parser.add_argument('--network', help='Network file')
    parser.add_argument('--n-workers', type=int,
                        default=os.cpu_count(), help='Number of Workers')
    args = parser.parse_args()

    ray.init(num_cpus=args.n_workers)

    encoder = ray.put(encoders.FivePlaneEncoder())
    log = Log.Logger.load_log(args.src)
    games = log.construct_game()
    game_per_worker = len(games) // args.n_workers
    games = [
        ray.put(games[game_per_worker*idx:game_per_worker*(idx+1)])
        for idx in range(args.n_workers)
    ]

    workers = [
        Simulator.remote(encoder, log.n_player) for _ in range(args.n_workers)
    ]
    collectors = ray.get([
        w.simulate_game.remote(games[idx]) for idx, w in enumerate(workers)
    ])

    tsumo_collector, ron_collector = [], []
    for collector in collectors:
        tsumo_collector += collector[0]
        ron_collector += collector[1]

    tsumo_buffer = Game.combine_experience(tsumo_collector)
    ron_buffer = Game.combine_experience(ron_collector)
    with h5py.File(args.dest, 'w') as h5file:
        tsumo_buffer.serialize(h5file, 'tsumo')
        ron_buffer.serialize(h5file, 'ron')