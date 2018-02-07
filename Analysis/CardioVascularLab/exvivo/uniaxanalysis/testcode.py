import pandas as pd
from numpy import genfromtxt
from getproperties import getproperties
import generalformat.parsecsv

#Dictionary to pass to parsecsv for obtaining dta on specimen
args_dict = {
            'dimsfile':'/home/richard/MyProjects/TissueMechanicsLab/RawData/Allfiles.csv',
            'topdir':'/home/richard/MyProjects/TissueMechanicsLab/CleanSheets'
            }
inst =  generalformat.parsecsv(**args_dict)
#Create the list of specimens to be tested from Dimensions file
d =inst.getMatchingData(inst.dimsFile,inst.topDir)

for item in d:
    analysis = getproperties(fileDimslist = item,smooth_width=59)

dictionary = {}

data = dictionary.get("message", "Fuck")

print(data)  # Hello, World!
