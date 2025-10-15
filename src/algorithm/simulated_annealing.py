from src.local_search import LocalSearch
from random import random
import math

class SimulatedAnnealing(LocalSearch):
	def __init__(self):
		super(self)
		self.probabilityValues = []
		self.localOptimaCount = 0

	def search(self):
		current = self.state.initial()
		
		while True:
			# TODO Implement Scheduler
			t = schedule() # type: ignore 

			if(t == 0):
				return current
			
			next = self.state.random_neighbor()
			de = next.value - current.value
			if(de > 0):
				current = next
			else:
				if(de == 0):
					self.localOptimaCount += 1
				probability = pow(math.e, de/t)
				self.probabilityValues.append(probability)
				# random.random() produces 0.0 <= X < 1.0
				if (random.random() < probability):
					current = next 
		