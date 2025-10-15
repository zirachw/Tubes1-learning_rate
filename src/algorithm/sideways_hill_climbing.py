from src.local_search import LocalSearch

class SidewayHillClimbing(LocalSearch):
	def __init__(self, maxSideways):
		super(self)
		self.maxSidewaysIteration = maxSideways
		self.sidewaysIteration = 0

	def search(self):
		current = self.state.initial()
		while True and self.sidewaysIteration < self.maxSidewaysIteration:
			neighbor = self.state.highest_value_neighbor()
			self.iteration += 1
			if(neighbor.value < current.value):
				return current
			elif(neighbor.value == current.value):
				self.sidewaysIteration += 1
			current = neighbor
