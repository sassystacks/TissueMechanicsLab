'''
Biax Analysis: Get HTM, LTM and Transition Stress/Strain Points for E11 and E22 in Biax txt file
Inputs: - 'path_name' = path where biax stress strain txt file is
        - 'output_csv' = where analysis csv file will go
Ouptuts:- parameter outputs --> biax analysis output Parameters
        - plot of truncated data with parameters

NOTE: Right now program can only read binned txt files, need to add unbinned txt files         
'''

import sys
sys.path.append('..')

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from math import sqrt
import rdp
from uniaxanalysis import getproperties as getprops
from Analyzer.TransitionProperties import ProcessTransitionProperties
from scipy import signal
import ntpath
import os

class Run_Analysis:

    def __init__(self, f, SS_type=[True, False, False], visualize=False, save_output=False):

        #Variables In and Initialize
        self.path_name = f
        #self.path_name = '/Volumes/Biomechanics_LabShare/Edmonton Valve Project/Real Tests/From Tais/Data/Binned_Interpolated/R15AL/Interpolated_4Dots_Stretch_Cauchy_bin_100_1_1.txt'
        self.visualize = visualize
        self.save_output = save_output
        self.SS_type = SS_type
        self.output_csv = '/Volumes/Biomechanics_LabShare/Analysis Programs/TissueMechanicsLab/Analysis/CardioVascularLab/ExVivo/BiaxAnalysisBasicOutputs/Biax_Outputs.csv'
        self.transitionProps = ProcessTransitionProperties(eps=0.025) # initialization step

        #set stress_strain, find max and normalize
        self.stress, self.strain = self.read_data() #read in data
        self.failIndx = self.findFailure() #find
        self.stress_strain_E11_norm, self.stress_strain_E22_norm = self._normalizeData()

        #Get transition properties
        self.stress_strain_E11, self.propDict_E11, self.LTMLine_E11, self.HTMLine_E11 = self.getTransitionProperties(direction = 11)
        self.stress_strain_E22, self.propDict_E22, self.LTMLine_E22, self.HTMLine_E22 = self.getTransitionProperties(direction = 22)

        #save proporties and plot data
        self.write2csv(self.propDict_E11)
        self.write2csv(self.propDict_E22)
        if self.visualize:
            self.plot_data()

    def read_data(self):
        #NEEDS MODIFICATION for differences in txt file for binned vs unbinned data
        #Read in Sample Data
        self.foldername = self.path_leaf(self.path_name)
        df = pd.read_csv(self.path_name, header = 'infer')
        if self.SS_type[0]: #1PK
            #self.strain = df[['L11(dots)','L22(dots)']].values
            #self.stress = df[['P11','P22']].values
            self.stresstype = '1PK (Pa)'
            self.straintype = 'Stetch'
        if self.SS_type[1]:#2PK
            #self.strain = df[['E11(dots)','E22(dots)']].values
            #self.stress = df[['S11','S22']].values
            self.stresstype = '2PK (Pa)'
            self.straintype = 'Strain'
        if self.SS_type[2]:#Cauchy
            #self.strain = df[['E11(dots)','E22(dots)']].values
            #self.stress = df[['T11','T22']].values
            self.stresstype = 'Cauchy'
            self.straintype = 'Strain'

        self.strain = df[['E11(dots)','E22(dots)']].values
        self.stress = df[['S11','S22']].values

        return self.stress, self.strain

    def path_leaf(self,path):
        fnameParts = path.split(os.path.sep)
        return fnameParts[-2]
        '''
        head, tail = ntpath.split(path)
        return head or ntpath.basename(head)
        '''

    def findFailure(self):

        # convolve the data with kernel
        # pick out the points where the sign changes

        indxArray1 = signal.argrelmax(self.stress[:,0], axis=0, order=1, mode='clip')
        indxArray2 = signal.argrelmax(self.stress[:,1], axis=0, order=1, mode='clip')
        # return index of the point of failure

        if indxArray1[0].any():
            indx1 = indxArray1[0][0]
        else:
            indx1 = np.argmax(self.stress[:,0])

        if indxArray2[0].any():
            indx2 = indxArray1[0][0]
        else:
            indx2 = np.argmax(self.stress[:,1])

        index = [indx1,indx2]
        return index

    def _normalizeData(self):
        '''
        This function normalizes x and y data between 0 and 1.
        Inputs: numpy arrays (x and y) and starting index.
        Returns: normalized data (as 2 separate arrays)
        '''
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

    def getTransitionProperties(self,direction):

        #Get  Biax Direction
        if direction == 11:
            type = 0
            stress_strain_norm = self.stress_strain_E11_norm
        elif direction == 22:
            type = 1
            stress_strain_norm = self.stress_strain_E22_norm

        #Prepare Data or Transition Properties
        stress_strain = np.stack((self.strain[:self.failIndx[type],type],
                            self.stress[:self.failIndx[type],type]),
                            axis=-1)

        self.transitionProps._setStressStrain(stress_strain,stress_strain_norm)
        self.transitionProps._runTransitionProps()
        self.propDict = self.transitionProps._outputAllValues()
        self.LTM_line, self.HTM_line = self.transitionProps._fitLineForMTM()

        self.propDict['Sample'] = self.foldername
        self.propDict['Direction'] = 'E' + str(direction)
        #self.MTM = {"HTM": self.LTM_line, "LTM": self.HTM_Line}
        '''
        propDict['MaxStrain_'] = self.props.strain[self.props.failIndx]
        propDict['StartStrain'] = self.props.strain[0]
        propDict['StartStress'] = self.props.stress[0]
        propDict['HighStiffness'] = self.transitionProps.rdp[-2:, :]
        print(propDict['HighStiffness'])
        propDict['RDP'] = self.transitionProps.rdp
        '''
        #print(self.propDict)
        return stress_strain, self.propDict, self.LTM_line, self.HTM_line

    def write2csv(self,dict):
        import csv
        csv_columns = ['MTMLow_', 'MTMhigh_','MaxStress_','T_Stress_Start_','T_Strain_Start_','T_Stress_End_','T_Strain_End_','Elbow_Region_','Sample','Direction']
        csv_file = self.output_csv

        if not os.path.isfile(csv_file):
            with open(csv_file, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                writer.writerow(dict)
        else:
            with open(csv_file, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writerow(dict)

    def make_line(self):
        #Re-organize data point in HTM and LTM for E11 and E22
        self.LTMLine_E11x = [self.LTMLine_E11[0],self.LTMLine_E11[2]]
        self.LTMLine_E11y = [self.LTMLine_E11[1],self.LTMLine_E11[3]]
        self.LTMLine_E22x = [self.LTMLine_E22[0],self.LTMLine_E22[2]]
        self.LTMLine_E22y = [self.LTMLine_E22[1],self.LTMLine_E22[3]]

        self.HTMLine_E11x = [self.HTMLine_E11[0],self.HTMLine_E11[2]]
        self.HTMLine_E11y = [self.HTMLine_E11[1],self.HTMLine_E11[3]]
        self.HTMLine_E22x = [self.HTMLine_E22[0],self.HTMLine_E22[2]]
        self.HTMLine_E22y = [self.HTMLine_E22[1],self.HTMLine_E22[3]]

    def plot_data(self):
        #Plot unprocessed stress v. strain
        self.make_line()
        plt.plot(self.stress_strain_E11[:,0],self.stress_strain_E11[:,1], color = 'Crimson', ls = 'dotted', label = 'E11')
        plt.plot(self.stress_strain_E22[:,0],self.stress_strain_E22[:,1], color = 'Blue',ls = 'dotted', label = 'E22')

        #Plot Stiffnesses
        plt.plot(self.LTMLine_E11x, self.LTMLine_E11y, color = 'Green')
        plt.plot(self.LTMLine_E22x, self.LTMLine_E22y, color = 'Green')
        plt.plot(self.HTMLine_E11x, self.HTMLine_E11y, color = 'Magenta')
        plt.plot(self.HTMLine_E22x, self.HTMLine_E22y, color = 'Magenta')


        # If Elbow Region Exists:
        if not np.isnan(self.propDict_E11['T_Strain_Start_']):
            plt.plot(self.propDict_E11['T_Strain_Start_'],self.propDict_E11['T_Stress_Start_'], marker = 'v', color = 'r')
            plt.plot(self.propDict_E11['T_Strain_End_'],self.propDict_E11['T_Stress_End_'], marker = 'v', color = 'r')
            plt.plot(self.propDict_E22['T_Strain_Start_'],self.propDict_E22['T_Stress_Start_'], marker = 'v', color = 'r')
            plt.plot(self.propDict_E22['T_Strain_End_'],self.propDict_E22['T_Stress_End_'], marker = 'v', color = 'r')

        #Plot Titles
        plt.xlabel(self.straintype)
        plt.ylabel(self.stresstype)
        plt.legend()
        plt.title(self.foldername)

        if self.save_output:
            self.plotfolder = '/Volumes/Biomechanics_LabShare/Analysis Programs/TissueMechanicsLab/Analysis/CardioVascularLab/ExVivo/BiaxAnalysisBasicOutputs/'
            plt.savefig(self.plotfolder + self.foldername + '.png')

        plt.show()
'''
--------------------------------MAIN--------------------------------------------
'''
import argparse

parser = argparse.ArgumentParser(prog='BiaxAnalysisBasic', description="""
                                    This is a command line based
                                    program that can be used to get stiffness parameters from biaxial
                                    data. Works for unbinned/binned data
                                    Example usage: python BiaxAnalysisBasic.py
                                    -f <path to file> -1PK -v -s """)
group = parser.add_mutually_exclusive_group(required=True)
parser.add_argument('-f','--file',
                        help="Enter a single file to have the data binned")
group.add_argument('-1PK','--firstPK', action = 'store_true',
                        help="File Type Selected 4Dots_Strain_1PK_1_1")
group.add_argument('-2PK','--secondPK', action = 'store_true',
                        help="File Type Selected 4Dots_Strain_2PK_1_1")
group.add_argument('-C','--Cauchy', action = 'store_true',
                        help="File Type Selected 4Dots_Strain_Cauchy_1_1")
parser.add_argument('-v','--visualize',action='store_true',help="""
                                pass this argument to visualize the data""")
parser.add_argument('-s','--save',action='store_true',
                    help="""pass this argument to save the plot""")

args = parser.parse_args()
f = args.file

Run_Analysis(f,SS_type = [args.firstPK, args.secondPK, args.Cauchy], visualize=args.visualize, save_output=args.save)
