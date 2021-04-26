# PYTHON 3.8.0
import tensorflow as tf
from keras.models import Sequential, Input, Model
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

X = []
Y = []

runs = 0
match_id = -1
innings = -1
over = 0
runs_per_over = [0 for i in range(8)]
runs_overall = 0
cur_stadium = ''


def format_output(data):
    yo = [[] for i in range(8)]
    for i in range(len(data)):
        for j in range(8):
            yo[j].append(data[i][j])

    yzero = np.array(yo[0])
    yone = np.array(yo[1])
    ytwo = np.array(yo[2])
    ythree = np.array(yo[3])
    yfour = np.array(yo[4])
    yfive = np.array(yo[5])
    ysix = np.array(yo[6])
    yseven = np.array(yo[7])

    return yzero, yone, ytwo, ythree, yfour, yfive, ysix, yseven


def add_new_data():
    global runs_per_over, runs_overall, X, Y, cur_stadium

    t = [stadiums[cur_stadium]]

    # t.append(runs_overall)
    batsman = {}
    try:
        batsman = all_players["Batsmen"][row["Year"]
                                         ][row["Batting"]][row["Striker"]]
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

    X.append(t[:])
    Y.append(runs_per_over[:])

    # print(runs_per_over)

    for j in range(len(runs_per_over)):
        runs_per_over[j] = 0

    return t

# input nodes = [stadium avg , runs_over_all , striker stats , bowler stats]
# output nodes = [0s, 1s, 2s, 3s, 4s, 5s, 6s, 7s]


with open("Matches.csv", encoding="utf-8") as csvf:
    csvReader = csv.DictReader(csvf)
    for row in csvReader:
        if match_id != row['ID'] or innings != row['Innings']:
            runs_overall = 0
            match_id = row['ID']
            innings = row['Innings']

        if over == 0:
            cur_stadium = row['Venue']

        # print(over, row['Ball'].split('.')[0])
        # print(runs_per_over)

        if over != row['Ball'].split('.')[0]:
            over = row['Ball'].split('.')[0]

            # take the last standing batsman
            # print(runs_per_over)
            add_new_data()

        outcome = row["Outcome"]
        if outcome == "W":
            outcome = 0

        # print(outcome)

        outcome = int(outcome)
        runs_per_over[outcome] += 1

        runs_overall = runs_overall + 1

add_new_data()


train_x = []
train_y = []

test_x = []
test_y = []

temp = list(zip(X, Y))
random.shuffle(temp)
X, Y = zip(*temp)

X = list(X)
Y = list(Y)

for i in range(len(X)):
    X[i] = np.array(X[i])


X = tuple(preprocessing.normalize(X))

# temp_X = []

# for i in range(len(X)):
#     temp_X.append(X[i])

# sys.exit()

for i in X[:5]:
    test_x.append(i[:])

for i in Y[:5]:
    test_y.append(i[:])

for i in X[5:]:
    train_x.append(i[:])

for i in Y[5:]:
    train_y.append(i[:])

assert len(train_x) == len(train_y)

assert len(train_x[0]) == 12

input_layer = Input(shape=(len(train_x[0]),))
first_dense = Dense(units='128', activation='tanh')(input_layer)
hidden_dense = Dense(units='64', activation='tanh')(first_dense)
second_dense = Dense(units='32', activation='relu')(hidden_dense)

zeros = Dense(units='1', name='zeros')(second_dense)
ones = Dense(units='1', name='ones')(second_dense)
twos = Dense(units='1', name='twos')(second_dense)
threes = Dense(units='1', name='threes')(second_dense)
fours = Dense(units='1', name='fours')(second_dense)
fives = Dense(units='1', name='fives')(second_dense)
sixes = Dense(units='1', name='sixes')(second_dense)
sevens = Dense(units='1', name='sevens')(second_dense)

# for i in train_y:
#     print(i)

# sys.exit()
model = Model(inputs=input_layer, outputs=[
              zeros, ones, twos, threes, fours, fives, sixes, sevens])

optimizer = tf.keras.optimizers.SGD(lr=0.001)
model.compile(optimizer=optimizer,
              loss={'zeros': 'mse', 'ones': 'mse', 'twos': 'mse', 'threes': 'mse',
                    'fours': 'mse', 'fives': 'mse', 'sixes': 'mse', 'sevens': 'mse'},
              metrics={'zeros': tf.keras.metrics.RootMeanSquaredError(),
                       'ones': tf.keras.metrics.RootMeanSquaredError(),
                       'twos': tf.keras.metrics.RootMeanSquaredError(),
                       'threes': tf.keras.metrics.RootMeanSquaredError(),
                       'fours': tf.keras.metrics.RootMeanSquaredError(),
                       'fives': tf.keras.metrics.RootMeanSquaredError(),
                       'sixes': tf.keras.metrics.RootMeanSquaredError(),
                       'sevens': tf.keras.metrics.RootMeanSquaredError(),
                       })

history = model.fit(np.array(train_x), format_output(train_y),
                    epochs=50)

print(model.evaluate(np.array(test_x), format_output(test_y)))

shd_save = input("Save Model ?(y/n)\n")

if shd_save == "y":
    model.save("model_1.h5")
