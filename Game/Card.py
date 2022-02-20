from collections import namedtuple
from unicodedata import name
NUM_OF_SET = 4
NUM_OF_TYPE = 11
NUM_OF_CARD = NUM_OF_SET * NUM_OF_SET

RED = 0
GREEN = 10

RED_SET = 3
GREEN_SET = [2, 3, 4, 6, 8, 10]
NOBLE_SET = [0, 1, 9, 10]

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