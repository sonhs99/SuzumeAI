from Game import Board, Experience, Display
from Game.agents import Random

def render_state(turn, state, actions):
    print('\nTurn:', turn)
    print('Dora:', Display.card_to_string(state.dora) + '\x1b[0m')
    draw = Display.card_to_string(state.draw)+ '\x1b[0m'
    for i in range(state.n_player):
        draws = draw if i == state.turn else ' '
        hand = Display.serise_to_string(state.hand[i].toArray())
        discard = Display.serise_to_string(state.discard[i].toArray())
        discard += ' ' * (6 - len(discard) // 6)
        action = ''
        if actions[i].isTsumo(): action += 'Tsumo'
        elif actions[i].isRon(): action += 'Ron'
        elif not actions[i].isPass():
            card = Display.card_to_string(actions[i].Encode()) + '\x1b[0m'
            action += f'Discard({card})'
        print(f'[{i + 1}] {hand} {draws} : {discard} : {action}')

print('=== Game Test ===')

buffer = Experience.ExperienceBuffer()
players = [
    Random.RandomAgent() for i in range(4)
]
board = Board.Board(players, buffer)
board.play()

for i in range(buffer.len()):
    exp = buffer.get(i)
    render_state(i, exp[0], exp[1])

print('\nResult :', buffer.get(0)[2])