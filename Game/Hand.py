from .Card import CardTable, RED, GREEN
from collections import namedtuple

table = CardTable()

class Triple:
	info = namedtuple('TripleInfo', 'type red green noble')
	def __init__(self, triple):
		self._triple = triple

	def count(self):
		card = [table.get(c) for c in self._triple]
		type = 0
		if card[0].num + 1 == card[1].num and \
			card[1].num + 1 == card[2].num:
			if card[0].num != RED and card[2].num != GREEN:
				type = 1
		if card[0].num == card[1].num and \
			card[1].num == card[2].num:
			type = 2
		if type == 0: return Triple.info(0, 0, 0, False)
		noble = card[0].noble or card[1].noble
		red, green = 0, 0
		for c in card:
			if c.red: red += 1
			elif c.green: green += 1
		return Triple.info(type, red, green, noble)

	def __str__(self):
		return f'Triple()'

class Hand:
	def __init__(self, hand):
		self._hand = hand
		self._hand.sort(key=lambda x: table.get(x).num)

	def point(self, draw):
		hand = self._hand + [draw]
		hand.sort(key=lambda x: table.get(x).num)
		triple = [Triple(hand[:3]).count(), Triple(hand[3:]).count()]
		if triple[0].type * triple[1].type == 0: return 0
		point = triple[0].type + triple[1].type
		
		if triple[0].red + triple[1].red == 6:
			return point + 20
		if triple[0].green + triple[1].green == 6:
			return point + 10
		if triple[0].noble and triple[1].noble:
			if triple[0].type == 2 and triple[1].type == 2:
				return point + 15
			else: point += 2
		elif not (triple[0].noble or triple[1].noble):
			point += 1
		
		point += triple[0].red + triple[1].red
		return point

	def change(self, draw, discard):
		self._hand.append(draw)
		self._hand.remove(discard)
		self._hand.sort(key=lambda x: table.get(x).num)

	def getList(self):
		return self._hand

	def __str__(self):
		return f'Hand({self._hand})'

class DiscardZone:
	def __init__(self):
		self._discard = []

	def collect(self, card):
		self._discard.append(card)

	def getList(self):
		return self._discard

	def __str__(self):
		return f'Hand({self._discard})'