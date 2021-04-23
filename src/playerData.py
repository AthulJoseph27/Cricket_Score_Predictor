import json
import csv
import os

team_map = {}
team_map["KKR"] = "Kolkata Knight Riders"
team_map["RCB"] = "Royal Challengers Bangalore"
team_map["RR"] = "Rajasthan Royals"
team_map["MI"] = "Mumbai Indians"
team_map["DD"] = "Delhi Daredevils"
team_map["KXIP"] = "Kings XI Punjab"
team_map["PW"] = "Pune Warriors"
team_map["CSK"] = "Chennai Super Kings"
team_map["SRH"] = "Sunrisers Hyderabad"
team_map["RPS"] = "Rising Pune Supergiants"
team_map["DC_18"] = "Delhi Capitals"
team_map["DC"] = "Deccan Chargers"
team_map["KTK"] = "Kochi Tuskers Kerala"
team_map["PK"] = "Punjab Kings"
team_map["GL"] = "Gujarat Lions"


all_data = {}

all_data["Batsmen"] = {}
all_data["Bowlers"] = {}

cur_path = os.path.dirname(__file__)

path = os.path.join(cur_path, "Players")

for file in os.listdir(path):

    filename = str(file).split(".")[0]

    t = filename.split("_")

    tm = team_map[t[1]]
    n = int(t[0])
    if n >= 2018 and t[1] == "DC":
        tm = team_map["DC_18"]

    if t[0] not in all_data[t[2]]:
        all_data[t[2]][t[0]] = {}

    if tm not in all_data[t[2]][t[0]]:
        all_data[t[2]][t[0]][tm] = {}

    csv_file = os.path.join(path, file)

    with open(csv_file, encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)
        for row in csvReader:
            player = {}
            if t[2] == "Batsmen":
                player["Inns"] = row["Inns"]
                player["Runs"] = row["Runs"]
                player["Ave"] = row["Ave"]
                player["BF"] = row["BF"]
                player["SR"] = row["SR"]
                player["4s"] = row["4s"]
                player["6s"] = row["6s"]
                tm = team_map[t[1]]
                n = int(t[0])
                if n >= 2018 and t[1] == "DC":
                    tm = team_map["DC_18"]

                all_data[t[2]][t[0]][tm][row["Player"]] = player.copy()
            else:
                player["Inns"] = row["Inns"]
                player["Overs"] = row["Overs"]
                player["Mdns"] = row["Mdns"]
                player["Runs"] = row["Runs"]
                player["Wkts"] = row["Wkts"]
                player["Ave"] = row["Ave"]
                player["Econ"] = row["Econ"]
                player["SR"] = row["SR"]

                tm = team_map[t[1]]
                n = int(t[0])
                if n >= 2018 and t[1] == "DC":
                    tm = team_map["DC_18"]

                all_data[t[2]][t[0]][tm][row["Player"]] = player.copy()


with open("AllPlayerData.json", "w") as f:
    json.dump(all_data, f, indent=4)


col = {}

# col["match_id"] = 0
# col["season"] = 1
# col["start_date"] = 2
# col["venue"] = 3
# col["innings"] = 4
# col["ball"] = 5
# col["batting_team"] = 6
# col["bowling_team"] = 7
# col["striker"] = 8
# col["non_striker"] = 9
# col["bowler"] = 10
# col["runs_off_bat"] = 11
# col["extras"] = 12
# col["wides"] = 13
# col["noballs"] = 14
# col["byes"] = 15
# col["legbyes"] = 16
# col["penalty"] = 17
# col["wicket_type"] = 18
# col["player_dismissed"] = 19
# col["other_wicket_type"] = 20
# col["other_player_dismissed"] = 21