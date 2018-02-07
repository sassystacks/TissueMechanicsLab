import pandas as pd
from numpy import genfromtxt
from getproperties import getproperties
from parsecsv import parsecsv
import csv

#Dictionary to pass to parsecsv for obtaining dta on specimen
args_dict = {
            'dimsfile':'/home/richard/MyProjects/TissueMechanicsLab/RawData/Allfiles.csv',
            'topdir':'/home/richard/MyProjects/TissueMechanicsLab/CleanSheets'
            }
inst =  parsecsv(**args_dict)
#Create the list of specimens to be tested from Dimensions file
d =inst.getMatchingData(inst.dimsFile,inst.topDir)

# for item in d:
#     analysis = getproperties(fileDimslist = item,smooth_width=59


for i,f in enumerate(d):
    f[1]=f[0]+".CSV"
    d[i] = f

print d
# sample,specimen = [f[0].split(" ") for f in d]
# project = "AA"
# fname = [f[0] + ".CSV" for f in d]
#
# finalList = []
# for i,vals in enumerate(d):
#     finallist.append([project,sample[i],specimen[i],fname[i],d[]])
t_fname = '/home/richard/MyProjects/TissueMechanicsLab/emergData/emergDataSheet.CSV'

with open(t_fname,'wb') as f:

    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(d)
