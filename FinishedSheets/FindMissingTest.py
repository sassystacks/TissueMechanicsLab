import os
import pandas as pd
import csv

def findFile(identifier, fileTofind, topDir,*args,**kwargs):
    #Finds files matching a substring. Recursively searches directory to find
    #The first file that matches while ignoring the ignore specified in __init__()
    #pass
    #fileTofind : takes a substring to find matching files in the topDir
    #topDir : point to the top directory to search Recursively from

    ignore = kwargs.get('ignore','.tdf')

    fnamelist = [[root,f] for root,dirs,fname in os.walk(topDir) for f in fname if fileTofind in f and identifier in f]
    # for root,dirs,fname in os.walk(topDir):
    #     for f in fname:
    #         if fileTofind in f and identifier in f:

    return fnamelist


def makeSearchNames(fname):
    #reads information from dimensions sheet and creates a list of sample and specimen
    #concantenated with an underscore Sample_Specimen. Used to search for raw data file
    fullDF = pd.read_csv(fname)

    nameparts = fullDF[["Sample","Specimen"]]
    nameparts = nameparts.values.tolist()
    searchNames = ["{}_{}".format(name[0],name[1]) for name in nameparts]

    return searchNames

def makeSearchNamesMissingFiles(fname):
    #checks just the beginning of the name to see if any matches
    fullDF = pd.read_csv(fname)
    nameparts = fullDF['Sample'].values.tolist()
    searchNames = [name[:4] for name in nameparts]

    return searchNames

#Variables
fnameRead = '/home/richard/MyProjects/TissueMechanicsLab/FinishedSheets/NotDone.CSV'
tDir = '/home/richard/MyProjects/TissueMechanicsLab/RawData'
ident = '_Fail'
sNames = makeSearchNamesMissingFiles(fnameRead)

filelists = [findFile(ident, f, tDir,'TXT') for f in sNames]
print(filelists)
csvwrite = '/home/richard/MyProjects/TissueMechanicsLab/FinishedSheets/fnamelist.CSV'
#
# with open(csvwrite,'wb') as f:
#     outcsv = csv.writer(f)
#     outcsv.writerows(filelists)
