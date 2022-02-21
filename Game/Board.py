from .Card import CardTable
from .Hand import Hand, DiscardZone

table = CardTable()

class Action:
	_tsumo = 45
	_ron = 46
	_pass = 47
	def __init__(self, idx):
		self._idx = idx

	@staticmethod
	def Discard(num):
		return Action(num)

	@staticmethod
	def Tsumo():
		return Action(Action._tsumo)

	@staticmethod
	def Ron():
		return Action(Action._ron)

	@staticmethod
	def Pass():
		return Action(Action._pass)

	def Encode(self):
		return self._idx

	def isTsumo(self):
		return self._idx == Action._tsumo

	def isRon(self):
		return self._idx == Action._ron

	def isPass(self):
		return self._idx == Action._pass

	def __str__(self):
		string = None
		if self.isTsumo(): string = 'Tsumo'
		elif self.isRon(): string = 'Ron'
		elif self.isPass(): string = 'Pass'
		else: string = f'Discard:{self._idx}'
		return 'Action(' + string + ')'

class State:
	def __init__(self, n_player, turn, hand, discard):
		self.n_player = n_player
		self.turn = turn
		self.hand = hand
		self.discard = discard
		self.draw = None

	@staticmethod
	def init(self, n_player, deck):
		hand = []
		discard = [DiscardZone()] * n_player
		for i in range(n_player):
			hand.append(Hand(deck[i*5:(i + 1)*5]))
		return State(0, n_player, hand, discard), deck[n_player*5:]

	def apply(self, draw, actions):
		self.draw = draw
		for action in actions:
			if action.isTsumo() or action.isRon():
				return None

		from copy import deepcopy
		hand = deepcopy(self.hand)
		discard = deepcopy(self.discard)
		discarded_card = actions[self.turn].Encode()
		hand[self.turn].change(draw, discarded_card)
		discard[self.turn].collect(discarded_card)
		return State(self.n_player, (self.turn + 1) % self.n_player, hand, discard)

	def action(self, turn, card):
		if turn == self.turn:
			pass
		else:
			pass