from .local_search import LocalSearch
from src.core.state import State

class SteepestHillClimbing(LocalSearch):
    def __init__(self, state: State):
        super().__init__(state)

    def search(self) -> State:
        self.start_timer()

        while True:
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

            if best_value >= current_value:
                self.final_state = self.state
                self.end_timer()
                
                return self.state

            self.state.execute_operation(best_operation)