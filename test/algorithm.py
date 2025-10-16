from src.utils.parse import Parse
from src.core.state import State
from src.algorithm.steepest_hill_climbing import SteepestHillClimbing
from src.algorithm.stochastic_hill_climbing import StochasticHillClimbing
from src.algorithm.sideways_hill_climbing import SidewaysHillClimbing
from src.algorithm.random_restart_hill_climbing import RandomRestartHillClimbing
from src.algorithm.simulated_annealing import SimulatedAnnealing
from src.algorithm.genetic_algorithm import GeneticAlgorithm

file_path = "./input/input.json"
parser = Parse(file_path)
data = parser.loadJson()
courses, rooms, students = parser.parseAll(data)

state = State(courses, rooms, students)
state.initial_state()
obj_value = state.calculate_objective()
print(f"Objective Value: {obj_value}")
print(f"Number of valid operations: {len(state.successors)}")
print()

algorithms = [
    ("Steepest Hill Climbing", lambda: SteepestHillClimbing(state)),
    ("Stochastic Hill Climbing", lambda: StochasticHillClimbing(state, max_iteration=150)),
    ("Sideways Hill Climbing", lambda: SidewaysHillClimbing(state, max_sideways=5)),
    ("Random Restart Hill Climbing", lambda: RandomRestartHillClimbing(state, max_restart=5)),
    ("Simulated Annealing", lambda: SimulatedAnnealing(state, initial_temp=1000, cooling_rate=0.95, max_iteration=150)),
    ("Genetic Algorithm", lambda: GeneticAlgorithm(state, population_size=8, max_iteration=150)),
]

for name, algo_factory in algorithms:
    print("=" * 80)
    print(f"Algorithm: {name}")
    print("=" * 80)

    try:
        algo = algo_factory()
        result = algo.search()

        algo.print_summary()
        algo.plot()

        print(f"[OK] {name} completed")
        print()

    except Exception as e:
        print(f"[ERROR] {name} failed: {e}")
        import traceback
        traceback.print_exc()
        print()