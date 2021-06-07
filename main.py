from  code.classes.models import House, Water, Map
import csv
from code.visualisation.visualize import visualisation

if __name__ == "__main__":

    amount_of_houses = 20
    test_kaart = Map('docs/wijk_1.csv', amount_of_houses)
    row_list = []


    for i in test_kaart.all_waters:
        test_kaart.all_waters[i].corners()
        water = test_kaart.all_waters[i]
        row_list.append([f"{water.type}_{water.id}", water.bottom_left, water.bottom_right, water.top_right, water.top_left ,water.type.upper()])

    for j in test_kaart.all_houses:
        house = test_kaart.all_houses[j]
        row_list.append([f"{house.type}_{house.id}", house.bottom_left, house.bottom_right, house.top_right, house.top_left, house.type.upper()])

    total_cost = 0
    for house in test_kaart.all_houses.items():
        house = house[1]
        temp_house = House(house.type, house.id, house.length, house.width,
                        house.bottom_left, 0)
        print(house.type + 'begin')
        min_count = 100
        for house1 in test_kaart.all_houses.items():
            house1 = house1[1]
            count = 0
            while temp_house.intersect(house1, True) == False:
                count = count + 1
                house.length = house.length + 2
                house.width = house.width + 2
                x = house.bottom_left.split(',')
                temp_house = House(house.type, house.id, house.length, house.width,
                                str(int(x[0]) - count) + ',' + str(int(x[1]) - count), 0)
            print(count)
            print(house1.type)
            if 0 < count and count < min_count:
                min_count = count
        total_cost = total_cost + house.cost_function(min_count)


    print(total_cost)
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["structure", "corner_1", "corner_2","corner_3","corner_4","type"])
        for j in row_list:
            writer.writerow(j)
        writer.writerow(["networth", "0"])

    visualisation('output.csv')
