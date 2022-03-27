from .open import OpenAgent
from .Random import RandomAgent
from .User import UserAgent
from .mcts import MCTSAgent

__agent_list = [
    RandomAgent,
    MCTSAgent,
    OpenAgent,
]

def selector(agent_name):
    for agent in __agent_list:
        if agent.name() == agent_name:
            return agent
    return None