# PYTHON 3.8.0
import tensorflow as tf
from keras.models import Sequential, Input
from keras.layers import Dense, Flatten, Dropout
from sklearn import preprocessing
import pandas as pd
import numpy as np
import random
import json
import csv
import copy
import os
import sys

all_players = {}

with open("AllPlayerData.json", "r") as file:
    all_players = json.load(file)

stadiums = {}

with open("AveragePowerPlayScore.json", "r") as file:
    stadiums = json.load(file)

runs = 0
match_id = -1
innings = -1

X = []
Y = []

x = []
y = []

batsmen_all = []
batsmen_names = []
bowlers_all = []
bowlers_names = []

with open("Matches.csv", encoding="utf-8") as csvf:
    csvReader = csv.DictReader(csvf)
    for row in csvReader:
        if match_id != -1 and (match_id != row["ID"] or innings != row["Innings"]):
            match_id = row["ID"]
            innings = row["Innings"]

            bt_details = [0 for i in range(6)]

            if len(batsmen_all) == 0:
                batsmen_all.append({
                    "Inns": "0",
                    "Runs": "0",
                    "Ave": "0",
                    "BF": "0",
                    "SR": "100",
                    "4s": "0",
                    "6s": "0",
                })

            if len(bowlers_all) == 0:
                bowlers_all.append(
                    {
                        "Inns": "0",
                        "Overs": "0",
                        "Mdns": "0",
                        "Runs": "0",
                        "Wkts": "0",
                        "Ave": "-",
                        "Econ": "-",
                        "SR": "-",
                    }
                )
            for i in batsmen_all:
                tmp = [
                    i["Runs"],
                    i["Ave"],
                    i["BF"],
                    i["SR"],
                    i["4s"],
                    i["6s"]
                ]
                for j in range(len(tmp)):
                    if tmp[j] == '-' or tmp[j] == '_':
                        tmp[j] = 0
                    else:
                        tmp[j] = float(tmp[j])

                for j in range(len(tmp)):
                    bt_details[j] += tmp[j]

            for j in range(len(bt_details)):
                bt_details[j] /= len(batsmen_all)

            bw_details = [0 for i in range(6)]

            for i in bowlers_all:
                tmp = [
                    i["Mdns"],
                    i["Runs"],
                    i["Wkts"],
                    i["Ave"],
                    i["Econ"],
                    i["SR"]
                ]
                for j in range(len(tmp)):
                    if tmp[j] == '-' or tmp[j] == '_':
                        tmp[j] = 1000
                    else:
                        tmp[j] = float(tmp[j])

                for j in range(len(tmp)):
                    bw_details[j] += tmp[j]

            for j in range(len(bt_details)):
                bw_details[j] /= len(bowlers_all)

            t = [stadiums[row["Venue"]]]

            t.extend(bt_details)
            t.extend(bw_details)

            X.append(copy.deepcopy(t))
            Y.append(runs)

            runs = 0

            batsmen = []
            bowlers = []
            batsmen_names = []
            bowlers_names = []

        batsman = {}
        bowler = {}
        match_id = row["ID"]
        innings = row["Innings"]

        try:
            batsman = all_players["Batsmen"][row["Year"]][row["Batting"]][
                row["Striker"]
            ]
        except Exception as e:
            pass

        if batsman != {} and row["Batting"] not in batsmen_names:
            batsmen_all.append(batsman)
            batsmen_names.append(row["Batting"])
        # non_striker = all_players['Batsmen'][row['Year']][row['Batting']][row['Non_Striker']]
        bowler = {}
        try:
            bowler = all_players["Bowlers"][row["Year"]
                                            ][row["Bowling"]][row["Bowler"]]
        except Exception as e:
            pass

        if bowler != {} and row["Bowling"] not in bowlers_names:
            bowlers_all.append(bowler)
            bowlers_names.append(row["Bowling"])

        outcome = row["Outcome"]
        if outcome == "W":
            outcome = 0

        outcome = float(outcome)
        runs = runs + outcome


temp = list(zip(X, Y))
random.shuffle(temp)
X, Y = zip(*temp)

X = list(X)
Y = list(Y)

for i in range(len(X)):
    X[i] = np.array(X[i])


X = preprocessing.normalize(X)

temp_X = []

for i in range(len(X)):
    temp_X.append(X[i].tolist())

X = temp_X

# print(type(X))
# print(type(X[0].tolist()))

# print(X[0])

train_x = []
train_y = []

test_x = []
test_y = []

for i in X[:2]:
    test_x.append(i[:])

for i in Y[:2]:
    test_y.append(i)

for i in X[2:]:
    train_x.append(i[:])

for i in Y[2:]:
    train_y.append(i)

epochs = 100

model = Sequential()

model.add(Input(shape=(13,)))
model.add(Dense(64, activation="tanh"))
model.add(Dense(32, activation="relu"))
model.add(Dense(1))

model.compile(
    optimizer=tf.keras.optimizers.RMSprop(0.0001),
    loss="mse",
    metrics=["mae", "mse"],
)

model.summary()

model.fit(train_x, train_y, epochs=epochs)
print(model.evaluate(test_x, test_y))

shd_save = input("Save Model ?(y/n)\n")

if shd_save == "y":
    model.save("model_1.h5")
