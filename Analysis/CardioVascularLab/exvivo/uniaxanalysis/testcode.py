import pandas as pd
from numpy import genfromtxt
#
testList = ['RSAA20160621_U1',
            '/home/richard/MyProjects/TissueMechanicsLab/CleanSheets/RSAA20160621_U1.CSV',
            4.62, 2.365, 5.0]
#Pandas method
df =pd.read_csv(testList[1],index_col=False)
#
force = df.loc[:,"Force"].values
displacement = df.loc[:,"Displacement"]

#data = genfromtxt(testList[1],delimiter=',')
print(force)
