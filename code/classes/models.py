import csv
import random
import math

WIDTH_MAX  = 180
HEIGHT_MAX = 160
random.seed(1243546)
class House():

    # The house class calculates the atributes of hte houses passed on to this class
    def __init__(self):
        self.neighbours = []

    # Calulates the coordinates of the corners of the houses
    def to_coordinates(self, bottom_left):
        # generates the remaining coordinates
        self.bottom_right = [bottom_left[0] + self.width, bottom_left[1]]
        self.top_left = [bottom_left[0] , bottom_left[1] + self.length]
        self.top_right = [bottom_left[0] + self.width, bottom_left[1] + self.length]

    # Calculates the costs of the houses
    def cost_function(self, free_meters):
        self.cost = self.min_cost * (1 + (self.percent_increase * (free_meters-self.min_distance)))
        return self.cost

    # Caclulates if the house itersects with another house
    def intersect(self, other):

        # Checks if the house overlaps with water or with another house
        if other.type == "water":
            min_distance = 0

        else:
            min_distance = max(self.min_distance, other.min_distance)

        # Checks if a house overlaps with another house on the map
        to_the_right = self.bottom_left[0] - min_distance >= other.top_right[0]
        to_the_left = other.bottom_left[0] >= self.top_right[0] + min_distance
        if (to_the_right or to_the_left):
            return False

        above_other = self.bottom_left[1] - min_distance >= other.top_right[1]
        below_other = other.bottom_left[1] >= self.top_right[1] + min_distance

        # Return false if no intersect with another house, else true
        if(above_other or below_other):
            return False

        return True

    # Make random coordinates for a house
    def random_location(self):
        self.bottom_left = [random.randint(0 + self.min_distance,(WIDTH_MAX - self.width - self.min_distance)),random.randint(0 + self.min_distance,(HEIGHT_MAX - self.length - self.min_distance))]
        self.coordinates = self.to_coordinates(self.bottom_left)

    # Make the coordinates for a house when it gets rotated
    def rotate(self,all_waters):

        # Calculate the new bottom left corner of the houses
        offset = int(abs(self.width - self.length) / 2)
        self.bottom_left[0] = self.bottom_left[0] + int(offset/2)
        self.bottom_left[1] = self.bottom_left[1] - int(offset/2)

        # Get the new coordinates of the house
        temp_width  = self.width
        self.width  = self.length
        self.length = temp_width
        self.coordinates = self.to_coordinates(self.bottom_left)

        # CHeck if rotated house is on the map
        if (self.bottom_left[0] < 0 or self.bottom_left[0] + self.width > WIDTH_MAX):
            return False

        if (self.bottom_left[1] < 0 or self.bottom_left[1] + self.length > HEIGHT_MAX):
            return False

        # Check if the rotated house intersects with water or another house
        for j in range(0, len(all_waters)):
            water = all_waters[j]
            if (self.intersect(water)):
                return False

        for i in range(0, len(self.neighbours)):
            other_house = self.neighbours[i]
            if (self.intersect(other_house)):
                return False

        return True

    # Checks the if there is enough free space on the map
    def check_distance(self):
        if self.bottom_right[0] + self.min_distance > WIDTH_MAX or self.top_left[1] + self.min_distance > HEIGHT_MAX or self.bottom_left[0] - self.min_distance < 0 or self.bottom_left[1] - self.min_distance < 0:
            return True
        else:
            return False

class Maison(House):

    # This is the class for maisons and sets the initial parameters
    def __init__(self, uid):
        self.type = "maison"
        self.id = uid
        self.min_distance = 6
        self.length = 10
        self.width = 12
        self.min_cost = 610000
        self.percent_increase = 0.06
        self.random_location()


class Bungalow(House):

    # This is the class for bungalows and sets the initial parameters
    def __init__(self, uid):
        self.type = "bungalow"
        self.id = uid
        self.min_distance = 3
        self.length = 7
        self.width  = 11
        self.cost = 0
        self.min_cost = 399000
        self.percent_increase = 0.04
        self.random_location()


class Eengezinswoning(House):

    # This is the class for eengezinswoningen and sets the initial parameters
    def __init__(self, uid):
        self.type = "eengezinswoning"
        self.id = uid
        self.min_distance = 2
        self.length = 8
        self.width = 8
        self.cost = 0
        self.min_cost = 285000
        self.percent_increase = 0.03
        self.random_location()

class Water():

    # The class for water. First set the initial parameters
    def __init__(self, type, uid, bottom_left, top_right):
        self.type = type
        self.id = uid
        self.bottom_left = bottom_left
        self.bottom_right = 0
        self.top_left = 0
        self.top_right = top_right

    # Calculate the coordinates of the corners of the water
    def corners(self):
        width = self.top_right[0]- self.bottom_left[0]
        height = self.top_right[1] - self.bottom_left[1]
        self.bottom_right = [self.bottom_left[0] + width,self.bottom_left[1]]
        self.top_left = [self.bottom_left[0],self.bottom_left[1] + height]
        return 1


class Map():

    # This class makes te total map of the houses and waters, first load the houses and the waters
    def __init__(self, source_file, number_of_houses):
        self.all_waters = self.load_water(source_file)
        self.all_houses = self.make_houses(number_of_houses)
        self.total_costs = self.total_cost()

    # Load in all the waters.
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

    # Make all the houses
    def make_houses(self, number_of_houses):
         houses = {}

         # Determine the amount of each house
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

         # Create every house
         counter = 0
         for x in types_of_houses:
             if x == 'eengezinswoning':
                 id_house = amount_eengezinswoning
                 amount_eengezinswoning = amount_eengezinswoning - 1
             if x == 'bungalow':
                 id_house = amount_bungalows
                 amount_bungalows = amount_bungalows - 1
             if x == 'maison':
                 id_house = amount_maisons
                 amount_maisons = amount_maisons - 1

             # Make a house and check if it overlaps with another house or water, if it overlaps, make the house again
             intersect = True
             while intersect == True:
                if x == 'eengezinswoning':
                    houses[counter] = Eengezinswoning(id_house)

                if x == 'bungalow':
                    houses[counter] = Bungalow(id_house)

                if x == 'maison':
                    houses[counter] = Maison(id_house)

                for j in range(0, len(self.all_waters)):
                    water = self.all_waters[j]
                    intersect = houses[counter].intersect(water)
                    if intersect == True:
                        break

                if intersect == False:
                    for i in range(0, counter):
                        intersect = houses[counter].intersect(houses[i])

                        if intersect == True:
                            break

             counter = counter + 1

         return houses

    # Determine the costs of all the houses and its free space
    def total_cost(self, test = False):

        # Iterate over all the houses and find the closest house
        total_cost = 0
        for j in range(0, len(self.all_houses)):
            min_distance = 180
            distance = 0
            house = self.all_houses[j]

            self.all_houses[j].neighbours = []

            # Iterate over the the other houses and calculate the smallest distance
            for i in range(0, len(self.all_houses)):
                other_house = self.all_houses[i]

                if i == j:
                    continue

                # Calculate the position and the distance of the house and use this if it is the smallest distance
                right,left,above,under = self.determine_direction(house,other_house)
                distance = self.determine_distance(right,left,above,under,house,other_house)

                if (distance < 10):
                    self.all_houses[j].neighbours.append(other_house)

                if distance < min_distance:
                    min_distance = distance

            # Calculate the total costs
            cost_house  = house.cost_function(min_distance)
            total_cost = total_cost + cost_house 
        return round(total_cost)

    # Determine in which direction two houses are from each other
    def determine_direction(self,house, other_house):
        right = house.bottom_left[0] > other_house.top_right[0]
        left = house.top_right[0] < other_house.bottom_left[0]
        above = house.bottom_left[1] > other_house.top_right[1]
        under = house.top_right[1] < other_house.bottom_left[1]

        return right,left,above,under

    # Calculate the distance between two houses
    def determine_distance(self, right,left,above,under , house, other_house):


        # Based on the position of the houses, the distance is calculated by pythagoras or just the absolute distance
        if right:
            distance = house.bottom_left[0] - other_house.top_right[0]

        if left:
            distance = other_house.bottom_left[0] - house.top_right[0]

        if above:
            distance = house.bottom_left[1] - other_house.top_right[1]

        if under:
            distance = other_house.bottom_left[1] - house.top_right[1]

        if left and above:
            distance = math.floor(math.sqrt(((house.top_right[0] - other_house.bottom_left[0]) ** 2) +
                ((house.bottom_left[1] - other_house.top_right[1]) ** 2)))

        if right and above:
            distance = math.floor(math.sqrt(((house.bottom_left[0] - other_house.top_right[0]) ** 2) +
                ((house.bottom_left[1] - other_house.top_right[1]) ** 2)))


        if left and under:
            distance = math.floor(math.sqrt(((other_house.bottom_left[0] - house.top_right[0]) ** 2) +
                ((house.top_right[1] - other_house.bottom_left[1]) ** 2)))

        if right and under:
            distance = math.floor(math.sqrt(((house.bottom_left[0] - other_house.top_right[0]) ** 2) +
                ((house.top_right[1] - other_house.bottom_left[1]) ** 2)))

        return distance
