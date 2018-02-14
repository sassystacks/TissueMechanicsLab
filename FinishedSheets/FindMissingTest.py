import os
import pandas as pd
import csv
from itertools import islice

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

def findFile_patient_specimen(identifier, fileTofind, topDir,*args,**kwargs):
    #Finds files matching a substring. Recursively searches directory to find
    #The first file that matches while ignoring the ignore specified in __init__()
    #pass
    #fileTofind : takes a substring to find matching files in the topDir
    #topDir : point to the top directory to search Recursively from

    ignore = kwargs.get('ignore','.tdf')

    fnamelist = [[root,f] for root,dirs,fname in os.walk(topDir) for f in fname if fileTofind[:4] in f and identifier in f and fileTofind[-2:] in f]
    fnamelist = [l for l in fnamelist for item in l if '.CSV' in item]

    return fnamelist

def makeSearchNames(fname):
    #reads information from dimensions sheet and creates a list of sample and specimen
    #concantenated with an underscore Sample_Specimen. Used to search for raw data file
    fullDF = pd.read_csv(fname)

    nameparts = fullDF[["Sample","Specimen"]]
    nameparts = nameparts.values.tolist()
    searchNames = ["{}_{}".format(name[0],name[1]) for name in nameparts]

    return searchNames

def makeSearchNamesMissingFiles(fullDF):
    #checks just the beginning of the name to see if any matches
    #input fullDF : pandas dataframe

    nameparts = fullDF['Sample'].values.tolist()
    #namesForlist = fullDF[['Sample','Specimen']].values.tolist()
    # searchNames = [name[0][:4]+"_"+name[1] for name in nameparts]
    searchNames = [name[:4] for name in nameparts]

    return searchNames

#Variables
fnameRead = '/home/richard/MyProjects/TissueMechanicsLab/FinishedSheets/NotDone.CSV'
tDir = '/home/richard/MyProjects/TissueMechanicsLab/RawData'
ident = '_Fail'
fullDF = pd.read_csv(fnameRead)
sNames = makeSearchNamesMissingFiles(fullDF)
sNames = set(sNames)
# t_list = [s[0][:4] for s in sNames]
filelists = [(findFile(ident, s, tDir,'TXT'),s) for s in sNames]

chklist = fullDF[['Sample','Specimen']].values.tolist()
chklist = [[l[0][:4],l[1]]for l in chklist]

finallist =[]
for l1 in filelists:
    for item in chklist:
        if item[0] == l1[1]:
            for l2 in l1[0]:
                if item[1] in l2[1] and '.CSV' in l2[1]:
                    t_list = [l2[0],l2[1],item[0],item[1]]
                    finallist.append(t_list)

for f in finallist:
    fNameIn = os.path.join(f[0],f[1])
    t_fname = f[2] + "_" + f[3] +".CSV"
    fNameOut = os.path.join('/home/richard/MyProjects/TissueMechanicsLab/CleanSheets/incompleteNames',t_fname)
    with open(fNameIn,"rb") as inTxt, open(fNameOut,"wb") as outCsv:
        r = csv.reader(islice(inTxt, 5,None))
        outCsv = csv.writer(outCsv)
        outCsv.writerow(["time","Displacement","Force"])
        outCsv.writerows(r)
# newfNamelist.append([fullFname,f[1]])
# csvwrite = '/home/richard/MyProjects/TissueMechanicsLab/FinishedSheets/fnamelist.CSV'


# with open(csvwrite,'wb') as f:
#     outcsv = csv.writer(f)
#     outcsv.writerows(filelists)
