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
            if old_house.type == 'eengezinswoning':
                new_map.all_houses[i] = Eengezinswoning(old_house.id)

            if old_house.type == 'bungalow':
                new_map.all_houses[i] = Bungalow(old_house.id)

            if old_house.type == 'maison':
                new_map.all_houses[i] = Maison(old_house.id)

            intersect = True
            while intersect == True:

                new_map.all_houses[i].random_location()

                for j in range(0, len(new_map.all_waters)):
                    water = new_map.all_waters[j]
                    intersect = new_map.all_houses[i].intersect(water)

                    # Check if the new house intersects with water, if so, place again
                    if intersect == True:
                        break

                # Check if the new house intersects with the other houses, if so, place again
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
    def check_solution(self, new_map):
        new_value = new_map.total_cost()
        old_value = self.value

        # We are looking for maps that cost more, so replace the map if the costs are higher
        if new_value >= old_value:
            self.map = new_map
            self.value = new_value

    # Swap some given houses
    def swap_house(self, new_map, list_of_houses):

        # Swap the coordinates of the houses
        first_house = list_of_houses[0]
        house = new_map.all_houses[first_house]
        second_house = list_of_houses[1]
        other_house = new_map.all_houses[second_house]
        storage = house.bottom_left
        house.bottom_left = other_house.bottom_left
        house.to_coordinates(house.bottom_left)
        other_house.bottom_left = storage
        other_house.to_coordinates(other_house.bottom_left)
        new_map.all_houses[second_house] = other_house
        new_map.all_houses[first_house] = house

        # Check if the house intersect with water, if so, cancel the swap
        intersect = False
        for g in range(0, len(new_map.all_waters)):
            water = new_map.all_waters[g]
            intersect = new_map.all_houses[second_house].intersect(water)
            if intersect == True:
                break
            
        if intersect == False:
            for g in range(0, len(new_map.all_waters)):
                water = new_map.all_waters[g]
                intersect = new_map.all_houses[first_house].intersect(water)
                if intersect == True:
                    break

        # Check if the new house itersects with the other houses, if so, cancel the swap
        if intersect == False:
            for p in range(0, len(new_map.all_houses)):
                if p == first_house:
                    continue
                intersect = new_map.all_houses[first_house].intersect(new_map.all_houses[p])
                if intersect == True:
                    break

        if intersect == False:
            for p in range(0, len(new_map.all_houses)):
                if p == second_house:
                    continue
                intersect = new_map.all_houses[second_house].intersect(new_map.all_houses[p])
                if intersect == True:
                    break

        # Check if the minimum free distance is on the map
        if intersect == False:
            for houses in [house, other_house]:
                intersect = houses.check_distance()
                if intersect == True:
                    break

        # Check if the solution is better
        if intersect == False:
            self.check_solution(new_map)

    # Attempts to rotate all houses 90 degrees
    def iterate_rotations(self):
        for i in range(0,len(self.map.all_houses)):
            test_map = copy.deepcopy(self.map)
            if (test_map.all_houses[i].width == test_map.all_houses[i].length):
                continue


            # rotate house, check if profit gets higher
            if (test_map.all_houses[i].rotate(test_map.all_waters)):
                self.check_solution(test_map)
            else:
                continue

    # Iterate over the hill climber alorithm as much as the user wants
    def run(self, iterations, verbose=True, mutate_houses_number=5):
        self.iterations = iterations

        for iteration in range(iterations):

            if iteration % 1000 == 0:
                # Print the iteration and value every 1000th iteration if verbose is set to True
                print(f'Iteration {iteration}/{iterations}, Current value: {self.value}') if verbose else None

            # Create a copy of the old map to simulate the change
            new_map = copy.deepcopy(self.map)
            self.mutate_map(new_map, number_of_houses=mutate_houses_number)

            # Accept if the new map is better
            self.check_solution(new_map)


        # Select random houses and swap them
        select_houses = []
        for i in range(0,len(new_map.all_houses)):
            select_houses.append(i)

        for i in range(2000):
            new_map = copy.deepcopy(self.map)
            if i % 1000 == 0:
                print(f'i {i}/{iterations}, current value: {self.value}') if verbose else None
            my_houses = random.sample(select_houses, 2)
            self.swap_house(new_map, my_houses)

        self.iterate_rotations()

        return self.map
