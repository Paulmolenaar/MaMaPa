from  code.classes.models import House, Water, Map
import csv
from code.visualisation.visualize import visualisation
from  code.algorithms.hillclimbing import HillClimber

if __name__ == "__main__":

    amount_of_houses = 20
    test_kaart = Map('docs/wijk_1.csv', amount_of_houses)
    row_list = []


    for i in test_kaart.all_waters:
        test_kaart.all_waters[i].corners()
        water = test_kaart.all_waters[i]
        row_list.append([f"{water.type}_{water.id}", f"{water.bottom_left[0]},{water.bottom_left[1]}", f"{water.bottom_right[0]},{water.bottom_right[1]}", f"{water.top_right[0]},{water.top_right[1]}", f"{water.top_left[0]},{water.top_left[1]}" ,water.type.upper()])

    a = int(test_kaart.total_costs)
    print(a)
    b = HillClimber(test_kaart)
    test_kaart = b.run(100)
    a = b.value
    print(a)
    
    for j in test_kaart.all_houses:
        house = test_kaart.all_houses[j]
        row_list.append([f"{house.type}_{house.id}", f"{house.bottom_left[0]},{house.bottom_left[1]}", f"{house.bottom_right[0]},{house.bottom_right[1]}", f"{house.top_right[0]},{house.top_right[1]}", f"{house.top_left[0]},{house.top_left[1]}" ,house.type.upper()])
        
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["structure", "corner_1", "corner_2","corner_3","corner_4","type"])
        for j in row_list:
            writer.writerow(j)
        writer.writerow(["networth", a])

    visualisation('output.csv')
