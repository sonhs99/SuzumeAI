from . import Card

RED = 31
GREEN = 32
NULL = 0

table = Card.CardTable()

def colored(text, color):
    if color == 'r': color = 31
    elif color == 'g': color = 32
    else: color = 0 
    return f'\x1b[{color}m{text}'

def card_to_string(card):
    color, num = NULL, table.get(card).num

    if table.get(card).red: color = RED
    elif table.get(card).green: color = GREEN

    if num == Card.GREEN: num = 'G'
    elif num == Card.RED: num = 'R'
    else: num = str(num + 1)
    return f'\x1b[{color}m{num}'

def serise_to_string(serise):
    string = ''
    for card in serise:
        string += card_to_string(card)
    return string + '\x1b[0m'