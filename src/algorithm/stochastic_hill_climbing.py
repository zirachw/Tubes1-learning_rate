from .local_search import LocalSearch
from src.core.state import State

class StochasticHillClimbing(LocalSearch):
    def __init__(self, state: State, input_basename: str = "default", max_iteration: int = 1000):
        super().__init__(state, input_basename)
        self.max_iteration = max_iteration

    def search(self) -> State:
        self.start_timer()

        for _ in range(self.max_iteration):
            current_value = self.state.calculate_objective()
            self.objective_history.append(current_value)

            operation = self.state.get_random_neighbor()
            self.iteration += 1

            neighbor = self.state.copy()
            neighbor.execute_operation(operation)

            if neighbor.calculate_objective() < current_value:
                self.state.execute_operation(operation)

        self.final_state = self.state
        self.end_timer()
        
        return self.state