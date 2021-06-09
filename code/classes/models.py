import csv
import random
import math

WIDTH_MAX  = 180
HEIGHT_MAX = 160

class House():
    def __init__(self, type, uid, length , width , bottom_left, min_distance):
        self.type = type
        self.id = uid
        self.value = 0
        self.min_distance = min_distance
        self.length = length
        self.width = width
        self.bottom_left = bottom_left
        self.bottom_right = 0
        self.top_left = 0
        self.top_right = 0
        self.neighbours = {}
        self.cost = 0
        self.coordinates = self.coordinates(bottom_left)

    def coordinates(self, bottom_left):
        # generates the remaining coordinates
        self.bottom_left = bottom_left
        self.bottom_right = [bottom_left[0] + self.width, bottom_left[1]]
        self.top_left = [bottom_left[0] , bottom_left[1] + self.length]
        self.top_right = [bottom_left[0] + self.width, bottom_left[1] + self.length]


    def cost_function(self, min_distance):
        # Generates the costs per house
        self.min_distance = min_distance
        if self.type =='maison':
            self.cost = 610000 * (1 + (0.06 * (self.min_distance-6)))
            return self.cost
        if self.type =='eengezinswoning':
            self.cost = 285000 * (1 + (0.03 * (self.min_distance-2)))
            return self.cost
        if self.type =='bungalow':
            self.cost = 399000 * (1 + (0.04 * (self.min_distance-3)))
            return self.cost

    def intersect(self, other, water):
        if water:
            min_distance = 0
        else:
            min_distance = max(self.min_distance, other.min_distance)
        test1 = self.bottom_left[0] - min_distance >= other.top_right[0]
        test2 = other.bottom_left[0] >= self.top_right[0] + min_distance
        if ( test1 or test2):
            return False
        
        test1 = self.bottom_left[1] - min_distance >= other.top_right[1]
        test2 = other.bottom_left[1] >= self.top_right[1] + min_distance
        if(test1 or test2):
            return False
        
        
        return True


class Water():
    def __init__(self, type, uid, bottom_left, top_right):
        self.type = type
        self.id = uid
        self.bottom_left = bottom_left
        self.bottom_right = 0
        self.top_left = 0
        self.top_right = top_right

    def corners(self):
        width = self.top_right[0]- self.bottom_left[0]
        height = self.top_right[1] - self.bottom_left[1]
        self.bottom_right = [self.bottom_left[0] + width,self.bottom_left[1]]
        self.top_left = [self.bottom_left[0],self.bottom_left[1] + height]
        return 1


class Map():
    def __init__(self, source_file, number_of_houses):
        self.all_waters = self.load_water(source_file)
        self.all_houses = self.make_houses(number_of_houses)
        self.total_costs = self.total_cost()

    def load_water(self, source_file):
        waters = {}
        with open(source_file, 'r') as in_file:
            reader = csv.DictReader(in_file)
            line = 0
            for row in reader:
                blxy = list(map(int, row['bottom_left_xy'].split(",")))
                trxy = xy = list(map(int, row['top_right_xy'].split(",")))
                waters[line] = Water("water", line+1, blxy, trxy)
                line = line + 1

        return waters

    def make_houses(self, number_of_houses):
         houses = {}
         width_dict =	{"maison": 12,"bungalow": 11,"eengezinswoning": 8}
         height_dict =	{"maison": 10,"bungalow": 7,"eengezinswoning": 8}
         min_distance_dict = {"maison": 6,"bungalow": 3,"eengezinswoning": 2}
         amount_maisons = int(0.15 * number_of_houses)
         amount_bungalows = int(0.25 * number_of_houses)
         amount_eengezinswoning = int(0.60 * number_of_houses)
        #  amount_maisons = 2
        #  amount_bungalows = 0
        #  amount_eengezinswoning = 0
         types_of_houses = []
         for i in range(amount_maisons):
             types_of_houses.append("maison")
         for j in range(amount_bungalows):
             types_of_houses.append("bungalow")
         for k in range(amount_eengezinswoning):
             types_of_houses.append("eengezinswoning")
         teller = 0
         for x in types_of_houses:
             height = height_dict.get(x)
             width = width_dict.get(x)
             min_distance = min_distance_dict.get(x)
             if x == 'eengezinswoning':
                 id_house = amount_eengezinswoning
                 amount_eengezinswoning = amount_eengezinswoning -1
             if x == 'bungalow':
                 id_house = amount_bungalows
                 amount_bungalows = amount_bungalows -1
             if x == 'maison':
                 id_house = amount_maisons
                 amount_maisons = amount_maisons -1
             valid = True
             while valid == True:
                x_bottomleft = random.randint(0,(WIDTH_MAX - width))
                y_bottomleft = random.randint(0,(HEIGHT_MAX - height))
                # x_bottomleft = 1+(18 * teller)
                # y_bottomleft = 40 +(16*teller)
                houses[teller] = House(x, id_house, height, width, [x_bottomleft,y_bottomleft], min_distance)
                for j in range(0, len(self.all_waters)):
                    water = self.all_waters[j]
                    valid = houses[teller].intersect(water, True)
                    if valid == True:
                        break
                if valid == False:
                    for i in range(0, teller):
                        valid = houses[teller].intersect(houses[i], False)
                        if valid == True:
                            break
             teller = teller + 1
         return houses

    def total_cost(self):
        total_cost = 0
        DEBUG_housenr = 0
        for house in self.all_houses.items():
            min_distance = 180
            distance = 0
            house = house[1]
            for other_house in self.all_houses.items():
                if other_house == house:
                    continue
                other_house = other_house[1]
                rechts = house.bottom_left[0] > other_house.top_right[0]
                links = house.top_right[0] < other_house.bottom_left[0]
                boven = house.bottom_left[1] > other_house.top_right[1]
                onder = house.top_right[1] < other_house.bottom_left[1]
                if rechts:
                    distance = house.bottom_left[0] - other_house.top_right[0]
                if links:
                    distance = other_house.bottom_left[0] - house.top_right[0]
                if boven:
                    distance = house.bottom_left[1] - other_house.top_right[1]
                if onder: 
                    distance = other_house.bottom_left[1] - house.top_right[1]
                if links and boven:
                    distance = round(math.sqrt(((house.top_right[0] - other_house.bottom_left[0]) ** 2) + ((house.bottom_left[1] - other_house.top_right[1]) ** 2)))
                if rechts and boven:
                    distance = round(math.sqrt(((house.bottom_left[0] - other_house.top_right[0]) ** 2) + ((house.bottom_left[1] - other_house.top_right[1]) ** 2)))
                if links and onder:
                    a = other_house.bottom_left[0] - house.top_right[0]
                    b = house.top_right[1] - other_house.bottom_left[1] 
                    a = a ** 2
                    b = b ** 2
                    distance = math.sqrt(a + b)
                    distance = round(distance)
                if rechts and onder:
                    distance = round(math.sqrt(((house.bottom_left[0] - other_house.top_right[0]) ** 2) + ((house.top_right[1] - other_house.bottom_left[1]) ** 2)))
                if distance < min_distance:
                    min_distance = distance
            total_cost = total_cost + house.cost_function(min_distance)
        return total_cost
