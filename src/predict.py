import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential, Input
from keras.layers import Dense, Flatten, Dropout
import numpy as np
import csv
import json
import sys
import os

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

all_players = {}

with open("predict_players.json", "r") as file:
    all_players = json.load(file)

input_data = {}

# with open("input_test_data.csv", "r") as csvf:
#     csvReader = csv.DictReader(csvf)
#     for row in csvReader:
#         input_data = row

# print(input_data)
# sys.exit()

runs = 0

inp = [0 for i in range(len(stadiums))]


inp[stadiums.index("Wankhede Stadium")] = 1

inp.append(runs)

batsman = {
    "Inns": "3",
    "Runs": "71",
    "Ave": "23.66",
    "BF": "64",
    "SR": "110.93",
    "4s": "9",
    "6s": "0",
}

non_striker = {
    "Inns": "2",
    "Runs": "36",
    "Ave": "18",
    "BF": "41",
    "SR": "87.8",
    "4s": "4",
    "6s": "0",
}

all_bowlers = [
    {
        "Inns": "3",
        "Overs": "12",
        "Mdns": "0",
        "Runs": "111",
        "Wkts": "3",
        "Ave": "37",
        "Econ": "9.25",
        "SR": "24",
    },
    {
        "Inns": "3",
        "Overs": "11",
        "Mdns": "0",
        "Runs": "101",
        "Wkts": "5",
        "Ave": "20.2",
        "Econ": "9.18",
        "SR": "13.2",
    },
    {
        "Inns": "3",
        "Overs": "12",
        "Mdns": "0",
        "Runs": "111",
        "Wkts": "3",
        "Ave": "37",
        "Econ": "9.25",
        "SR": "24",
    },
    {
        "Inns": "3",
        "Overs": "11",
        "Mdns": "0",
        "Runs": "101",
        "Wkts": "5",
        "Ave": "20.2",
        "Econ": "9.18",
        "SR": "13.2",
    },
    {
        "Inns": "3",
        "Overs": "12",
        "Mdns": "0",
        "Runs": "100",
        "Wkts": "6",
        "Ave": "16.66",
        "Econ": "8.33",
        "SR": "12",
    },
    {
        "Inns": "1",
        "Overs": "3",
        "Mdns": "0",
        "Runs": "40",
        "Wkts": "0",
        "Ave": "-",
        "Econ": "13.33",
        "SR": "-",
    },
]
bowler = all_bowlers[0]

inp.append(batsman["Runs"])
inp.append(batsman["Ave"])
inp.append(batsman["SR"])
inp.append(batsman["4s"])
inp.append(batsman["6s"])
inp.append(bowler["Mdns"])
inp.append(bowler["Runs"])
inp.append(bowler["Wkts"])
inp.append(bowler["Ave"])
inp.append(bowler["Econ"])
inp.append(bowler["SR"])

for i in range(len(inp)):
    if inp[i] == "-" or inp[i] == "_":
        inp[i] = 1e9
    else:
        inp[i] = float(inp[i])

# model = Sequential()

# model.add(Input(shape=(55,)))
# model.add(Dense(32, activation="sigmoid"))
# model.add(Dense(32, activation="sigmoid"))
# model.add(Dense(1))

# model.compile(
#     optimizer=tf.keras.optimizers.RMSprop(0.001),
#     loss="mse",
#     metrics=["mae", "mse"],
# )

cur_path = os.path.dirname(__file__)

path = os.path.join(cur_path, "model_1.h5")

model = keras.models.load_model(path)


model.summary()

runs = 0

# print(len(inp))

# print(inp)

for i in range(36):
    new_score = model.predict(np.array([inp])).flatten()[0]
    new_score = round(new_score)
    if (new_score - runs) % 2 != 0 or ((i != 0) and (i % 6 == 0)):
        batsman, non_striker = non_striker, batsman

    bowler = all_bowlers[i % 6]
    inp = []
    inp = [0 for i in range(len(stadiums))]
    inp[stadiums.index("Wankhede Stadium")]
    inp.append(new_score)
    inp.append(batsman["Runs"])
    inp.append(batsman["Ave"])
    inp.append(batsman["SR"])
    inp.append(batsman["4s"])
    inp.append(batsman["6s"])
    inp.append(bowler["Mdns"])
    inp.append(bowler["Runs"])
    inp.append(bowler["Wkts"])
    inp.append(bowler["Ave"])
    inp.append(bowler["Econ"])
    inp.append(bowler["SR"])
    for i in range(len(inp)):
        if inp[i] == "-" or inp[i] == "_":
            inp[i] = 1e9
        else:
            inp[i] = float(inp[i])
    assert len(inp) == 55
    runs = new_score

print("Predicted Score is : " + str(round(runs)))
