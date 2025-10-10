from src.local_search import LocalSearch

class SteepestHillClimbing(LocalSearch):
	def __init__(self):
		super(self)
		
	# Steepest
	def search(self):
		current = self.state.initial()
		while True:
			neighbor = self.state.highest_value_neighbor()
			self.iteration += 1
			if(neighbor.value <= current.value):
				return current
			else:
				current = neighbor
