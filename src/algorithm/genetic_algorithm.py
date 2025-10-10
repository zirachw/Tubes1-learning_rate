from src.local_search import LocalSearch
from random import random

class GeneticAlgorithm(LocalSearch):
	def __init__(self, maxIteration):
		super(self)
		self.maxIteration = maxIteration
		pass

	# Steepest
	def search(self):
		# Random threshold 0.9
		iteration = 0
		current = self.state.initial_genetic()
		while current.value < 0.9 or iteration < self.maxIteration:
			new_population = []
			self.iteration += 1

			for _ in range(self.state.population()):
				# TODO: Implement fitness function
				x = self.state.random_selection(self.state.population(), fitness_function()) #type: ignore
				y = self.state.random_selection(self.state.population(), fitness_function()) #type: ignore
	
				child = self.state.reproduce(x,y)

				# Random low threshold value = 0.3
				if(random.random() < 0.3):
					child = self.state.mutate()
				new_population = new_population.append(child)
			current = new_population
		
		return self.state.highest_fitness_state()
		
