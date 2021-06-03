from  code.classes.models import House, water
import csv
from code.visualisation.visualize import visualisation

if __name__ == "__main__":

    all_waters = water.load_water('docs/wijk_1.csv')
    row_list = []
    amount_of_houses = 20



    for i in all_waters:
        all_waters[i].corners()
        row_list.append([f"{all_waters[i].type}_{all_waters[i].id}", all_waters[i].bottom_left, all_waters[i].bottom_right, all_waters[i].top_right, all_waters[i].top_left ,all_waters[i].type.upper()])

    ## Creating 3 houses
    row_list.append(["eengezinswoning_1", "40,121", "32,121", "32,129", "40,129", "EENGEZINSWONING"])
    row_list.append(["maison_12", "32,74", "32,64", "44,64", "44,74", "MAISON"])
    row_list.append(["bungalow_1", "10,32", "3,32", "3,43", "10,43", "BUNGALOW"])

    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["structure", "corner_1", "corner_2","corner_3","corner_4","type"])
        for j in row_list:
            writer.writerow(j)
        writer.writerow(["networth", "0"])

    visualisation('output.csv')
