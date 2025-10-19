from .local_search import LocalSearch
from src.core.state import State
from src.core.entity import *
import matplotlib.pyplot as plt
import random
from typing import List, Tuple
from tqdm import tqdm

class GeneticAlgorithm(LocalSearch):
    def __init__(self, state: State, input_basename: str = "default", population_size: int = 4, max_iteration: int = 100):
        super().__init__(state, input_basename)
        self.population_size = population_size
        self.max_iteration = max_iteration

        self.gene_map: List[Tuple[int, int]] = []
        self._build_gene_map()

        self.max_fitness_history: List[float] = []
        self.avg_fitness_history: List[float] = []

    def _build_gene_map(self):
        for course_idx, course in enumerate(self.state.courses):
            for sks_idx in range(course.SKS):
                self.gene_map.append((course_idx, sks_idx))

    def _state_to_genes(self, state: State) -> List[Tuple[Time, Room]]:
        genes = [None] * len(self.gene_map)

        for meeting in state.course_meetings:
            course_idx = self.state.courses.index(meeting.course)
            gene = (meeting.time, meeting.room)

            for gene_idx, (c_idx, _) in enumerate(self.gene_map):
                if c_idx == course_idx and genes[gene_idx] is None:
                    genes[gene_idx] = gene
                    break

        return genes

    def _genes_to_state(self, genes: List[Tuple[Time, Room]]) -> State:
        new_state = State(self.state.courses, self.state.rooms, self.state.students)

        for gene_idx, (course_idx, _) in enumerate(self.gene_map):
            time, room = genes[gene_idx]
            course = self.state.courses[course_idx]
            meeting = CourseMeeting(course, time, room)
            new_state.course_meetings.append(meeting)

            day, hour = time.start
            new_state.schedule[room.code][day][hour].append(course)

        return new_state

    def _generate_random_individual(self) -> List[Tuple[Time, Room]]:
        genes = []

        for _ in self.gene_map:
            day = random.randint(0, 4)
            hour = random.randint(State.MIN_HOUR, State.MAX_HOUR)
            time = Time((day, hour), (day, hour + 1))
            room = random.choice(self.state.rooms)
            genes.append((time, room))

        return genes

    def _fitness(self, genes: List[Tuple[Time, Room]]) -> float:

        state = self._genes_to_state(genes)
        penalty = state.calculate_objective()

        return 1.0 / (1.0 + penalty)

    def _selection(self, population: List[List[Tuple[Time, Room]]], fitnesses: List[float]) -> List[Tuple[Time, Room]]:

        total_fitness = sum(fitnesses)
        spin = random.uniform(0, total_fitness)
        
        cumulative_fitness = 0
        for individual, fitness in zip(population, fitnesses):
            cumulative_fitness += fitness
            if cumulative_fitness >= spin:
                return individual

    def _crossover(self, parent1: List[Tuple[Time, Room]], parent2: List[Tuple[Time, Room]]) -> Tuple[List[Tuple[Time, Room]], List[Tuple[Time, Room]]]:

        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]

        return child1, child2

    def _mutate(self, genes: List[Tuple[Time, Room]]) -> List[Tuple[Time, Room]]:

        mutated = genes[:]
        idx = random.randint(0, len(mutated) - 1)
        day = random.randint(0, 4)
        hour = random.randint(State.MIN_HOUR, State.MAX_HOUR - 1)
        time = Time((day, hour), (day, hour + 1))
        room = random.choice(self.state.rooms)
        mutated[idx] = (time, room)

        return mutated

    def search(self) -> State:

        self.initial_state = self.state.copy()
        self.start_timer()

        population = [self._generate_random_individual() for _ in range(self.population_size)]

        best_individual = None
        best_fitness = 0.0

        for generation in tqdm(range(self.max_iteration), desc="Iteration"):
            fitnesses = [self._fitness(ind) for ind in population]

            max_fitness = max(fitnesses)
            avg_fitness = sum(fitnesses) / len(fitnesses)
            self.max_fitness_history.append(max_fitness)
            self.avg_fitness_history.append(avg_fitness)

            best_objective = 1.0 / max_fitness - 1.0 if max_fitness > 0 else float('inf')
            self.objective_history.append(best_objective)

            if max_fitness > best_fitness:
                best_fitness = max_fitness
                best_individual = population[fitnesses.index(max_fitness)]

            self.iteration = generation + 1

            new_population = []

            while len(new_population) < self.population_size:

                parent1 = self._selection(population, fitnesses)
                parent2 = self._selection(population, fitnesses)

                child1, child2 = self._crossover(parent1, parent2)

                child1 = self._mutate(child1)
                child2 = self._mutate(child2)

                new_population.extend([child1, child2])

            population = new_population[:self.population_size]

        self.final_state = self._genes_to_state(best_individual) if best_individual else self.state
        self.end_timer()
        
        return self.final_state

    def plot(self):
        from datetime import datetime
        objective_plot = super().plot()

        fitness_plot = None
        if self.max_fitness_history and self.avg_fitness_history:
            plt.figure(figsize=(10, 6))
            plt.plot(self.max_fitness_history, linewidth=2, label='Max Fitness', color='green')
            plt.plot(self.avg_fitness_history, linewidth=2, label='Avg Fitness', color='blue')
            plt.xlabel('Generation', fontsize=12)
            plt.ylabel('Fitness (1/(1+penalty))', fontsize=12)
            plt.title('Genetic Algorithm - Fitness vs Generations', fontsize=14)
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()

            import os
            output_dir = f"output/plot/{self.input_basename}"
            os.makedirs(output_dir, exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{output_dir}/geneticalgorithm_fitness_{timestamp}.png"
            plt.savefig(filename)
            print(f"Saved: {filename}")
            plt.close()
            fitness_plot = filename
        
        self.extra_plot_filename = fitness_plot
        return objective_plot

    def print_summary(self):
        super().print_summary()

        print(f"Population Size: {self.population_size}")
        print(f"Max Iterations: {self.max_iteration}\n")