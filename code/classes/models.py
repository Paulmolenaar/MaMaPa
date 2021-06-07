import csv
import random

class House():
    def __init__(self, type, uid, length , width , bottom_left, min_distance):
        self.type = type
        self.id = uid
        self.value = 0
        self.length = length
        self.width = width
        self.bottom_left = bottom_left
        self.bottom_right = 0
        self.top_left = 0
        self.top_right = 0
        self.neighbours = {}
        self.cost = 0
        self.distance = 0
        self.coordinates = self.coordinates(bottom_left)

    def coordinates(self, bottom_left):
        # generates the remaining coordinates
        self.bottom_left = bottom_left
        x = self.bottom_left.split(",")
        self.bottom_right = str(int(x[0]) + int(self.width)) + ',' + x[1]
        self.top_left = x[0] + ',' + str(int(x[1]) + self.length)
        self.top_right = str(int(x[0]) + self.width) + ',' + str(int(x[1]) + self.length)

    def cost_function(self, min_distance):
        # Generates the costs per house
        self.distance = min_distance
        if self.type =='MAISON':
            self.cost = 610000 * (1 + (0.06 * (self.distance-6)))
        if self.type =='EENGEZINSWONING':
            self.cost = 285000 * (1 + (0.03 * (self.distance-2)))
        if self.type =='BUNGALOW':
            self.cost = 399000 * (1 + (0.04 * (self.distance-3)))


class Water():
    def __init__(self, type, uid, bottom_left, top_right):
        self.type = type
        self.id = uid
        self.bottom_left = bottom_left
        self.bottom_right = 0
        self.top_left = 0
        self.top_right = top_right

    def corners(self):
        x = self.bottom_left.split(",")
        #50,44
        y = self.top_right.split(",")
        #130,116
        width = int(y[0]) - int(x[0])
        height = int(y[1]) - int(x[1])
        self.bottom_right = f"{int(x[0]) + width},{int(x[1])}"
        self.top_left = f"{int(x[0])},{int(x[1]) + height}"
        return 1


class Map():
    def __init__(self, source_file, number_of_houses):
        self.all_houses = self.make_houses(number_of_houses)
        self.all_waters = self.load_water(source_file)

    def load_water(self, source_file):
        waters = {}
        with open(source_file, 'r') as in_file:
            reader = csv.DictReader(in_file)
            line = 0
            for row in reader:
                waters[line] = Water("water", line+1, row['bottom_left_xy'], row['top_right_xy'])
                line = line + 1

        return waters

    def make_houses(self, number_of_houses):
         houses = {}
         width_dict =	{"maisons": 12,"bungalows": 11,"eengezinswoning": 8}
         height_dict =	{"maisons": 10,"bungalows": 7,"eengezinswoning": 8}
         amount_maisons = int(0.15 * number_of_houses)
         amount_bungalows = int(0.25 * number_of_houses)
         amount_eengezinswoning = int(0.60 * number_of_houses)
         types_of_houses = []
         for i in range(amount_maisons):
             types_of_houses.append("maisons")
         for j in range(amount_bungalows):
             types_of_houses.append("bungalows")
         for k in range(amount_eengezinswoning):
             types_of_houses.append("eengezinswoning")
         teller = 0
         for x in types_of_houses:
             height = height_dict.get(x)
             width = width_dict.get(x)
             if x == 'eengezinswoning':
                 id_house = amount_eengezinswoning
                 amount_eengezinswoning = amount_eengezinswoning -1
             if x == 'bungalows':
                 id_house = amount_bungalows
                 amount_bungalows = amount_bungalows -1
             if x == 'maisons':
                 id_house = amount_maisons
                 amount_maisons = amount_maisons -1
             x_bottomleft = random.randint(0,(180 - width))
             y_bottomleft = random.randint(0,(160 - height))
             houses[teller] = House(x, id_house, height, width, str(x_bottomleft) + ',' + str(y_bottomleft), 0)
             teller = teller + 1
         return houses
