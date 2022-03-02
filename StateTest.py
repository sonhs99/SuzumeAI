from Game.Board import State, Action
from Game.Type import NUM_OF_CARD, N_PLAYER
import random

print('=== State initialize Test ===')
deck = list(range(NUM_OF_CARD))
random.shuffle(deck)
state, deck = State.init(deck, 0)
print(state)

print('=== Available Action Test ===')
draw = deck[0]
print('Draw:', draw)
action = state.action(0, draw)
print('Action(turn): [')
for a in action:
    print('\t', a)
print(']')
discard = action[0].Encode()
print('Discard:', discard)
action2 = state.action(1, action[0].Encode())
print('Action(next_turn): [')
for a in action2:
    print('\t', a)
print(']')

print('=== State Apply Test ===')
apply_action = [Action.Pass()] * N_PLAYER
apply_action[state.getTurn()] = action[0]
state = state.apply(draw, apply_action)
print(state)