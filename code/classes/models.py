import csv

class House():
    def __init__(self, type, uid, length , width , bottom_left):
        self.type = type
        self.id = uid
        self.value = 0
        self.length = length
        self.width = width
        self.bottom_left = 0
        self.bottom_right = 0
        self.top_left = 0
        self.top_right = 0
        self.neighbours = {}

    def coordinates(self, bottom_left):
        # generates the remaining coordinates 
        self.bottom_left = bottom_left 
        self.bottom_right = ((bottom_left[0] + self.width), bottom_left[1])
        self.top_left = (bottom_left[0], (bottom_left[1] + self.length))
        self.top_right = ((bottom_left[0] + self.width), (bottom_left[1] + self.length))

class water():
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
    def __init__(self, source_file):
        self.all_houses = {}
        self.all_waters = self.load_water(source_file)

    def load_water(self, source_file):
        waters = {}
        with open(source_file, 'r') as in_file:
            reader = csv.DictReader(in_file)
            line = 0
            for row in reader:
                waters[line] = water("water", line+1, row['bottom_left_xy'], row['top_right_xy'])
                line = line + 1

        return waters
