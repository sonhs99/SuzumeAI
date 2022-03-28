from Game.Board import Action

class Round:
    def __init__(self, init_hand, start_turn):
        self.init_hand = init_hand
        self.actions = []
        self.start_turn = start_turn
        self.result = None

    def apply_action(self, action):
        self.actions.append(action)

    def apply_result(self, result):
        self.result = result

class Game:
    def __init__(self):
        self.rounds = []
        self.rank = None

    def start_round(self, init_hand, start_turn):
        self.rounds.append(Round(init_hand, start_turn))

    def apply_action(self, tsumo, ron):
        self.rounds[-1].apply_action(tsumo)
        if not tsumo.isTsumo() and Action.Ron() in ron:
            self.rounds[-1].apply_action(Action.Ron())
    
    def apply_result(self, result):
        self.rounds[-1].apply_result(result)
    
    def apply_rank(self, rank):
        self.rank = rank

class Logger:
    def __init__(self):
        self.games = []

    def start_game(self, init_hand, start_turn):
        self.games.append(Game())
        self.games[-1].start_round(init_hand, start_turn)

    def apply_action(self, tsumo, ron):
        self.games[-1].apply_action(tsumo, ron)
    
    def apply_result(self, result):
        self.rounds[-1].apply_result(result)
    
    def apply_rank(self, rank):
        self.games[-1].apply(rank)

def combine_log(loggers):
    new_log = Logger()
    for logger in loggers:
        new_log.games += logger.games
    return new_log
