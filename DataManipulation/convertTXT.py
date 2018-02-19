import csv
import os
from itertools import islice

def convertTXT(fnameOld,fnameNew,topDir,newDir):

    fname = os.path.join(topDir,fnameOld)
    fullFname = os.path.join(newDir,fnameNew)

    with open(fname) as inTxt, open(fullFname,"w") as outCsv:
        r = csv.reader(islice(inTxt, 5,None))
        outCsv = csv.writer(outCsv)
        outCsv.writerow(["time","Displacement","Force"])
        outCsv.writerows(r)

newDir = '/home/richard/MyProjects/TissueMechanicsLab/CleanSheets/Feb16_2018'
topDir = '/home/richard/MyProjects/TissueMechanicsLab/RawData/cp_Test_Data/20180216_testing'
flist = os.listdir(topDir)

flistOld = [f for f in flist if '.TXT' in f and '_Fail' in f]
flistNew = [f.split(" ")[0][:-5] + ".CSV" for f in flistOld]

for f in flistNew:
    for item in flistOld:
        if f[:-5] in item:
            convertTXT(item,f,topDir,newDir)
            print "writing"
print(flist)
