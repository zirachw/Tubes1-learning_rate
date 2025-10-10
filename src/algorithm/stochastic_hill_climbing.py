from src.local_search import LocalSearch

class StochasticHillClimbing(LocalSearch):
	def __init__(self, maxIteration):
		super(self)
		self.maxIteration = maxIteration

	def search(self):
		current = self.state.initial()
		for _ in range(self.maxIteration):
			neighbor = self.state.random_neighbor()
			self.iteration += 1
			if(neighbor.value > current.value):
				current = neighbor
