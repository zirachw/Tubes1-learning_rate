from abc import abstractmethod

class LocalSearch:
    def __init__(self, algorithm: str, state):
        self.algorithm = algorithm
        self.state = state
        self.iteration = 0

    @abstractmethod
    def search(self):
        pass



