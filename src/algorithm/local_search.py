from abc import ABC, abstractmethod
from src.core.state import State
import matplotlib.pyplot as plt
import time
from typing import List

class LocalSearch(ABC):
    def __init__(self, state: State):
        self.state = state
        self.iteration = 0

        try:
            self.state.initial_state()
        except:
            pass

        self.initial_state: State = self.state.copy()
        self.final_state: State = None
        self.objective_history: List[float] = []
        self.duration: float = 0.0
        self.start_time: float = None

    def start_timer(self):
        self.start_time = time.time()

    def end_timer(self):
        if self.start_time is not None:
            self.duration = time.time() - self.start_time

    @abstractmethod
    def search(self) -> State:
        pass

    def plot(self):

        if not self.objective_history:
            print("No data to plot")
            return

        plt.figure(figsize=(10, 6))
        plt.plot(self.objective_history, linewidth=2)
        plt.xlabel('Iteration', fontsize=12)
        plt.ylabel('Objective Function Value', fontsize=12)
        plt.title(f'{self.__class__.__name__} - Objective vs Iterations', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        # Save plot
        filename = f"output/{self.__class__.__name__.lower()}_objective.png"
        plt.savefig(filename)
        print(f"Saved: {filename}")
        plt.close()

    def print_summary(self):

        print(f"\n{'='*80}")
        print(f"{self.__class__.__name__} - Summary")
        print(f"{'='*80}")
        print(f"Initial Objective: {self.initial_state.calculate_objective() if self.initial_state else 'N/A':.2f}")
        print(f"Final Objective: {self.final_state.calculate_objective() if self.final_state else 'N/A':.2f}")
        print(f"Total Iterations: {self.iteration}")
        print(f"Duration: {self.duration:.4f} seconds")
        print(f"{'='*80}\n")