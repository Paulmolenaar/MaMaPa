import matplotlib.pyplot as plt
import csv
from matplotlib.patches import Rectangle

def visualisation(output):
    datapoints = []
    with open(output, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            datapoints.append(row)

    fig, ax = plt.subplots()

    for row in datapoints[1:len(datapoints)-1]:
        bottom_left = row[1].split(',')
        top_left = row[2].split(',')
        top_right = row[3].split(',')
        bottom_right = row[4].split(',')
        type_house = row[5].strip()
        if type_house == 'WATER':
            ax.add_patch(Rectangle((int(bottom_left[0]), int(bottom_left[1])), int(bottom_right[1]) - int(bottom_left[1]),
                            int(top_left[0]) - int(bottom_left[0]), facecolor = 'blue'))
        elif type_house == 'EENGEZINSWONING':
            ax.add_patch(Rectangle((int(bottom_left[0]), int(bottom_left[1])), int(bottom_right[1]) - int(bottom_left[1]),
                            int(top_left[0]) - int(bottom_left[0]), facecolor = 'red'))
        elif type_house == 'BUNGALOW':
            ax.add_patch(Rectangle((int(bottom_left[0]), int(bottom_left[1])), int(bottom_right[1]) - int(bottom_left[1]),
                            int(top_left[0]) - int(bottom_left[0]), facecolor = 'green'))
        elif type_house == 'MAISON':
            ax.add_patch(Rectangle((int(bottom_left[0]), int(bottom_left[1])), int(bottom_right[1]) - int(bottom_left[1]),
                            int(top_left[0]) - int(bottom_left[0]), facecolor = 'brown'))



    plt.title('Amstelhaege', fontsize=20)
    plt.xlim(0,180)
    plt.ylim(0,160)
    plt.savefig('visualisation.png')
