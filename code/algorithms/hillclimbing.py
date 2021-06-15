from ..classes.models import Eengezinswoning , Bungalow, Maison
import copy
import random
WIDTH_MAX  = 180
HEIGHT_MAX = 160

class HillClimber:
    def __init__(self, map):

        self.map = copy.deepcopy(map)
        self.value = map.total_costs
        
    def mutate_houses(self, new_map, select_houses):
        for i in select_houses:
            old_house = new_map.all_houses[i]
            intersect = True
            while intersect == True:
                if old_house.type == 'eengezinswoning':
                    new_map.all_houses[i] = Eengezinswoning(old_house.id)
                if old_house.type == 'bungalow':
                    new_map.all_houses[i]= Bungalow(old_house.id)
                if old_house.type == 'maison':
                    new_map.all_houses[i]= Maison(old_house.id)
                for j in range(0, len(new_map.all_waters)):
                    water = new_map.all_waters[j]
                    intersect = new_map.all_houses[i].intersect(water)
                    if intersect == True:
                        break
                if intersect == False:
                    for k in range(0, len(new_map.all_houses)):
                        if k == i:
                            continue
                        intersect = new_map.all_houses[i].intersect(new_map.all_houses[k])
                        if intersect == True:
                            break
                        
    def mutate_map(self, new_map, number_of_houses):
        select_houses = []
        for i in range(0,len(new_map.all_houses)):
            select_houses.append(i)
        select_houses = random.sample(select_houses, number_of_houses)
        self.mutate_houses(new_map,select_houses)

    def check_solution(self, new_map,iteration):
        iteration = iteration
        new_value = new_map.total_cost()
        old_value = self.value

        # We are looking for maps that cost less!
        if new_value >= old_value:
            self.map = new_map
            self.value = new_value

    def run(self, iterations, verbose=False, mutate_houses_number=5):

        self.iterations = iterations

        for iteration in range(iterations):
            # Nice trick to only print if variable is set to True
            print(f'Iteration {iteration}/{iterations}, current value: {self.value}') if verbose else None

            # Create a copy of the graph to simulate the change
            new_map = copy.deepcopy(self.map)

            self.mutate_map(new_map, number_of_houses=mutate_houses_number)
            # Accept it if it is better
            self.check_solution(new_map,iteration)
        return self.map