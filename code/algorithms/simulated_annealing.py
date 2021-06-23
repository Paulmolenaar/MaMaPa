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

        # Calculate the probability of accepting this new map
        delta = (new_value - old_value)
        if delta  > 0:
            probability = 1
        else:
            a = delta / self.T
            probability = math.exp(a)


        # Pull a random number between 0 and 1 and see if we accept the map, if so, update the map
        pull = random.random()
        if pull < probability:
            self.map = new_map
            self.value = new_value

        # Update the temperature
        self.update_temperature()

    # Attempts to rotate all houses 90 degrees
    def iterate_rotations(self):
        for i in range(0,len(self.map.all_houses)):
            test_map = copy.deepcopy(self.map)
            if (test_map.all_houses[i].width == test_map.all_houses[i].length):
                continue


            # Rotate house, check if profit gets higher
            if (test_map.all_houses[i].rotate(test_map.all_waters)):
                self.hill_check_solution(test_map)
            else:
                continue
    
    # Check solution for rotate function
    def hill_check_solution(self, new_map):
        new_value = new_map.total_cost()
        old_value = self.value

        # We are looking for maps that cost more, so replace the map if the costs are higher
        if new_value >= old_value:
            self.map = new_map
            self.value = new_value

    # Run the algorithm
    def run(self, iterations, verbose=True, mutate_houses_number=5):
        self.iterations = iterations

        for iteration in range(iterations):
            if iteration % 1000 == 0:
                # Print the iteration and value every 1000th iteration if verbose is set to True
                print(f'Iteration {iteration}/{iterations}, current value: {self.value}') if verbose else None

            # Create a copy of the old map to simulate the change
            new_map = copy.deepcopy(self.map)
            self.mutate_map(new_map, number_of_houses=mutate_houses_number)

            # Accept if the new map is better
            self.check_solution(new_map)

        self.iterate_rotations()
        return self.map
