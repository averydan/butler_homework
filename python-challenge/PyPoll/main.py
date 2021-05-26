# import required modules
import os
import csv
import operator
# set path to csv file
csvpath = os.path.join('.', 'files', 'election_data.csv')
# open csv file
with open(csvpath) as csvfile:
    # set deliminator and start reading file
    csvreader = csv.reader(csvfile, delimiter=',')
    # skip header
    next(csvreader)
    # print total votes
    total_votes = sum(1 for row in csvfile )
    print(f"Total Votes: {total_votes}")
    print()
    # initialize dictionary to put candidates into
    candidates = {}
    # reset csvreader to first data row
    csvfile.seek(0)
    next(csvreader)
    # loop through all rows of data in csv
    for row in csvreader:
        # if the candidate is already in the dictionary, update their vote count
        if row[2] in candidates:
            candidates[row[2]]["Votes"] += 1
        else:
            # if the candidate is not yet in the dictionary, add them, add nested dictionary with vote count and and set their vote count to 1
            candidates.update({row[2]: {"Votes": 1}})
# loop through all candidates, calculate their percentage of votes, add it to a new key/value in nested dictionary
for i in candidates:
    candidates[i].update({"Percentage": candidates[i]["Votes"] / total_votes * 100})
# print list of candidates
print("List of Candidates:")
for i in candidates:
    print(i)
print()
# print each candidates percentage of votes
print("Each Candidates percetnage of votes:")
for i in candidates:
    print(f"{i} received {round(candidates[i]['Percentage'])} of votes.")
print()
# print each candidates amount of votes
print("Each Candidate recieved this many votes:")
for i in candidates:
    print(f"{i} received {round(candidates[i]['Votes'])} votes.")
print()
# initialize dictionary to look at only candidate name and vote count
vote_counts = {}
# add each candidate the their amount of votes to dictionary
for i in candidates:
    vote_counts.update({i : candidates[i]['Votes']})
# find key with highest value, print key
print(f"{max(vote_counts.items(), key=operator.itemgetter(1))[0]} won the vote.")

results = open("Results.txt", "w")
results.writelines(candidates["Khan"])