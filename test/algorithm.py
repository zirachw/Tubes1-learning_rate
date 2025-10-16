from src.utils.parse import Parse
from src.core.state import State
from src.algorithm.steepest_hill_climbing import SteepestHillClimbing
from src.algorithm.stochastic_hill_climbing import StochasticHillClimbing
from src.algorithm.sideways_hill_climbing import SidewaysHillClimbing
from src.algorithm.random_restart_hill_climbing import RandomRestartHillClimbing
from src.algorithm.simulated_annealing import SimulatedAnnealing
from src.algorithm.genetic_algorithm import GeneticAlgorithm

print("=" * 80)
print("ALGORITHM TESTING")
print("=" * 80)
print()

# Load data
file_path = "./input/input.json"
parser = Parse(file_path)
data = parser.loadJson()
courses, rooms, students = parser.parseAll(data)

state = State(courses, rooms, students, objective='student_conflicts')
state.initial_state()
penalty1 = state.calculate_objective()
print(f"Objective: {state.objective}")
print(f"Penalty: {penalty1}")
print(f"Number of valid operations: {len(state.successors)}")

# Test each algorithm
algorithms = [
    # ("Steepest Hill Climbing", lambda: SteepestHillClimbing(state)),
    ("Stochastic Hill Climbing", lambda: StochasticHillClimbing(state, max_iteration=1000)),
    # ("Sideways Hill Climbing", lambda: SidewaysHillClimbing(state, max_sideways=10)),
    # ("Random Restart Hill Climbing", lambda: RandomRestartHillClimbing(state, max_restart=3)),
    ("Simulated Annealing", lambda: SimulatedAnnealing(state, initial_temp=1000, cooling_rate=0.95, max_iteration=1000)),
    ("Genetic Algorithm", lambda: GeneticAlgorithm(state, population_size=8, max_iteration=1000)),
]

for name, algo_factory in algorithms:
    print("=" * 80)
    print(f"TESTING: {name}")
    print("=" * 80)

    try:
        # Create algorithm instance
        algo = algo_factory()

        # Run search
        print(f"Running {name}...")
        result = algo.search()

        # Print summary
        algo.print_summary()

        # Plot
        print(f"Generating plots...")
        algo.plot()

        print(f"[OK] {name} completed successfully")
        print()

    except Exception as e:
        print(f"[ERROR] {name} failed: {e}")
        import traceback
        traceback.print_exc()
        print()

print("=" * 80)
print("ALL TESTS COMPLETED")
print("=" * 80)
