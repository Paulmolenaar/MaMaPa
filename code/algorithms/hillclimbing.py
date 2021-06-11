from  ..classes.models import House
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
            valid = True
#            counter = 0
            while valid == True:
#                counter = counter + 1
#                if counter % 100 == 0:
#                    print(counter)
                x_bottomleft = random.randint(0 + old_house.min_distance,(WIDTH_MAX - old_house.width - old_house.min_distance))
                y_bottomleft = random.randint(0 + old_house.min_distance,(HEIGHT_MAX - old_house.length  - old_house.min_distance))
                new_map.all_houses[i] = House(old_house.type, old_house.id, old_house.length , old_house.width , [x_bottomleft,y_bottomleft], old_house.min_distance)
                for j in range(0, len(new_map.all_waters)):
                    water = new_map.all_waters[j]
                    valid = new_map.all_houses[i].intersect(water, True)
                    if valid == True:
                        break
                if valid == False:
                    for k in range(0, len(new_map.all_houses)):
                        if k == i:
                            continue
                        valid = new_map.all_houses[i].intersect(new_map.all_houses[k], False)
                        if valid == True:
                            break
                        
    def mutate_map(self, new_map, number_of_houses):
        select_houses = []
        for i in range(0,len(new_map.all_houses)):
            select_houses.append(i)
        select_houses = random.sample(select_houses, number_of_houses)
        self.mutate_houses(new_map,select_houses)

    def check_solution(self, new_map):
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
            self.check_solution(new_map)
        return self.map