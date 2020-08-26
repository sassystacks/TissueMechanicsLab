from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from biax.GetBiaxData import ReadBiaxData
from Data.DataInterface import DataInterfacer
from scipy import signal
from uniaxanalysis.getproperties import getproperties as getprops


class biaxProps(object):

    def __init__(self, fname, dataType="Unbinned", ftype="4Dots_Stretch_1PK_1_1.txt", **kwargs):
        # initialize variables
        self.fname = fname[1]
        self.sample = fname[0]
        self.dataType = dataType
        self.ftype = ftype
        self.stress = []
        self.strain = []

        #set stress and strain, find max and normalize
        self.stress, self.strain = self.read_data()

        if self.dataType == "Unbinned":
            self.stress = self._smoothData(self.stress)
            self.strain = self._smoothData(self.strain)

        self.failIndx = self._findMax()

        self.stress_strain_E11_norm, self.stress_strain_E22_norm = self._normalizeBiaxData()


    def read_data(self):
        if self.dataType == "Binned":
            rawDataDF = pd.read_csv(self.fname, skiprows=0)
        if self.dataType == "Unbinned":
            rawDataDF = pd.read_csv(self.fname, skiprows=1)

        if self.ftype == "4Dots_Stretch_1PK_1_1.txt":  # 1PK
            self.stresstype = '1PK (Pa)'
            self.straintype = 'Stretch'
            self.StrainHeaders = ['L11(dots)','L22(dots)']
            self.StressHeaders = ['P11','P22']
        if self.ftype == "4Dots_Strain_2PK_1_1.txt":  # 2PK
            self.stresstype = '2PK (Pa)'
            self.straintype = 'Strain'
            self.StrainHeaders = ['E11(dots)','E22(dots)']
            self.StressHeaders = ['S11','S22']
        if self.ftype == "4Dots_Strain_Cauchy_1_1.txt":  # Cauchy
            self.stresstype = 'Cauchy (Pa)'
            self.straintype = 'Strain'
            self.StrainHeaders = ['L11(dots)','L22(dots)']
            self.StressHeaders = ['T11','T22']
        # read in headers for binned vs. unbinned data files
        if self.dataType == "Binned":
            self.strain = rawDataDF[self.StrainHeaders].to_numpy()
            self.stress = rawDataDF[self.StressHeaders].to_numpy()
        if self.dataType == "Unbinned":
            self.strain = rawDataDF[self.StrainHeaders].to_numpy()
            self.stress = rawDataDF[self.StressHeaders].to_numpy()

        return self.stress, self.strain

    def _findMax(self):

        indx1 = np.argmax(self.stress[:,0])
        indx2 = np.argmax(self.stress[:,1])
        index = [indx1, indx2]

        return index

    def _smoothData(self, data, winlen=71, porder=2):
        import numpy as np
        from scipy import signal
        data[:,0] = signal.savgol_filter(data[:,0], winlen, porder, deriv=0,
                                    delta=1.0, axis=-1, mode='interp', cval=0.0)
        data[:,1] = signal.savgol_filter(data[:,1], winlen, porder, deriv=0,
                                       delta=1.0, axis=-1, mode='interp', cval=0.0)
        return data

    def _normalizeBiaxData(self):

        xdata1 = self.strain[:,0]
        xdata2 = self.strain[:,1]
        ydata1 = self.stress[:,0]
        ydata2 = self.stress[:,1]

        x1_norm = (xdata1 - np.min(xdata1[:self.failIndx[0]])) / (np.max(xdata1[:self.failIndx[0]]) - np.min(xdata1[:self.failIndx[0]]))
        y1_norm = (ydata1 - np.min(ydata1[:self.failIndx[0]])) / (np.max(ydata1[:self.failIndx[0]]) - np.min(ydata1[:self.failIndx[0]]))

        x2_norm = (xdata2 - np.min(xdata2[:self.failIndx[1]])) / (np.max(xdata2[:self.failIndx[1]]) - np.min(xdata2[:self.failIndx[1]]))
        y2_norm = (ydata2 - np.min(ydata2[:self.failIndx[1]])) / (np.max(ydata2[:self.failIndx[1]]) - np.min(ydata2[:self.failIndx[1]]))

        stress_strain_E11_norm = np.stack((x1_norm[:self.failIndx[0]],
                            y1_norm[:self.failIndx[0]]),
                            axis=-1)
        stress_strain_E22_norm = np.stack((x2_norm[:self.failIndx[1]],
                            y2_norm[:self.failIndx[1]]),
                            axis=-1)

        return stress_strain_E11_norm, stress_strain_E22_norm
