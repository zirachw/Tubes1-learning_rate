from .local_search import LocalSearch
from src.core.state import State
import matplotlib.pyplot as plt
import math

class SimulatedAnnealing(LocalSearch):
    def __init__(self, state: State, initial_temp: float = 1000.0, cooling_rate: float = 0.95, max_iteration: int = 1000):
        super().__init__(state)
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.max_iteration = max_iteration
        self.probability_values = []
        self.stuck_count = 0

    def search(self) -> State:
        self.start_timer()

        temperature = self.initial_temp

        for _ in range(self.max_iteration):
            current_value = self.state.calculate_objective()
            self.objective_history.append(current_value)

            if temperature == 0:
                break

            operation = self.state.get_random_neighbor()
            self.iteration += 1

            neighbor = self.state.copy()
            neighbor.execute_operation(operation)
            neighbor_value = neighbor.calculate_objective()

            delta = neighbor_value - current_value

            if delta < 0:
                self.state.execute_operation(operation)
            else:
                if delta == 0:
                    self.stuck_count += 1

                probability = math.exp(-delta / temperature)
                self.probability_values.append(probability)

                if probability > 0.5:
                    self.state.execute_operation(operation)

            temperature *= self.cooling_rate

        self.final_state = self.state
        self.end_timer()
        
        return self.state

    def plot(self):
        from datetime import datetime
        objective_plot = super().plot()

        probability_plot = None
        if self.probability_values:
            plt.figure(figsize=(10, 6))
            plt.plot(self.probability_values, linewidth=2, color='orange')
            plt.xlabel('Iteration (when worse neighbor accepted)', fontsize=12)
            plt.ylabel('Acceptance Probability (e^(-ΔE/T))', fontsize=12)
            plt.title('Simulated Annealing - Acceptance Probability vs Iterations', fontsize=14)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()

            import os
            os.makedirs("output/plot", exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"output/plot/simulatedannealing_probability_{timestamp}.png"
            plt.savefig(filename)
            print(f"Saved: {filename}")
            plt.close()
            probability_plot = filename
        
        self.extra_plot_filename = probability_plot
        return objective_plot

    def print_summary(self):
        super().print_summary()
        print(f"Initial Temperature: {self.initial_temp}")
        print(f"Cooling Rate: {self.cooling_rate}")
        print(f"Stuck at Local Optima (ΔE=0): {self.stuck_count} times\n") 