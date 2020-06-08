#from TestingTemplate import Test
import sys
sys.path.append('../../ExVivo')

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from math import sqrt
import rdp
from uniaxanalysis import getproperties as getprops

def calcStress(disp,force,dims):

    #Cauchy Stress
    stretch = (disp - disp[0])/dims4['length'] + 1
    stress = force/(dims4['width']*dims4['thickness'])*stretch

    return stress

def calcStrain(disp, dims):

    #Engineering Strain
    disp = disp-disp[0]  # Zero the displacement for the first measurement
    strain = disp/dims4['length'] # engineering strain

    return strain

def _findMax(data,index):

    currVal = data[index]
    nextVal = data[index + 1]

    while currVal < nextVal:
        index += 1

        currVal = data[index]
        nextVal = data[index+1]

        maxInd = index - 1

    return maxInd

def _normalizeData(ydata, xdata):
    '''
    This intakes 2 numpy arrays and normalizes them.
    returns:
        numpy arrays
    '''

    maxInd = _findMax(ydata,10)

    xdata = xdata[:maxInd]
    ydata = ydata[:maxInd]


    x_norm = (xdata - np.min(xdata))/(np.max(xdata)-np.min(xdata))
    y_norm = (ydata - np.min(ydata))/(np.max(ydata)-np.min(ydata))


    return y_norm, x_norm


# How the X_data Y_data will look once its in the data structure format
    #xdata = DataStructure._ProcessedData[0, :]
    #ydata = DataStructure._ProcessedData[:, 0]

#Read in Sample Data
df1 = pd.read_csv("NIH_BAV_Z2LC2_L1.csv", skiprows=[0,1,2,4], header = 'infer')
df2 = pd.read_csv("NIH_BAV_Z2LC2_U1.csv", skiprows=[0,1,2,4], header = 'infer')
df3 = pd.read_csv("NIH_BAV_Z2P2_L1.CSV", skiprows=[0,1,2,4],header = 'infer')
df4 = pd.read_csv("NIH_BAV_Z2A8_U1.CSV", skiprows=[0,1,2,4],header = 'infer')

dims1 = {'width':2.745,'thickness':1.75,'length':9.98}
dims2 = {'width':2.87,'thickness':1.815,'length':8.67}
dims3 = {'width':2.125,'thickness':2.16,'length':5.16}
dims4 = {'width':2.37,'thickness':2.10,'length': 2.65}

#Calculate Stress Strain
stress = calcStress(df4['Disp'],df4['Load'],dims4)
strain = calcStrain(df4['Disp'],dims4)

maxInd = _findMax(stress,10)

stress_trunc = stress[:maxInd]
strain_trunc = strain[:maxInd]

#Plot unprocessed stress v. strain
plt.plot(strain_trunc,stress_trunc, color = 'Blue', linestyle = 'dashed')
plt.xlabel('Strain')
plt.ylabel('Stress')
plt.title('Test Data')

'''
#Normalize Data and Plot
stress_norm, strain_norm = _normalizeData(stress, strain)
plt.plot(strain_norm, stress_norm, color = 'Blue')
plt.xlabel('Strain')
plt.ylabel('Stress')
plt.title('Test Data')

#Plot RDP curve (NORMALIZED DATA)
norm_data = list(zip(strain_norm, stress_norm))
norm_rdp_curve = rdp.rdp(norm_data, 0.02)
norm_rdpx, norm_rdpy = map(list,zip(*norm_rdp_curve))
plt.plot(norm_rdpx, norm_rdpy, color = "Red")
'''
#Plot RDP curve (ORIG DATA)
data = list(zip(strain_trunc, stress_trunc))
rdp_curve = rdp.rdp(data, 0.02)
rdpx, rdpy = map(list,zip(*rdp_curve))
plt.plot(rdpx, rdpy, color = "Red")


plt.show()