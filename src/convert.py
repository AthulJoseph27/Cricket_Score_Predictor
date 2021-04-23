import json

data = []

with open('data.txt','r') as file:
	data = file.read().split('\n')

dic = {}

team = input('Enter Team Name : \n')

with open('all.json','r') as file:
	dic = json.load(file)

dic[team] = {}


for i in range(0,len(data),15):
	player = {}
	# player['Name'] = data[i]
	player['Span'] = data[i+1]
	player['Mat'] = data[i+2]
	player['Inns'] = data[i+3]
	player['NO'] = data[i+4]
	player['Runs'] = data[i+5]
	player['HS'] = data[i+6]
	player['Ave'] = data[i+7]
	player['BF'] = data[i+8]
	player['SR'] = data[i+9]
	player['100'] = data[i+10]
	player['50'] = data[i+11]
	player['0'] = data[i+12]
	player['4s'] = data[i+13]
	player['6s'] = data[i+14]
	dic[team][data[i]] = player

print(dic[team])

with open('All.json','w') as f:
		json.dump(dic,f,indent=4)





'''
"Player
Span
Mat
Inns
NO
Runs
HS
Ave
BF
SR
100
50
0
4s
6s
'''