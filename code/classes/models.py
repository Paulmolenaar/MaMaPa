import csv
import random
import math

WIDTH_MAX  = 180
HEIGHT_MAX = 160
# random.seed(12)
class House():
    def __init__(self):
        pass
    def coordinates(self, bottom_left):
        # generates the remaining coordinates
        self.bottom_right = [bottom_left[0] + self.width, bottom_left[1]]
        self.top_left = [bottom_left[0] , bottom_left[1] + self.length]
        self.top_right = [bottom_left[0] + self.width, bottom_left[1] + self.length]
        
    def cost_function(self, free_meters):
        self.cost = self.min_cost * (1 + (self.percent_increase * (free_meters-self.min_distance)))
        return self.cost


    def intersect(self, other):
        if other.type == "water":
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
    
class Maison(House):
    def __init__(self, uid):
        self.type = "maison"
        self.id = uid
        self.min_distance = 6
        self.length = 10
        self.width = 12
        self.bottom_left = [random.randint(0 + self.min_distance,(WIDTH_MAX - self.width - self.min_distance)),random.randint(0 + self.min_distance,(HEIGHT_MAX - self.length - self.min_distance))]
        self.min_cost = 610000 
        self.percent_increase = 0.06
        self.coordinates = self.coordinates(self.bottom_left)
        
        
class Bungalow(House):
    def __init__(self, uid):
        self.type = "bungalow"
        self.id = uid
        self.min_distance = 3
        self.length = 7
        self.width = 11
        self.bottom_left = [random.randint(0 + self.min_distance,(WIDTH_MAX - self.width - self.min_distance)),random.randint(0 + self.min_distance,(HEIGHT_MAX - self.length - self.min_distance))]
        self.cost = 0
        self.min_cost = 399000 
        self.percent_increase = 0.04
        self.coordinates = self.coordinates(self.bottom_left)
        
        
class Eengezinswoning(House):
    def __init__(self, uid):
        self.type = "eengezinswoning"
        self.id = uid
        self.min_distance = 2
        self.length = 8
        self.width = 8
        self.bottom_left = [random.randint(0 + self.min_distance,(WIDTH_MAX - self.width - self.min_distance)),random.randint(0 + self.min_distance,(HEIGHT_MAX - self.length - self.min_distance))]
        self.cost = 0
        self.min_cost = 285000
        self.percent_increase = 0.03
        self.coordinates = self.coordinates(self.bottom_left)

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
                trxy = list(map(int, row['top_right_xy'].split(",")))
                waters[line] = Water("water", line+1, blxy, trxy)
                line = line + 1

        return waters

    def make_houses(self, number_of_houses):
         houses = {}
         amount_maisons = int(0.15 * number_of_houses)
         amount_bungalows = int(0.25 * number_of_houses)
         amount_eengezinswoning = int(0.60 * number_of_houses)
         types_of_houses = []
         for i in range(amount_maisons):
             types_of_houses.append("maison")
         for j in range(amount_bungalows):
             types_of_houses.append("bungalow")
         for k in range(amount_eengezinswoning):
             types_of_houses.append("eengezinswoning")
         teller = 0
         for x in types_of_houses:
             if x == 'eengezinswoning':
                 id_house = amount_eengezinswoning
                 amount_eengezinswoning = amount_eengezinswoning -1
             if x == 'bungalow':
                 id_house = amount_bungalows
                 amount_bungalows = amount_bungalows -1
             if x == 'maison':
                 id_house = amount_maisons
                 amount_maisons = amount_maisons -1
             intersect = True
             while intersect == True:
                if x == 'eengezinswoning':
                    houses[teller] = Eengezinswoning(id_house)
                if x == 'bungalow':
                    houses[teller] = Bungalow(id_house)
                if x == 'maison':
                    houses[teller] = Maison(id_house)
                for j in range(0, len(self.all_waters)):
                    water = self.all_waters[j]
                    intersect = houses[teller].intersect(water)
                    if intersect == True:
                        break
                if intersect == False:
                    for i in range(0, teller):
                        intersect = houses[teller].intersect(houses[i])
                        if intersect == True:
                            break
             teller = teller + 1
         return houses

    def total_cost(self, test = False):
        total_cost = 0
        for j in range(0, len(self.all_houses)):
            min_distance = 180
            distance = 0
            house = self.all_houses[j]
            tempdict=house.__dict__  
            for i in range(0, len(self.all_houses)):
                other_house = self.all_houses[i]
                tempdict2=other_house.__dict__
                if i == j:
                    continue
                rechts,links,boven,onder = self.determine_direction(house,other_house)
                distance = self.determine_distance(rechts,links,boven,onder,house,other_house)
                if distance < min_distance:
                    min_distance = distance
            a = house.cost_function(min_distance)
            total_cost = total_cost + a
        return round(total_cost)
    
    def determine_direction(self,house, other_house):
        rechts = house.bottom_left[0] > other_house.top_right[0]
        links = house.top_right[0] < other_house.bottom_left[0]
        boven = house.bottom_left[1] > other_house.top_right[1]
        onder = house.top_right[1] < other_house.bottom_left[1]
        return rechts,links,boven,onder
    
    def determine_distance(self, rechts,links,boven,onder , house, other_house):
        if rechts:
            distance = house.bottom_left[0] - other_house.top_right[0]
        if links:
            distance = other_house.bottom_left[0] - house.top_right[0]
        if boven:
            distance = house.bottom_left[1] - other_house.top_right[1]
        if onder: 
            distance = other_house.bottom_left[1] - house.top_right[1]
        if links and boven:
            distance = math.floor(math.sqrt(((house.top_right[0] - other_house.bottom_left[0]) ** 2) + ((house.bottom_left[1] - other_house.top_right[1]) ** 2)))
        if rechts and boven:
            distance = math.floor(math.sqrt(((house.bottom_left[0] - other_house.top_right[0]) ** 2) + ((house.bottom_left[1] - other_house.top_right[1]) ** 2)))
        if links and onder:
            a = other_house.bottom_left[0] - house.top_right[0]
            b = house.top_right[1] - other_house.bottom_left[1] 
            a = a ** 2
            b = b ** 2
            distance = math.sqrt(a + b)
            distance = math.floor(distance)
        if rechts and onder:
            distance = math.floor(math.sqrt(((house.bottom_left[0] - other_house.top_right[0]) ** 2) + ((house.top_right[1] - other_house.bottom_left[1]) ** 2)))
        return distance