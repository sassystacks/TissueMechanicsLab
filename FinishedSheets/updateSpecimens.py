import csv
import pandas as pd

'''
Takes 2 CSVs and compares a list of 2 to see if one contains the other.
Returns a pandas dataframe from the csv with items missing. Writes a CSV
to a specified folder.

input args:

fnameBig - larger of the 2 csvs to check if the smaller is contained within
fnameSmall - the smaller csv Allfiles
fnameNewCSV - the name of the new csv file
headerList - entered as kwargs if you want to specify a header list
columns - identifiers to parse the data on can be entered as kwargs

To Do

Finish Writing the function
'''
#
# def checkAndWRite(fnameBig,fnameSmall,newCSVfname,**kwargs):

# headers = kwargs.get('headers',None)
# print(headers)
# columns = kwargs.get('columns',[0])#This needs a fix

fnameAll= '/home/richard/MyProjects/TissueMechanicsLab/RawData/Allfiles.csv'
fnameDone = '/home/richard/MyProjects/TissueMechanicsLab/emergData/emergDataSheet.CSV'
newCSVfname = '/home/richard/MyProjects/TissueMechanicsLab/FinishedSheets/NotDone.CSV'
kwarg_dict={'headers' : ['Project','Sample','Specimen','G-G','Width','Thickness','Position','Direction']}


dfAll = pd.read_csv(fnameAll)
dfDone = pd.read_csv(fnameDone,header=None,usecols=[0])
listAll = dfAll.loc[:,'Project':'Direction'].astype(str).values
#listAll = [fname[0]+"_"+fname[1] for fname in listAll]
listDone = dfDone.astype(str).values
#a = "_".join(listAll[1],listAll[2])
listForCSV = [item for item in listAll if not any("_".join((str(item[1]),str(item[2]))) in x for x in listDone) ]

dfCSV = pd.DataFrame(listForCSV)
dfCSV.to_csv(newCSVfname,index=False,header=kwarg_dict['headers'])

# fnameAll= '/home/richard/MyProjects/TissueMechanicsLab/RawData/Allfiles.csv'
# fnameDone = '/home/richard/MyProjects/TissueMechanicsLab/emergData/emergDataSheet.CSV'
# newCSVfname = '/home/richard/MyProjects/TissueMechanicsLab/FinishedSheets/NotDone.CSV'
# kwarg_dict={'headers' : ['Project','Sample','Specimen','G-G','Width','Thickness','Position','Direction']}
#
# checkAndWRite(fnameAll,fnameDone,newCSVfname,**kwarg_dict)
