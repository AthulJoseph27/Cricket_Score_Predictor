import csv
import json

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

runs = {}
matches = {}

for i in stadiums:
    runs[i] = 0
    matches[i] = []

with open("Matches.csv", encoding="utf-8") as csvf:
    csvReader = csv.DictReader(csvf)
    for row in csvReader:
        n = row["Outcome"]
        if n == "W":
            n = 0
        n = int(n)
        runs[row["Venue"]] = runs[row["Venue"]] + int(n)
        matches[row["Venue"]].append(row["ID"]+row["Innings"])


dic = {}

for i in stadiums:
    n = len(set(matches[i]))
    dic[i] = round(runs[i]/n)

with open('AveragePowerPlayScore.json', 'w') as file:
    json.dump(dic, file, sort_keys=True, indent=4)
