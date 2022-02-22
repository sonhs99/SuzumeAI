from Game import Board, Experience, Display
from Game.agents import Random

def render_state(state, actions):
    print('Turn :', state.turn)
    print('Draw:', Display.card_to_string(state.draw)+ '\x1b[0m')
    for i in range(state.n_player):
        hand = Display.serise_to_string(state.hand[i].toArray())
        discard = Display.serise_to_string(state.discard[i].toArray())
        discard += ' ' * (6 - len(discard) // 6)
        action = ''
        if actions[i].isTsumo(): action += 'Tsumo'
        elif actions[i].isRon(): action += 'Ron'
        elif not actions[i].isPass():
            card = Display.card_to_string(actions[i].Encode()) + '\x1b[0m'
            action += f'Discard({card})'
        print('[%d] %s : %s : %s' % (i + 1, hand, discard, action))

print('=== Game Test ===')

buffer = Experience.ExperienceBuffer()
players = [
    Random.RandomAgent() for i in range(4)
]
board = Board.Board(players, buffer)
board.play()

print('Lenght:', buffer.len())
print()
exp = buffer.get(0)
render_state(exp[0], exp[1])

print()
exp = buffer.get(-1)
render_state(exp[0], exp[1])