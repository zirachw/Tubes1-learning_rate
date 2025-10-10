from src.local_search import LocalSearch
from random import random

class RandomRestartHillClimbing(LocalSearch):
	def __init__(self, maxRestart):
		super(self)
		self.maxRestart = maxRestart
		self.restart = 0
		# Override parent iteration attribute 
		self.iteration = [0]

	def search(self):
		current = self.state.initial()
		
		for i in range(self.maxRestart):
			while True:
				neighbor = self.state.highest_value_neighbor()
				self.iteration[i] += 1
				if(neighbor.value <= current.value):
					break
				else:
					current = neighbor