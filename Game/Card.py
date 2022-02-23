from collections import namedtuple
from unicodedata import name
NUM_OF_SET = 4
NUM_OF_TYPE = 11
NUM_OF_CARD = NUM_OF_SET * NUM_OF_TYPE

RED = 9
GREEN = 10

RED_SET = 3
GREEN_SET = [1, 2, 3, 5, 7, 10]
NOBLE_SET = [1, 8, 9, 10]

class CardTable:
    _table = None
    info = namedtuple('CardInfo', 'num red green noble')
    def __init__(self):
        if CardTable._table is not None: return
        CardTable._table = []
        for idx in range(NUM_OF_CARD):
            cset, num = idx % NUM_OF_SET, idx // NUM_OF_SET
            red = num == RED or (cset == RED_SET and not num == GREEN)
            green = not red and num in GREEN_SET
            noble = num in NOBLE_SET
            CardTable._table.append(CardTable.info(num, red, green, noble))

    def get(self, index):
        return CardTable._table[index]

    def getid(self, num):
        return [(NUM_OF_SET * num + i) for i in range(NUM_OF_SET)]