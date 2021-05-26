# import required modules
import os
import csv
# set path to csv file
csvpath = os.path.join('.', 'files', 'budget_data.csv')
# open csv file
with open(csvpath) as csvfile:
    # set deliminator and start reading file
    csvreader = csv.reader(csvfile, delimiter=',')
    # skip header
    next(csvreader)
    # print total months
    total_months = "Total Months: " + str(sum(1 for row in csvfile ))
    print(total_months)
    # reset reader back to first row of data
    csvfile.seek(0)
    next(csvreader)
    # print total profit/loss
    total = "Total: " + str(sum(int(row[1]) for row in csvreader ))
    print(total)
    # reset reader back to first row of data
    csvfile.seek(0)
    next(csvreader)
    # set value for first month profit/loss
    last = int(next(csvreader)[1])
    # intitiate list of differences
    differences = []
    # iterate through csv to find differences in profit/loss
    for row in csvreader:
        differences.append(last - int(row[1]))
        last = int(row[1])
    # print average chnage
    average = "Average Change: " + str(sum(differences) / len(differences))
    print(average)
    # print greatest increase is profits
    increase = "Greatest Increase: " + str(max(differences))
    print(increase)
    # print greatest decrease is profits
    decrease = "Greatest Decrease: " + str(min(differences))
    print(decrease)
results = open("Results.txt", "w")
L = [total_months + "\n", total + "\n", average + "\n", increase + "\n", decrease]
results.writelines(L)