from .local_search import LocalSearch
from src.core.state import State
import matplotlib.pyplot as plt
import math
import random

class SimulatedAnnealing(LocalSearch):
    def __init__(self, state: State, input_basename: str = "default", max_iteration: int = 1000):
        super().__init__(state, input_basename)
        self.max_iteration = max_iteration
        self.target_acceptance = 0.9    # acceptance ratio for T0 calculation
        self.sample_size = 100          # samples for T0 calculation
        self.probability_values = []
        self.stuck_count = 0

        self.initial_temp = self._calculate_initial_temperature()
        self.beta = self._calculate_beta()

    def _calculate_initial_temperature(self) -> float:

        if not self.state.successors:
            return 100.0  # fallback

        deltas = []
        sample_count = min(self.sample_size, len(self.state.successors))

        for _ in range(sample_count):
            if not self.state.successors:
                break

            operation = random.choice(self.state.successors)
            neighbor = self.state.copy()
            neighbor.execute_operation(operation)

            delta = neighbor.calculate_objective() - self.state.calculate_objective()
            if delta > 0:  # only consider worsening moves
                deltas.append(delta)

        if not deltas:
            return 1000.0 # fallback

        avg_delta = sum(deltas) / len(deltas)

        # T0 = -avg_delta / ln(target_acceptance)
        initial_temp = -avg_delta / math.log(self.target_acceptance)

        return max(initial_temp, 1.0)

    def _calculate_beta(self) -> float:
        beta = 1.0 / (self.max_iteration * self.initial_temp)
        return beta

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

                if probability > 0.5:
                    self.probability_values.append(probability)
                    self.state.execute_operation(operation)

            # adaptive cooling (Lundy-Mees): T(k+1) = T(k) / (1 + beta * T(k))
            temperature = temperature / (1 + self.beta * temperature)

        self.final_state = self.state
        self.end_timer()
        
        return self.state

    def plot(self):
        from datetime import datetime
        objective_plot = super().plot()

        probability_plot = None
        if self.probability_values:
            plt.figure(figsize=(10, 6))
            plt.scatter(range(len(self.probability_values)), self.probability_values, s=20, color='orange', alpha=0.6)
            plt.xlabel('Iteration (when worse neighbor accepted)', fontsize=12)
            plt.ylabel('Acceptance Probability (e^(-ΔE/T))', fontsize=12)
            plt.title('Simulated Annealing - Acceptance Probability vs Iterations', fontsize=14)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()

            import os
            output_dir = f"output/plot/{self.input_basename}"
            os.makedirs(output_dir, exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{output_dir}/simulatedannealing_probability_{timestamp}.png"
            plt.savefig(filename)
            print(f"Saved: {filename}")
            plt.close()
            probability_plot = filename
        
        self.extra_plot_filename = probability_plot
        return objective_plot

    def print_summary(self):
        super().print_summary()
        print(f"Initial Temperature (auto-calculated): {self.initial_temp:.4f}")
        print(f"Beta (adaptive cooling): {self.beta:.6f}")
        print(f"Target Acceptance Ratio: {self.target_acceptance}")
        print(f"Stuck at Local Optima (ΔE=0): {self.stuck_count} times\n") 