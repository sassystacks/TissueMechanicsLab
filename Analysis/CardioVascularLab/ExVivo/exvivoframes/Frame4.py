import sys
sys.path.append('..')

from Analyzer.TransitionProperties import ProcessTransitionProperties
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk, filedialog
import uniaxanalysis.getproperties as getprops
from uniaxanalysis.plotdata import DataPlotter
from uniaxanalysis.saveproperties import write_props_csv


from matplotlib import pyplot as plt

import time

class Frame_4(tk.Frame):

    def __init__(self, master, tab, tab_no):

        tk.Frame.__init__(self, master)
        self.master = master
        self.tab = tab
        self.tab_no = tab_no

        self.fig = plt.figure(1)
        self.transitionProps = ProcessTransitionProperties(eps=0.025)
        self.plotter = DataPlotter()

        canvas = self.plotter.plot_graph(self.master, Row=0, Col=0)

    def getTransitionProperties(self):
        '''
        This sets all the transition properties for plotting
        '''
        import numpy as np
        stress_strain = np.stack((self.props.strain[:self.props.failIndx],
                                    self.props.stress[:self.props.failIndx]),
                                    axis=-1)
        stress_strain_norm = np.stack((self.props.strain_norm[:self.props.failIndx],
                                    self.props.stress_norm[:self.props.failIndx]),
                                    axis=-1)
        self.transitionProps._setStressStrain(stress_strain,stress_strain_norm)
        self.transitionProps._runTransitionProps()
        propDict = self.transitionProps._outputAllValues()
        propDict['MaxStrain_'] = self.props.strain[self.props.failIndx]
        propDict['StartStrain'] = self.props.strain[0]
        propDict['StartStress'] = self.props.stress[0]
        propDict['HighStiffness'] = self.transitionProps.rdp[-2:, :]
        print(propDict['HighStiffness'])
        propDict['RDP'] = self.transitionProps.rdp

        self.plotter.set_props(propDict)


    def getGraph(self, samplename):
        self.fig.clear()

        # Iterate through sample list to find matching sample
        for sample in self.sampleList:

            if samplename == sample[0]:
                # Get all of the properties for this sample
                self.props = getprops(fileDimslist=sample, smooth_width=29,
                                      std=7, chkderivate=0.04,
                                      stresstype=self.stresstype,
                                      straintype=self.straintype)
                self.getTransitionProperties()
                # create an instance of DataPlotter class and pass instance of
                # getproperties
                self.plotter.setClass(self.props)
                self.plotter.setSample(sample[0])
                self.frame7._SetCheckState()


                break
        else:
            print("Couldn't find the file")

