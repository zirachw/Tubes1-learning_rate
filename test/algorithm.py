from src.utils.parse import Parse
from src.core.state import State
from src.algorithm.steepest_hill_climbing import SteepestHillClimbing
from src.algorithm.stochastic_hill_climbing import StochasticHillClimbing
from src.algorithm.sideways_hill_climbing import SidewaysHillClimbing
from src.algorithm.random_restart_hill_climbing import RandomRestartHillClimbing
from src.algorithm.simulated_annealing import SimulatedAnnealing
from src.algorithm.genetic_algorithm import GeneticAlgorithm
import matplotlib.pyplot as plt

print("=" * 80)
print("ALGORITHM TESTING")
print("=" * 80)
print()

# Load data
print("Loading input data...")
parser = Parse("./input/input.json")
data = parser.loadJson()
courses, rooms, students = parser.parseAll(data)
print(f"[OK] Loaded {len(courses)} courses, {len(rooms)} rooms, {len(students)} students")
print()

# Test each algorithm
algorithms = [
    ("Steepest Hill Climbing", lambda: SteepestHillClimbing(State(courses, rooms, students, 'capacity_overflow'))),
    ("Stochastic Hill Climbing", lambda: StochasticHillClimbing(State(courses, rooms, students, 'capacity_overflow'), max_iteration=100)),
    ("Sideways Hill Climbing", lambda: SidewaysHillClimbing(State(courses, rooms, students, 'capacity_overflow'), max_sideways=10)),
    ("Random Restart Hill Climbing", lambda: RandomRestartHillClimbing(State(courses, rooms, students, 'capacity_overflow'), max_restart=3)),
    ("Simulated Annealing", lambda: SimulatedAnnealing(State(courses, rooms, students, 'capacity_overflow'), initial_temp=1000, cooling_rate=0.95, max_iteration=100)),
    ("Genetic Algorithm", lambda: GeneticAlgorithm(State(courses, rooms, students, 'capacity_overflow'), population_size=4, max_iteration=100)),
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
        plt.savefig(f"output/{name.replace(' ', '_').lower()}_plot.png")
        plt.close()

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
