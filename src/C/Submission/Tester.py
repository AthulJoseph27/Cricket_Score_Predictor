import subprocess
import os

cur_path = os.path.dirname(__file__)
path = os.path.join(cur_path, "Inputs")

for file in os.listdir(path):
	print(str(file)," : ")
	subprocess.run('python3.8 main.py Inputs/'+str(file), shell=True)