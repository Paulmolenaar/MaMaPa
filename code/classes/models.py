import csv
import random

WIDTH_MAX  = 80
HEIGHT_MAX = 80

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
        x = self.bottom_left.split(",")
        self.bottom_right = str(int(x[0]) + int(self.width)) + ',' + x[1]
        self.top_left = x[0] + ',' + str(int(x[1]) + self.length)
        self.top_right = str(int(x[0]) + self.width) + ',' + str(int(x[1]) + self.length)

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
        bottom_left = self.bottom_left.split(",")
        top_right = self.top_right.split(",")
        other_bottom_left = other.bottom_left.split(",")
        other_top_right = other.top_right.split(",")
        
        if water:
            min_distance = 0
        else:
            min_distance = max(self.min_distance, other.min_distance)

        test1 = (int(bottom_left[0]) - min_distance) >= int(other_top_right[0])
        test2 = int(other_bottom_left[0]) >= (int(top_right[0]) + min_distance)
        if ( test1 or test2):
            return False
        
        test1 = (int(bottom_left[1]) - min_distance) >= int(other_top_right[1])
        test2 = int(other_bottom_left[1]) >= (int(top_right[1]) + min_distance)
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
        self.all_waters = self.load_water(source_file)
        self.all_houses = self.make_houses(number_of_houses)
        self.total_costs = self.total_cost()

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
         width_dict =	{"maison": 12,"bungalow": 11,"eengezinswoning": 8}
         height_dict =	{"maison": 10,"bungalow": 7,"eengezinswoning": 8}
         min_distance_dict = {"maison": 6,"bungalow": 3,"eengezinswoning": 2}
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
                houses[teller] = House(x, id_house, height, width, str(x_bottomleft) + ',' + str(y_bottomleft), min_distance)
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
            house = house[1]
            
            orig_length = house.length
            orig_width  = house.width
            min_count   = WIDTH_MAX

            for other_house in self.all_houses.items():
                if other_house == house:
                    continue

                temp_house  = House(house.type, house.id, orig_length, orig_width,
                                house.bottom_left, house.min_distance)

                other_house = other_house[1]
                count = 0
                while temp_house.intersect(other_house, True) == False:
                    x      = house.bottom_left.split(',')

                    count  = count + 1
                    length = temp_house.length + 2
                    width  = temp_house.width + 2

                    x[0] = int(x[0]) - count
                    x[1] = int(x[1]) - count
                    
                    temp_house = House(house.type, house.id, length, width,
                                    str(x[0]) + ',' + str(x[1]), house.min_distance)

                    # check if left bottom coords hit left/bottom side of map, check if right top coords hit right/top side of map
                    if (x[0] <= 0 or x[1] <= 0) or (x[0] + temp_house.width >= WIDTH_MAX or x[1] + temp_house.length >= HEIGHT_MAX):
                        break

                if  0 < count and count < min_count:
                    min_count = count
            DEBUG_housenr = DEBUG_housenr + 1
            print ("("+str(DEBUG_housenr)+")"+str(house.type) + ": " + str(house.min_distance)+"\n")
            total_cost = total_cost + house.cost_function(min_count - 1)
        return total_cost
