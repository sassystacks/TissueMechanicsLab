import sys
sys.path.append('..')

from Analyzer.TransitionProperties import ProcessTransitionProperties
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk, filedialog
import uniaxanalysis.getproperties as getprops
from uniaxanalysis.plotdata import DataPlotter
from uniaxanalysis.saveproperties import write_props_csv
from biax.biaxProps import biaxProps as getBiaxProps
from biax.biaxPlotter import BiaxPlotter
import numpy as np

from matplotlib import pyplot as plt

import time

class Frame_4(tk.Frame):

    def __init__(self, master, tab, tab_no, dataInterface):

        tk.Frame.__init__(self, master)
        self.master = master
        self.tab = tab
        self.tab_no = tab_no
        self.dataInt = dataInterface
        self.dataType = self.dataInt.dataType
        self.stresstype = self.dataInt.stresstype
        self.straintype = self.dataInt.straintype

        self.fig = plt.figure(1)
        self.plotter = DataPlotter(self.dataInt, self.tab_no)
        self.biaxPlotter = BiaxPlotter(self.dataInt, self.tab_no)

        self.transitionProps = ProcessTransitionProperties(self.tab_no, eps=0.03) #eps 0.025 for uniax, 0.03 for biax

        #separate functions for tabs
        if self.tab_no == 1:  # UNIAX TAB
            canvas = self.plotter.plot_graph(self.master, Row=0, Col=0)

            getGraphButton = ttk.Button(self.tab, text='Show Graph', width=20,
                                        command=self.getGraph)
            getGraphButton.grid(row=12, column=1, sticky='SE')

        elif self.tab_no == 2:  # BIAX TAB
            canvas = self.biaxPlotter.plot_graph(self.master, Row=0, Col=0)

            getGraphButton = ttk.Button(self.tab, text='Show Graph', width=20,
                                        command=self.getGraphBiax)
            getGraphButton.grid(row=12, column=2, sticky='SE')


    def getTransitionProperties(self):
        '''
        This sets all the transition properties for plotting
        '''
        stress_strain = np.stack((self.props.strain[:self.props.failIndx],
                                    self.props.stress[:self.props.failIndx]),
                                    axis=-1)
        stress_strain_norm = np.stack((self.props.strain_norm[:self.props.failIndx],
                                    self.props.stress_norm[:self.props.failIndx]),
                                    axis=-1)
        self.transitionProps._setStressStrain(stress_strain,stress_strain_norm)
        self.transitionProps.runTransitionProps()
        propDict = self.transitionProps.outputAllValues()
        propDict['MaxStrain_'] = self.props.strain[self.props.failIndx]
        propDict['StartStrain'] = self.props.strain[0]
        propDict['StartStress'] = self.props.stress[0]
        propDict['HighStiffness'] = self.transitionProps.rdp[-2:, :]
        propDict['RDP'] = self.transitionProps.rdp
        print(propDict)
        self.dataInt.setTransitionProps(propDict)
        return propDict

    def getBiaxTransitionProperties(self, direction):
        #get direction
        if direction == 11:
            type = 0
            stress_strain_norm = self.props.stress_strain_E11_norm
        elif direction == 22:
            type = 1
            stress_strain_norm = self.props.stress_strain_E22_norm

        #prepare data for transition props
        stress_strain = np.stack((self.props.strain[:self.props.failIndx[type],type],
                                  self.props.stress[:self.props.failIndx[type],type]),
                                 axis=-1)

        self.transitionProps._setStressStrain(stress_strain, stress_strain_norm)

        self.transitionProps.runTransitionProps()

        propDict = self.transitionProps.outputAllValues()

        self.LTM_line, self.HTM_line = self.transitionProps._fitLineForMTM()

        propDict['Sample'] = self.dataInt.sampleName
        propDict['Direction'] = 'E' + str(direction)

        propDict['MaxStrain_'] = self.props.strain[self.props.failIndx[type],type]
        propDict['StartStrain'] = self.props.strain[0,type]
        propDict['StartStress'] = self.props.stress[0,type]
        propDict['HighStiffness'] = self.transitionProps.rdp[-2:,:]
        propDict['RDP'] = self.transitionProps.rdp
        print(propDict)

        if direction == 11:
            self.dataInt.setBiaxTransitionProps11(propDict)
        elif direction == 22:
            self.dataInt.setBiaxTransitionProps22(propDict)

        return stress_strain, propDict, self.LTM_line, self.HTM_line

    def getGraph(self):
        self.fig.clear()

        # Iterate through sample list to find matching sample
        for sample in self.dataInt.sampleList:

            if self.dataInt.sampleName == sample[0]:
                # Get all of the properties for this sample
                self.props = getprops(fileDimslist=sample, smooth_width=29,
                                      std=7, chkderivate=0.04,
                                      stresstype=self.stresstype,
                                      straintype=self.straintype)

                self.getTransitionProperties()

                # create an instance of DataPlotter class and pass instance of
                # getproperties
                self.dataInt.setMaster(self.master)
                self.plotter.setClass(self.props, self.master)
                self.plotter.setSample(sample[0])
                self.plotter.SetCheckState()
                self.dataInt.buttonsdict[self.dataInt.sampleName].configure(bg="yellow")

                break
        else:
            print("Couldn't find the file")

        canvas = self.plotter.plot_graph(self.master, Row=0, Col=0)

    def getGraphBiax(self):
        self.fig.clear()

        #iterate through sample list to find matching sample
        for sample in self.dataInt.sampleList:
            if self.dataInt.sampleName == sample[0]:

                self.props = getBiaxProps(fname=sample, dataType=self.dataInt.dataType, ftype=self.dataInt.ftype)

                self.getBiaxTransitionProperties(direction=11)
                self.getBiaxTransitionProperties(direction=22)

                # create an instance of BiaxPlotter class
                self.dataInt.setMaster(self.master)
                self.biaxPlotter.setClass(self.props, self.master)
                self.biaxPlotter.setSample(sample[0])
                self.biaxPlotter.SetCheckState()

                self.dataInt.buttonsdict[self.dataInt.sampleName].configure(bg='yellow')

                break
        else:
            print("Couldn't find the file")

        canvas = self.plotter.plot_graph(self.master, Row=0, Col=0)


