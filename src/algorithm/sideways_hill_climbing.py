from .local_search import LocalSearch
from src.core.state import State

class SidewaysHillClimbing(LocalSearch):
    def __init__(self, state: State, input_basename: str = "default", max_sideways: int = 10):
        super().__init__(state, input_basename)
        self.max_sideways = max_sideways
        self.sideways_count = 0

    def search(self) -> State:
        self.start_timer()

        while self.sideways_count < self.max_sideways:
            current_value = self.state.calculate_objective()
            self.objective_history.append(current_value)

            if not self.state.successors:
                self.final_state = self.state
                self.end_timer()
                return self.state

            successors_dict = {}
            for operation in self.state.successors:
                neighbor = self.state.copy()
                neighbor.execute_operation(operation)
                successors_dict[operation] = neighbor.calculate_objective()

            best_operation = min(successors_dict, key=successors_dict.get)
            best_value = successors_dict[best_operation]

            self.iteration += 1

            if best_value > current_value:
                self.final_state = self.state
                self.end_timer()
                return self.state

            if best_value == current_value:
                self.sideways_count += 1

            self.state.execute_operation(best_operation)

        self.final_state = self.state
        self.end_timer()
        
        return self.state

    def print_summary(self):
        super().print_summary()
        print(f"Sideways Moves: {self.sideways_count}/{self.max_sideways}\n")