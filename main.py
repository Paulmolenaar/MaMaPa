from  code.classes.models import Map
import csv
from code.visualisation.visualize import visualisation
from  code.algorithms.hillclimbing import HillClimber
# to debug total duration of optimization
import time

if __name__ == "__main__":


    def current_milli_time():
        return round(time.time() * 1000)

    amount_of_houses = 40
    row_list = []

    # Import the waters and add them to the map and the list for the excel file
    map = Map('docs/wijk_2.csv', amount_of_houses)
    for i in map.all_waters:
        map.all_waters[i].corners()
        water = map.all_waters[i]
        row_list.append([f"{water.type}_{water.id}", f"{water.bottom_left[0]}, {water.bottom_left[1]}",
                f"{water.bottom_right[0]},{water.bottom_right[1]}", f"{water.top_right[0]},{water.top_right[1]}",
                f"{water.top_left[0]},{water.top_left[1]}" ,water.type.upper()])


    # Print the solution of the first map and then run the hill climber and print that solution
    firstTime = current_milli_time()
    first_solution = int(map.total_costs)
    print('Random solution: ', first_solution)
    hillclimb = HillClimber(map)
    map = hillclimb.run(100, mutate_houses_number=1)
    better_solution = hillclimb.value
    print('Algoritm solution: ', better_solution)

    timeDifference = current_milli_time() - firstTime
    print ('Time: ', str(timeDifference)+" ms")

    # Add the houses to the list for the excel file
    for j in map.all_houses:
        house = map.all_houses[j]
        row_list.append([f"{house.type}_{house.id}", f"{house.bottom_left[0]},{house.bottom_left[1]}",
                f"{house.bottom_right[0]},{house.bottom_right[1]}", f"{house.top_right[0]},{house.top_right[1]}",
                f"{house.top_left[0]},{house.top_left[1]}" ,house.type.upper()])

    # Make an excel file with the locations of the houses and water
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["structure", "corner_1", "corner_2","corner_3","corner_4","type"])
        for j in row_list:
            writer.writerow(j)
        writer.writerow(["networth", better_solution])

    # Make the visualistions
    visualisation('output.csv')
