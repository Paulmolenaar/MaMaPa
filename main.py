from  code.classes.models import House, Water, Map
import csv
from code.visualisation.visualize import visualisation

if __name__ == "__main__":

    amount_of_houses = 6
    test_kaart = Map('docs/wijk_1.csv', amount_of_houses)
    row_list = []


    for i in test_kaart.all_waters:
        test_kaart.all_waters[i].corners()
        water = test_kaart.all_waters[i]
        row_list.append([f"{water.type}_{water.id}", water.bottom_left, water.bottom_right, water.top_right, water.top_left ,water.type.upper()])

    for j in test_kaart.all_houses:
        house = test_kaart.all_houses[j]
        row_list.append([f"{house.type}_{house.id}", house.bottom_left, house.bottom_right, house.top_right, house.top_left, house.type.upper()])

    print(test_kaart.total_costs)

    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["structure", "corner_1", "corner_2","corner_3","corner_4","type"])
        for j in row_list:
            writer.writerow(j)
        writer.writerow(["networth", "0"])

    visualisation('output.csv')
