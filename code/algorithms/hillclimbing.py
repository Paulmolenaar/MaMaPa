from ..classes.models import Eengezinswoning , Bungalow, Maison
import copy
import random
WIDTH_MAX  = 180
HEIGHT_MAX = 160

class HillClimber:

    # Hill climber algorithm, first set the initial map and the initial costs
    def __init__(self, map):
        self.map = copy.deepcopy(map)
        self.value = map.total_costs

    # Do the mutations on the map
    def mutate_houses(self, new_map, select_houses):

        # Take the selected houses and replace it with a new one
        for i in select_houses:
            old_house = new_map.all_houses[i]
            intersect = True
            while intersect == True:
                if old_house.type == 'eengezinswoning':
                    new_map.all_houses[i] = Eengezinswoning(old_house.id)

                if old_house.type == 'bungalow':
                    new_map.all_houses[i] = Bungalow(old_house.id)

                if old_house.type == 'maison':
                    new_map.all_houses[i] = Maison(old_house.id)

                for j in range(0, len(new_map.all_waters)):
                    water = new_map.all_waters[j]
                    intersect = new_map.all_houses[i].intersect(water)

                    # Check if the new house intersects with water, if so, place again
                    if intersect == True:
                        break

                # Check if the new house itersects with the other houses, if so, place again
                if intersect == False:
                    for k in range(0, len(new_map.all_houses)):
                        if k == i:
                            continue
                        intersect = new_map.all_houses[i].intersect(new_map.all_houses[k])
                        if intersect == True:
                            break

    # Select which houses to replace
    def mutate_map(self, new_map, number_of_houses):
        select_houses = []
        for i in range(0,len(new_map.all_houses)):
            select_houses.append(i)
        select_houses = random.sample(select_houses, number_of_houses)

        # Use the mutate_houses function to replace the house
        self.mutate_houses(new_map, select_houses)

    # Check if the new map gives a better solution
    def check_solution(self, new_map, iteration):
        iteration = iteration
        new_value = new_map.total_cost()
        old_value = self.value

        # We are looking for maps that cost less, so replace the map if the costs are higher
        if new_value >= old_value:
            self.map = new_map
            self.value = new_value

    # Iterate over the hill climber alorithm as much as the user wants
    def run(self, iterations, verbose=False, mutate_houses_number=5):
        self.iterations = iterations

        for iteration in range(iterations):

            # Nice trick to only print if variable is set to True
            print(f'Iteration {iteration}/{iterations}, current value: {self.value}') if verbose else None

            # Create a copy of the old graph to simulate the change
            new_map = copy.deepcopy(self.map)
            self.mutate_map(new_map, number_of_houses=mutate_houses_number)

            # Accept if the new map is better
            self.check_solution(new_map, iteration)

        return self.map
