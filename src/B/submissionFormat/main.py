### Imports ###
# add imports - classes and defs
import sys
from predictor import predictRuns

"""
sys.argv[1] is the input test file name given as command line arguments

"""

runs = predictRuns(str(sys.argv[1]))
print("Predicted Runs: ", runs)