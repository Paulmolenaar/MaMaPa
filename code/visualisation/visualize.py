import matplotlib.pyplot as plt
import csv
from matplotlib.patches import Rectangle

WIDTH_MAX = 180
HEIGHT_MAX = 160

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
        house_color = ''
        if type_house == 'WATER':
            house_color = 'blue'
        elif type_house == 'EENGEZINSWONING':
            house_color = 'grey'
        elif type_house == 'BUNGALOW':
            house_color = 'yellow'
        elif type_house == 'MAISON':
            house_color = 'brown'
        ax.add_patch(Rectangle((int(bottom_left[0]), int(bottom_left[1])), int(bottom_right[1]) - int(bottom_left[1]),
                int(top_left[0]) - int(bottom_left[0]), facecolor = house_color, label = type_house))
                
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    plt.title('Amstelhaege', fontsize=20) 
    plt.legend(bbox_to_anchor=(1, 0.5), loc="center left")
    plt.xlim(0, WIDTH_MAX)
    plt.ylim(0, HEIGHT_MAX)
    plt.savefig('visualisation.png',)
