import matplotlib.pyplot as plt
import csv
from matplotlib.patches import Rectangle, Patch


WIDTH_MAX  = 180
HEIGHT_MAX = 160

# Function that makes visualisations of an excel file
def visualisation(output):

    # Open the excel file with the coordinates of the houses and waters
    datapoints = []
    with open(output, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            datapoints.append(row)

    # Make a figure with the houses and the water
    fig, ax = plt.subplots()
    for row in datapoints[1:len(datapoints)-1]:

        # Read the coordinates from the excel file
        bottom_left = row[1].split(',')
        bottom_right = row[2].split(',')
        top_right = row[3].split(',')
        top_left = row[4].split(',')
        type_house = row[5].strip()
        color_dict = {'MAISON': 'brown', 'BUNGALOW': 'yellow', 'EENGEZINSWONING': 'grey', 'WATER': 'blue'}
        house_color = ''
        patch_list = []

        # Make the legend
        for key,value in color_dict.items():
            legend_key = Patch(color = color_dict[key], label=key)
            patch_list.append(legend_key)
            if key == type_house:
                house_color = value

        # Add the houses to the map
        ax.add_patch(Rectangle((int(bottom_left[0]), int(bottom_left[1])), int(bottom_right[0]) - int(bottom_left[0]),
                int(top_left[1]) - int(bottom_left[1]), facecolor = house_color))

    # Add the atributes to the graph
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height * 0.7])
    plt.title('Amstelhaege', fontsize=20)
    plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", handles = patch_list)
    plt.xlim(0, WIDTH_MAX)
    plt.ylim(0, HEIGHT_MAX)
    plt.savefig('visualisation.png',)
