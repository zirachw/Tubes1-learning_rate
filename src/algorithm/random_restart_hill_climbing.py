from .local_search import LocalSearch
from src.core.state import State

class RandomRestartHillClimbing(LocalSearch):
    def __init__(self, state: State, max_restart: int):
        super().__init__(state)
        self.max_restart = max_restart
        self.iteration_per_restart = []

    def search(self) -> State:
        self.start_timer()

        best_overall = None
        best_value = float('inf')

        for _ in range(self.max_restart):
            current_state = self.state.copy()
            current_state.course_meetings.clear()
            current_state.initial_state()

            restart_iterations = 0

            while True:
                self.objective_history.append(current_state.calculate_objective())

                if not current_state.successors:
                    break

                successors_dict = {}
                for operation in current_state.successors:
                    neighbor = current_state.copy()
                    neighbor.execute_operation(operation)
                    successors_dict[operation] = neighbor.calculate_objective()

                best_operation = min(successors_dict, key=successors_dict.get)
                neighbor_value = successors_dict[best_operation]

                restart_iterations += 1
                self.iteration += 1

                if neighbor_value >= current_state.calculate_objective():
                    break

                current_state.execute_operation(best_operation)

            self.iteration_per_restart.append(restart_iterations)

            final_value = current_state.calculate_objective()
            if best_overall is None or final_value < best_value:
                best_overall = current_state
                best_value = final_value

        self.final_state = best_overall if best_overall else self.state
        self.end_timer()

        return self.final_state

    def print_summary(self):
        super().print_summary()
        print(f"Number of Restarts: {self.max_restart}")
        print(f"Iterations per restart: {self.iteration_per_restart}\n")