#!/usr/bin/env python3
import json
import operator
from pprint import pprint

'''
Reads results.json
Prints the vote count sorted and human readable to stdout
Writes the vote count unsorted to a json file
'''


with open("results.json",'r') as f:
    ballots = json.load(f)

score = {}

score['entertainment'] = {}
score['gastsprekers'] = {}
score['workshops'] = {}

for key in ballots:
    if 'entertainment' in ballots[key]:
        for item in ballots[key]['entertainment']:
            try:
                score['entertainment'][item] += 1
            except KeyError:
                score['entertainment'][item] = 1

    if 'gastsprekers' in ballots[key]:
        for item in ballots[key]['gastsprekers']:
            try:
                score['gastsprekers'][item] += 1
            except KeyError:
                score['gastsprekers'][item] = 1

    if 'workshops' in ballots[key]:
        for item in ballots[key]['workshops']:
            try:
                score['workshops'][item] += 1
            except KeyError:
                score['workshops'][item] = 1

# print highscore
gastsprekers = sorted(score['gastsprekers'].items(), key=operator.itemgetter(1),reverse=True)
workshops = sorted(score['workshops'].items(), key=operator.itemgetter(1),reverse=True)
entertainment = sorted(score['entertainment'].items(), key=operator.itemgetter(1),reverse=True)


print("Gastsprekers:")
for item in gastsprekers:
    print (str(item[1]) + " votes\t" + item[0].split("(")[0] )

print ("\nWorkshops:")
for item in workshops:
    print (str(item[1]) + " votes\t" + item[0].split("(")[0] )

print ("\nEntertainment:")
for item in entertainment:
    print (str(item[1]) + " votes\t" + item[0].split("(")[0] )

with open("score.json",'w') as f:
    print (json.dumps(ballots), file=f)
