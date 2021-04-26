# PYTHON 3.8.0
import tensorflow as tf
from keras.models import Sequential, Input
from keras.layers import Dense, Flatten, Dropout
from keras import backend as K
from keras.layers import Activation
from keras.utils.generic_utils import get_custom_objects
from sklearn import preprocessing
import seaborn as sns
import pandas as pd
import numpy as np
import statistics
import random
import json
import csv
import copy
import os
import sys
# import tensorflow.compat.v1 as tfc


# def custom_activation(x):
#     x = K.cast(K.sum(x, axis=None, keepdims=False), dtype=K.floatx())
#     # sess = tfc.InteractiveSession()
#     # tfc.print(K.sigmoid(x) * 7)
#     return (K.sigmoid(x))


# get_custom_objects().update(
#     {'custom_activation': Activation(custom_activation)})


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
        t = [0 for k in range(len(stadiums))]
        t[stadiums.index(row["Venue"])] = 1
        t.append(runs)
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
            bowler = all_players["Bowlers"][row["Year"]
                                            ][row["Bowling"]][row["Bowler"]]
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
                t[i] = 1000
            else:
                t[i] = float(t[i])
        x.append(t[:])

        outcome = row["Outcome"]
        if outcome == "W":
            outcome = 0

        outcome = float(outcome)
        runs = runs + float(outcome)
        y.append(outcome)

if len(x) > 0:
    X.append(copy.deepcopy(x))
    Y.append(copy.deepcopy(y))

# sys.exit()
# MODEL

"""
    Output Nodes:

        0 , 1, 2, 3, 4, 5, 6
"""

train_x = []
train_y = []

test_x = []
test_y = []

temp = list(zip(X, Y))
random.shuffle(temp)
X, Y = zip(*temp)

for i in X[:5]:
    test_x.extend(i[:])

for i in Y[:5]:
    test_y.extend(i[:])

for i in X[5:]:
    train_x.extend(i[:])

for i in Y[5:]:
    train_y.extend(i[:])


# for i in range(len(train_x)):
#     assert train_x[i][43] <= train_y[i]


epochs = 10

model = Sequential()

model.add(Input(shape=(55,)))
model.add(Dense(1024, activation="sigmoid"))
model.add(Dense(256, activation="sigmoid"))
model.add(Dense(32, activation="sigmoid"))
model.add(Dense(1, activation="sigmoid"))
# model.add(Activation(custom_activation, name='SpecialActivation'))

model.compile(
    optimizer=tf.keras.optimizers.RMSprop(0.00001),
    loss="mse",
    metrics=["mae", "mse"],
)

model.summary()

model.fit(train_x, train_y, epochs=epochs)
print(model.evaluate(test_x, test_y))

shd_save = input("Save Model ?(y/n)\n")

if shd_save == "y":
    model.save("model_1.h5")
