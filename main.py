from  code.classes.models import House, water 
import csv

if __name__ == "__main__":

    all_waters = water.load_water('docs/wijk_1.csv')
    row_list = []

    for i in all_waters:
        all_waters[i].corners()
        row_list.append([f"{all_waters[i].type}_{all_waters[i].id}", all_waters[i].bottom_left, all_waters[i].bottom_right, all_waters[i].top_right, all_waters[i].top_left ,all_waters[i].type.upper()])
    
    print(row_list)

    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["structure", "corner_1", "corner_2","corner_3","corner_4","type"])
        for j in row_list:
            writer.writerow(j)
        writer.writerow(["networth", "0"])
