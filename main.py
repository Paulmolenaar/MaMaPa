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
        print(house.bottom_left)

    ## Creating 3 houses "40,121", "32,121", "32,129", "40,129"
    row_list.append(["eengezinswoning_1", "32,121", "40,121", "40,129", "32,129", "EENGEZINSWONING"])
    row_list.append(["maison_12", "32,64", "44,64", "44,74", "32,72", "MAISON"]) 
    row_list.append(["bungalow_1", "3,32", "10,32", "10,43", "3,43", "BUNGALOW"])

    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["structure", "corner_1", "corner_2","corner_3","corner_4","type"])
        for j in row_list:
            writer.writerow(j)
        writer.writerow(["networth", "0"])

    visualisation('output.csv')
