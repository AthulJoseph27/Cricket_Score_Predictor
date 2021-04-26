import tensorflow as tf
import keras
from sklearn import preprocessing
from keras.models import Sequential, Input
from keras.layers import Dense, Flatten, Dropout
import pandas as pd
import numpy as np
import random
import json
import csv
import copy
import os
import sys


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
            batsmen.append(players['Batsmen'][batting_team][i])
        except Exception as e:
            pass

    if len(batsmen) == 0:
        batsmen = [
            {
                "Inns": "10",
                "Runs": "100",
                "Ave": "30",
                "BF": "150",
                "SR": "130",
                "4s": "10",
                "6s": "5"
            }
        ]

    names = inp_data['bowlers'][0].split(',')
    bowlers = []

    for i in names:
        try:
            batsmen.append(players['Bowlers'][bowling_team][i])
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
            }
        ]

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

    bt_details = [0 for i in range(6)]
    bw_details = [0 for i in range(6)]

    for i in batsmen:
        tmp = [
            i["Runs"],
            i["Ave"],
            i["BF"],
            i["SR"],
            i["4s"],
            i["6s"]
        ]
        for j in range(len(tmp)):
            bt_details[j] += tmp[j]

    for i in bowlers:
        tmp = [
            i["Mdns"],
            i["Runs"],
            i["Wkts"],
            i["Ave"],
            i["Econ"],
            i["SR"]
        ]
        for j in range(len(tmp)):
            bw_details[j] += tmp[j]

    stadiums = {}

    with open('AveragePowerPlayScore.json', 'r') as file:
        stadiums = json.load(file)

    test_x = []

    if inp_data['venue'][0] in stadiums:
        test_x.append(stadiums[inp_data['venue'][0]])
    else:
        test_x.append(random.randint(40, 70))

    test_x.extend(bt_details)
    test_x.extend(bw_details)

    return test_x


def predict(filename):

    test_x = getTestInput(filename)

    temp = []
    temp.append(preprocessing.normalize([np.array(test_x)]).tolist())

    test_x = temp[0]

    cur_path = os.path.dirname(__file__)
    path = os.path.join(cur_path, "model_1.h5")

    model = keras.models.load_model(path)

    prediction = model.predict(np.array(test_x)).flatten()[0]

    prediction = round(prediction)

    return prediction


def predictRuns(testInput):
    prediction = int(predict(testInput))
    return prediction


print(predictRuns('inputFile.csv'))
