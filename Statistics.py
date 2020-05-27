__author__ = "verrecchia"
__file__ = "Statistics"
__date__ = "20/02/20"

import csv
import os


def extract_height(csv_name) :
    file = open(csv_name, "r")
    reader = csv.reader(file)
    extracted = [column[1] for column in reader ]
    file.close()
    return extracted[1]

def extract_width(csv_name) :
    file = open(csv_name, "r")
    reader = csv.reader(file)
    extracted = [column[2] for column in reader]
    file.close()
    return extracted[1]


def opening(csv_name) :
    "Extract the seed, size of the grid and pc for each grid from the csv file"
    file = open(csv_name,"r")
    reader = csv.reader(file)
    seed = []
    height = extract_height(csv_name)
    width = extract_width(csv_name)
    pc = []
    for row in reader :
        pc += [row[3]]
        seed += [row[0]]
    file.close()
    return(seed,height,width,pc)

def mean_value_percolation_rate(opened) :
    """
    :param opened: The output of the function opening
    :return:  The size of the matrix / The mean Pc / The percolation rate / the (min,max) value
    """
    sum = 0
    number_percolation = 0
    max = 0
    min = float("inf")
    for i in range(1,len(opened[3])) :
        value = float(opened[3][i])
        if value != -1 :
            sum += value
            if value < min :
                min = value
            if value > max :
                max = value
        else :
            number_percolation += 1
    return ((opened[1], opened[2]) , (sum / ( len(opened[3]) - 1 - number_percolation )),
            number_percolation/( len(opened[3]) - 1), (min,max))

def saving_stat(csv_name_in, csv_name_out) :
    """
    :param stat: The output of the function mean_value_percolation_rate
    Save the results in a csv
    """
    opened = opening(csv_name_in)
    stat = mean_value_percolation_rate(opened)
    file = open(csv_name_out, "a")
    writer = csv.writer(file)
    if os.path.getsize(csv_name_out) == 0 :
        writer.writerow(["Matrix size", "Mean Pc", "Percolation rate", "(min,max)"])
    writer.writerow([stat[0], stat[1], stat[2], stat[3]])



