import sys
import copy
import csv
import json
import random
import numpy as np
import pandas as pd
from keras.layers import Dense, Flatten, Dropout
from keras.models import Sequential, Input
from sklearn import preprocessing
import keras
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def getTestInput(filename):

    inp_data = pd.read_csv(filename)

    players = {}

    with open('PlayerData_2021.json', 'r') as file:
        players = json.load(file)

    names = inp_data['batsmen'][0].split(',')

    batting_team = inp_data['batting_team'][0]
    bowling_team = inp_data['bowling_team'][0]

    batsmen = []

    for i in names:
        try:
            batsmen.append(players[batting_team][i])
        except Exception as e:
            pass

    while len(batsmen) < 2:
        batsmen.append({
            "Inns": "10",
            "Runs": "100",
            "Ave": "30",
            "BF": "150",
            "SR": "130",
            "4s": "10",
            "6s": "5"
        })

    names = inp_data['bowlers'][0].split(',')
    bowlers = []

    for i in names:
        try:
            batsmen.append(players[bowling_team][i])
        except Exception as e:
            pass

    if len(bowlers) == 0:
        bowlers = [
            {
                "Inns": "3",
                "Overs": "10",
                "Mdns": "0",
                "Runs": "70",
                "Wkts": "3",
                "Ave": "36",
                "Econ": "7.12",
                "SR": "21"
            },
            {
                "Inns": "3",
                "Overs": "10",
                "Mdns": "0",
                "Runs": "61",
                "Wkts": "10",
                "Ave": "36",
                "Econ": "6.12",
                "SR": "15"
            }
        ]
    i = 0
    while len(bowlers) < 6:
        i = i % len(bowlers)
        bowlers.append(bowlers[i])
        i+1

    for i in range(len(batsmen)):
        for j in batsmen[i]:
            if batsmen[i][j] == '-' or batsmen[i][j] == '_':
                batsmen[i][j] = 0
            else:
                batsmen[i][j] = float(batsmen[i][j])

    for i in range(len(bowlers)):
        for j in bowlers[i]:
            if bowlers[i][j] == '-' or bowlers[i][j] == '_':
                bowlers[i][j] = 1000
            else:
                bowlers[i][j] = float(bowlers[i][j])

    stadiums = {}

    with open('AveragePowerPlayScore.json', 'r') as file:
        stadiums = json.load(file)

    test_x = []

    # print(bowlers)

    assert len(batsmen) >= 2
    assert len(bowlers) >= 6

    for i in range(6):
        t = [stadiums[inp_data['venue'][0]]]
        btm = batsmen[i % 2]
        bwl = bowlers[i]
        t.append(btm["Runs"])
        t.append(btm["Ave"])
        t.append(btm["SR"])
        t.append(btm["4s"])
        t.append(btm["6s"])
        t.append(bwl["Mdns"])
        t.append(bwl["Runs"])
        t.append(bwl["Wkts"])
        t.append(bwl["Ave"])
        t.append(bwl["Econ"])
        t.append(bwl["SR"])

        for j in range(len(t)):
            if t[j] == "-" or t[j] == "_":
                t[j] = 1000
            else:
                t[j] = float(t[j])

        test_x.append(t[:])

    return test_x


def predict(filename):
    X = getTestInput(filename)

    assert len(X) == 6

    for i in range(len(X)):
        X[i] = np.array(X[i])

    X = preprocessing.normalize(X)

    temp_X = []

    for i in range(len(X)):
        temp_X.append(X[i].tolist())

    X = temp_X

    cur_path = os.path.dirname(__file__)
    path = os.path.join(cur_path, "model_1.h5")

    model = keras.models.load_model(path)

    predictions = []

    for i in range(6):
        pr = model.predict(np.expand_dims(X[i], 0))
        predictions.append(pr[:])

    runs = 0

    # print(predictions)
    # print(pr[0])
    # assert False

    for i in range(6):
        tr = 0
        sm = 0
        for j in range(8):
            tr = tr + j * predictions[i][j][0][0]
            sm = sm + predictions[i][j][0][0]

        assert sm != 0
        # print("runs", runs)
        # print("Tr", tr)
        # print("sum", sum(pr[i]))
        runs = runs + (tr/sm) * 6
        print(tr, sm)

    runs = round(runs)

    return runs


def predictRuns(testInput):
    prediction = int(predict(testInput))
    return prediction


# print(predictRuns('inputFile.csv'))
