import numpy as np
import csv
import matplotlib.pyplot as plt

"""This program is for taking the imported data, and displaying it for the use of analysis. 
Following the analysis, the program cleans the data for finding a productive d(Force)/d(Displacement) value from the instron data, to use for deducing the material's Young's modulus."""

#opening the data csv
with open(r"C:\Users\blake\Desktop\instron data\65 pasta sheet_1.csv", newline='') as csvfile:
    data_reader = csv.reader(csvfile, delimiter=' ')
    #initialising a counter, to keep track of which non-data lines have been looped past
    x = 0
    data_set = []
    #adding the dataset to the array for further processing
    #The first 14 rows are metadata, so I'm using the 15th row.
    for row in data_reader:
        x+=1
        if x>=14:
            data_set.append(row)

#for testing that the start of the data in the array is infact the values not the 
print(data_set[0])
print(data_set[1])
print(data_set[2])
print(data_set[3])

times = []
displacements = []
forces = []

for data in data_set:
    #split the data by the commas
    #handling the empty line issue
    try:
        print(type(data[0]))
        tdf = data[0].rstrip("'")
        tdf_separated = tdf.split(",")

        #pull out the force, displacement, time values.
        times.append(float(tdf_separated[0]))
        displacements.append(float(tdf_separated[1].strip("'\"")))
        forces.append(float(tdf_separated[2].strip("'\"")))

    #handling the case where there is an empty line throwing an error.    
    except:
        print("the line is erroneous")
    

    
#plot a graph of force against displacement
if len(forces) == len(displacements):
    plt.plot(displacements, forces)
else:
    print("the array lengths don't match, so the graph won't plot.")

plt.ylabel("Force / N")
plt.xlabel("Displacement / mm")

print("The maximum force was: ", max(forces))

#save the raw data figure
plt.savefig(r"C:\Users\blake\Desktop\instron data\ten_peieces_spagetti_plot.png")

plt.show()

#trim the values about the first point where the graph hits the appropriate gradient, and the first point where it peaks 
#(thresholds set by inspection, then stored in code)

#threshold defined here as the linear region at 6mm displacement and greater.

lower_bound_index = None
upper_bound_index = None

for y in range(len(displacements)):
    if displacements[y] > 2.5 and lower_bound_index == None:
        lower_bound_index = y
    if displacements[y] > 9.0 and upper_bound_index == None:
        upper_bound_index = y

trimmed_forces = np.array(forces[lower_bound_index: upper_bound_index])
trimmed_displacements = np.array(displacements[lower_bound_index: upper_bound_index])

plt.plot(trimmed_displacements, trimmed_forces)
plt.show()
#do a least squares line fit on the remaining data.
A = np.vstack([trimmed_displacements, np.ones(len(trimmed_displacements))]).T
m, c = np.linalg.lstsq(A, trimmed_forces)[0]
plt.plot(trimmed_displacements, trimmed_forces, label = 'Raw data')
plt.plot(trimmed_displacements, m*trimmed_displacements +c, label = 'Least squares fitted line')

plt.xlabel("Displacement/ mm")
plt.ylabel("Force/ N")

print("The gradient of the fitted line is:", m)

#save the figure
plt.savefig(r"C:\Users\blake\Desktop\instron data\ten_pieces_spagetti_plot_with_fitting.png")

plt.show()

