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
	def __init__(self, turn, hand, discard):
		self.turn = turn
		self.hand = hand
		self.discard = discard
		self.draw = None

	@staticmethod
	def init(self, n_players, deck):
		hand = []
		discard = [DiscardZone()] * n_players
		for i in range(n_players):
			hand.append(Hand(deck[i*5:(i + 1)*5]))
		return State(0, hand, discard), deck[n_players*5:]

	def apply(self, actions):
		pass

	def action(self, turn, card):
		pass