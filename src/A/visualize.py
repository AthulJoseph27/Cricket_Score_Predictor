import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import random
import json
import csv
import copy
import sys

"""
# Creating Training data

all_players = {}

with open("AllPlayerData.json", "r") as file:
    all_players = json.load(file)

X = []
Y = []


stadiums = [
    "Arun Jaitley Stadium",
    "Barabati Stadium",
    "Brabourne Stadium",
    "Brabourne Stadium, Mumbai",
    "Buffalo Park",
    "De Beers Diamond Oval",
    "Dr DY Patil Sports Academy",
    "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium",
    "Dubai International Cricket Stadium",
    "Eden Gardens",
    "Feroz Shah Kotla",
    "Green Park",
    "Himachal Pradesh Cricket Association Stadium",
    "Holkar Cricket Stadium",
    "JSCA International Stadium Complex",
    "Kingsmead",
    "M Chinnaswamy Stadium",
    "M.Chinnaswamy Stadium",
    "MA Chidambaram Stadium",
    "MA Chidambaram Stadium, Chepauk",
    "MA Chidambaram Stadium, Chepauk, Chennai",
    "Maharashtra Cricket Association Stadium",
    "Nehru Stadium",
    "New Wanderers Stadium",
    "Newlands",
    "OUTsurance Oval",
    "Punjab Cricket Association IS Bindra Stadium",
    "Punjab Cricket Association IS Bindra Stadium, Mohali",
    "Punjab Cricket Association Stadium, Mohali",
    "Rajiv Gandhi International Stadium",
    "Rajiv Gandhi International Stadium, Uppal",
    "Sardar Patel Stadium, Motera",
    "Saurashtra Cricket Association Stadium",
    "Sawai Mansingh Stadium",
    "Shaheed Veer Narayan Singh International Stadium",
    "Sharjah Cricket Stadium",
    "Sheikh Zayed Stadium",
    "St George's Park",
    "Subrata Roy Sahara Stadium",
    "SuperSport Park",
    "Vidarbha Cricket Association Stadium, Jamtha",
    "Wankhede Stadium",
    "Wankhede Stadium, Mumbai",
]

# training data = [stadium no , total runs , batsman runs , batsman avg ,
#                   batsman strike rate , batsman 4s , batsman 6s,
#                   bowler maidens , bowler runs conceded , bowler wickets,
#                   bowler average , bowler economy , bowler strike rate ]

runs = 0
match_id = -1
innings = -1

x = []
y = []

with open("Matches.csv", encoding="utf-8") as csvf:
    csvReader = csv.DictReader(csvf)
    for row in csvReader:
        if match_id != row["ID"] or innings != row["Innings"]:
            match_id = row["ID"]
            innings = row["Innings"]
            runs = 0
            if len(x) > 0:
                X.append(copy.deepcopy(x))
                Y.append(copy.deepcopy(y))
            x = []
            y = []
        t = [stadiums.index(row["Venue"]), runs]
        batsman = {}
        bowler = {}

        try:
            batsman = all_players["Batsmen"][row["Year"]][row["Batting"]][
                row["Striker"]
            ]
        except Exception as e:
            batsman = {
                "Inns": "0",
                "Runs": "0",
                "Ave": "0",
                "BF": "0",
                "SR": "100",
                "4s": "0",
                "6s": "0",
            }
        # non_striker = all_players['Batsmen'][row['Year']][row['Batting']][row['Non_Striker']]
        bowler = {}
        try:
            bowler = all_players["Bowlers"][row["Year"]][row["Bowling"]][row["Bowler"]]
        except Exception as e:
            bowler = {
                "Inns": "0",
                "Overs": "0",
                "Mdns": "0",
                "Runs": "0",
                "Wkts": "0",
                "Ave": "-",
                "Econ": "-",
                "SR": "-",
            }
        t.append(batsman["Runs"])
        t.append(batsman["Ave"])
        t.append(batsman["SR"])
        t.append(batsman["4s"])
        t.append(batsman["6s"])
        t.append(bowler["Mdns"])
        t.append(bowler["Runs"])
        t.append(bowler["Wkts"])
        t.append(bowler["Ave"])
        t.append(bowler["Econ"])
        t.append(bowler["SR"])

        for i in range(len(t)):
            if t[i] == "-" or t[i] == "_":
                t[i] = 100
            else:
                t[i] = float(t[i])
        x.append(t[:])
        y.append(row["Outcome"])
        outcome = row["Outcome"]
        if outcome == "W":
            outcome = 0
            y[-1] = 0

        y[-1] = min(int(y[-1]), 6)
        outcome = min(int(outcome), 6)
        runs += min(int(outcome), 6)

if len(x) > 0:
    X.append(copy.deepcopy(x))
    Y.append(copy.deepcopy(y))

data_set = []

for i in X:
    data_set.extend(i)

data_set = data_set[:1000]

filename = "Training_dataset.csv"

fields = [
    "stadium no",
    "total runs",
    "batsman runs",
    "batsman avg",
    "batsman strike rate",
    "batsman 4s",
    "batsman 6s",
    "bowler maidens",
    "bowler runs conceded",
    "bowler wickets",
    "bowler average",
    "bowler economy",
    "bowler strike rate",
]

with open(filename, "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(data_set)

"""

data_set = pd.read_csv("Training_dataset.csv")

sns.pairplot(
    data_set[
        [
            "total runs",
            "batsman avg",
        ]
    ],
    diag_kind="kde",
)


plt.show()
