import numpy as np

class InitState:
    def __init__(self, init_hand, dora, start_player):
        self.init_hand = init_hand
        self.dora = dora
        self.start_player = start_player

    def __str__(self):
        return '\n'.join([
            f"hand {str(hand).replace(',', '')}" for hand in self.init_hand
        ]) + '\n' + \
            f'dora {self.dora}\nstrt {self.start_player}'

class Turn:
    def __init__(self, draw, tsumo, ron):
        self.draw = draw
        self.tsumo = tsumo
        self.ron = ron

    def __str__(self):
        return f'turn {self.draw} {self.tsumo} {self.ron}'

class Result:
    def __init__(self, result):
        self.result = result

    def __str__(self):
        return f'res  {str(self.result)}'

class Uma:
    def __init__(self, rank):
        self.rank = rank

    def __str__(self):
        return f'uma  {str(self.rank)}'

class Logger:
    def __init__(self, n_player):
        self.log = []
        self.n_player = n_player

    def apply_init(self, init_hand, dora, start_player):
        self.log.append(InitState(init_hand, dora, start_player))

    def apply_turn(self, draw, tsumo, ron):
        self.log.append(Turn(draw, tsumo, ron))

    def apply_result(self, result):
        self.log.append(Result(result))

    def apply_uma(self, uma):
        self.log.append(Uma(uma))

    def construct_game(self):
        games = []
        start = 0, 0
        for idx, op in enumerate(self.log):
            if isinstance(op, Uma):
                games.append(self.log[start:idx + 1])
                start = idx + 1
        return games

    def record_file(self, filename):
        with open(filename, 'w') as file:
            file.write(f'START {self.n_player}\n')
            for action in self.log:
                file.write(str(action) + '\n')
            file.write('END')

    @classmethod
    def load_log(cls, filename):
        with open(filename, 'r') as file:
            parsed_log = [
                split_op(
                    line.replace('\n', '').replace('  ', ' ')
                    ) for line in file.readlines() if line]
        log = Logger(int(parsed_log[0][1]))
        idx = 1
        while idx < len(parsed_log) - 1:
            if parsed_log[idx][0] == 'hand':
                log.apply_init(
                    [np.fromstring(parsed_log[i][1]) for i in range(idx, idx+log.n_player)],
                    int(parsed_log[idx+log.n_player][1]),
                    start_player=int(parsed_log[idx+log.n_player+1][1])
                )
                idx += log.n_player + 1
            elif parsed_log[idx][0] == 'turn':
                log.apply_turn(
                    int(parsed_log[idx][1]),
                    int(parsed_log[idx][2]),
                    np.fromstring(parsed_log[idx][3]))
            elif parsed_log[idx][0] == 'res':
                log.apply_result(np.fromstring(parsed_log[idx][1]))
            elif parsed_log[idx][0] == 'uma':
                log.apply_uma(np.fromstring(parsed_log[idx][1]))
            idx += 1
        return log

def split_op(line):
    op = []
    start = 0
    for idx, char in enumerate(line):
        if char == ' ':
            op.append(line[start:idx])
            start = idx+1
        elif char == '[':
            op.append(line[start:-1])
            break
    return op

def combine_log(logs, n_player):
    new_log = Logger(n_player)
    for log in logs:
        new_log.log += log.log
    return new_log