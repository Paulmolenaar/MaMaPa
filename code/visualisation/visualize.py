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
        ax.add_patch(Rectangle((int(bottom_left[0]), int(bottom_left[1])), int(bottom_right[1]) - int(bottom_left[1]),
                        int(top_left[0]) - int(bottom_left[0])))

    plt.title('Amstelhaege', fontsize=20)
    plt.xlim(0,180)
    plt.ylim(0,160)
    plt.savefig('visualisation.png')
