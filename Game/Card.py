from collections import namedtuple
from . import Type

__all__ = [
    'CardTable'
]

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
        for idx in range(Type.NUM_OF_CARD):
            cset, num = idx % Type.NUM_OF_SET, idx // Type.NUM_OF_SET
            red = num == RED or (cset == RED_SET and not num == GREEN)
            green = not red and num in GREEN_SET
            noble = num in NOBLE_SET
            CardTable._table.append(CardTable.info(num, red, green, noble))

    @staticmethod
    def get(index):
        return CardTable._table[index]

    def __getitem__(self, index):
        return CardTable._table[index]

    def getid(self, num):
        return [(Type.NUM_OF_SET * num + i) for i in range(Type.NUM_OF_SET)]