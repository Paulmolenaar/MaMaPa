import random
import math
import copy
from .hillclimbing import HillClimber


class SimulatedAnnealing(HillClimber):

    # Simulated Annealing algorithm
    def __init__(self, map, temperature=100000):

        # Use the init of the Hillclimber class
        super().__init__(map)

        # Starting temperature and current temperature
        self.T0 = temperature
        self.T = temperature

    # Updates the temperature with every iteration
    def update_temperature(self):
        self.T = self.T - (self.T0 / self.iterations)


    # Check if the solution is better following simulated annealing algorithm
    def check_solution(self, new_map):
        new_value = new_map.total_cost()
        old_value = self.value

        # Calculate the probability of accepting this new graph
        delta = (new_value - old_value)
        if delta  > 0:
            probability = 1
        else:
            a = delta / self.T
            probability = math.exp(a)


        # Pull a random number between 0 and 1 and see if we accept the graph, if so, update the map
        pull = random.random()
        if pull < probability:
            self.map = new_map
            self.value = new_value

        # Update the temperature
        self.update_temperature()

    # Run the algorithm
    def run(self, iterations, verbose=True, mutate_houses_number=5):
        self.iterations = iterations

        for iteration in range(iterations):
            if iteration % 1000 == 0:
                # Nice trick to only print if variable is set to True
                print(f'Iteration {iteration}/{iterations}, current value: {self.value}') if verbose else None

            # Create a copy of the old graph to simulate the change
            new_map = copy.deepcopy(self.map)
            self.mutate_map(new_map, number_of_houses=mutate_houses_number)

            # Accept if the new map is better
            self.check_solution(new_map)

        return self.map
