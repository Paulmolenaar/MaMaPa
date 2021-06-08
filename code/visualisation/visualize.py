import matplotlib.pyplot as plt
import csv
from matplotlib.patches import Rectangle, Patch


WIDTH_MAX  = 80 
HEIGHT_MAX = 80

def visualisation(output):
    datapoints = []
    with open(output, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            datapoints.append(row)

    fig, ax = plt.subplots()


    for row in datapoints[1:len(datapoints)-1]:
        bottom_left = row[1].split(',')
        bottom_right = row[2].split(',')
        top_right = row[3].split(',')
        top_left = row[4].split(',')
        type_house = row[5].strip()
        color_dict = {'MAISON': 'brown', 'BUNGALOW': 'yellow', 'EENGEZINSWONING': 'grey', 'WATER': 'blue'}
        house_color = ''
        patch_list = []
        for key,value in color_dict.items(): 
            legend_key = Patch(color = color_dict[key], label=key)
            patch_list.append(legend_key)
            if key == type_house:
                house_color = value
        ax.add_patch(Rectangle((int(bottom_left[0]), int(bottom_left[1])), int(bottom_right[0]) - int(bottom_left[0]),
                int(top_left[1]) - int(bottom_left[1]), facecolor = house_color))

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    plt.title('Amstelhaege', fontsize=20)
    plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", handles = patch_list)
    plt.xlim(0, WIDTH_MAX)
    plt.ylim(0, HEIGHT_MAX)
    plt.savefig('visualisation.png',)
