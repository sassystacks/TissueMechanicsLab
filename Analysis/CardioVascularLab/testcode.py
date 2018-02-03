#!/home/richard/anaconda/bin/python

import os
import pandas as pd

PATH = '/home/richard/MyProjects/Analysis/RawData'
dimensions = '/home/richard/MyProjects/Analysis/RawData/Analysis_part1_june2016_june2017.csv'
# items = os.listdir(importFolder)

#Read csv dimensions and populate list of patient and specimen concantenated
df = pd.read_csv(dimensions)
dic = df.to_dict()
t_fname_lst = [dic['Patient'][x] + '_' + dic['Specimen'][x] for x in xrange(0,len(dic['Patient']))]

#Recursively search below given path for all csv files
#result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(PATH) for f in filenames if os.path.splitext(f)[1] == '.CSV']
#Same thing as above, but no path included
result = [f for dp, dn, filenames in os.walk(PATH) for f in filenames if os.path.splitext(f)[1] == '.CSV' or os.path.splitext(f)[1] == '.TXT']

df["Filename"]= None


#List comprehension to extract all matching filenames from the dimensions CSV
fname_lst = [[name.split("_"),fname] for name in t_fname_lst for fname in result if (name in fname and "_Fail" in fname) ]


for name in fname_lst:

    df.loc[(df["Patient"] == name[0][0]) & (df["Specimen"] == name[0][1]),"Filename"] = name[1]
# #name for x in xrange(0,len(dic['Patient']
fnameWrite = os.path.join(PATH,"no_path_testCsv.csv")
df.to_csv(fnameWrite)

for name in result:
    if 'LLAA' in name:
        print(name)
