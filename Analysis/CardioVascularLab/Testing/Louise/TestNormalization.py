#from TestingTemplate import Test
import sys
sys.path.append('../../ExVivo')

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def calcStress(disp,force,dims):

    #Cauchy Stress
    stretch = (disp - disp[0])/dims1['length'] + 1
    stress = force/(dims1['width']*dims1['thickness'])*stretch

    return stress

def calcStrain(disp, dims):

    #Engineering Strain
    disp = disp-disp[0]  # Zero the displacement for the first measurement
    strain = disp/dims1['length'] # engineering strain

    return strain

def _normalizeData(ydata, xdata):
    '''
    This intakes 2 numpy arrays and normalizes them.
    returns:
        numpy arrays
    '''

    x_norm = (xdata - np.min(xdata))/(np.max(xdata)-np.min(xdata))
    y_norm = (ydata - np.min(ydata))/(np.max(ydata)-np.min(ydata))


    return y_norm, x_norm



# How the X_data Y_data will look once its in the data structure format
    #xdata = DataStructure._ProcessedData[0, :]
    #ydata = DataStructure._ProcessedData[:, 0]

#Read in Sample Data
df1 = pd.read_csv("NIH_BAV_Z2LC2_L1.csv", skiprows=[0,1,2,4], header = 'infer')
df2 = pd.read_csv("NIH_BAV_Z2LC2_U1.csv", skiprows=[0,1,2,4], header = 'infer')
dims1 = {'width':2.745,'thickness':1.75,'length':9.98}
dims2 = {'width':2.87,'thickness':1.815,'length':8.67}

#Calculate Stress Strain
stress = calcStress(df1['Disp'],df1['Load'],dims1)
strain = calcStrain(df1['Disp'],dims1)


#Plot unprocessed stress v. strain
plt.plot(strain,stress)
plt.xlabel('Strain')
plt.ylabel('Stress')
plt.title('Test Data')

#Normalize Data and Plot
stress_norm, strain_norm = _normalizeData(stress, strain)
plt.plot(strain_norm, stress_norm)
plt.xlabel('strain_norm')
plt.ylabel('stress_norm')
plt.title('Test Data - Normalized')

plt.show()