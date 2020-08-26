import sys
sys.path.append('..')

from Analyzer.TransitionProperties import ProcessTransitionProperties
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk, filedialog
from uniaxanalysis.getproperties import getproperties as getprops
from uniaxanalysis.plotdata import DataPlotter
from uniaxanalysis.saveproperties import write_props_csv
from Data.DataInterface import DataInterfacer
from Analyzer.TransitionProperties import ProcessTransitionProperties as transitionProps

from matplotlib import pyplot as plt

import time

""""This frame creates a "good" button for the user to confirm that the analysis is adequate and save properties to TestOutputs
CSV. It also creates buttons for "Properties to Change" """

class Frame_3(tk.Frame):

    def __init__(self, master, tab, tab_no, dataInterface):

        tk.Frame.__init__(self, master)

        self.master = master
        self.tab = tab
        self.tab_no = tab_no
        self.dataInt = dataInterface
        self.fnameOut = 'TestOutputs.csv'

        self.transitionProps = ProcessTransitionProperties(self.tab_no, eps=0.025)

        # separate functions in tabs
        if self.tab_no == 1:  # UNIAX TAB

            changeLabel = Label(self.master, text="Properties to Change")
            changeLabel.grid(row=0, column=0, sticky='NW')

            button4 = Button(self.master, text="Ultimate Stress", width=20,
                             command=self.get_uts)
            button4.grid(row=1, column=0, sticky='NW')

            button5 = Button(self.master, text="Linear Stiffness", width=20,
                             command=self.get_linear)
            button5.grid(row=2, column=0, sticky='NW')

            spaceLabel = Label(self.master, text="                ")
            spaceLabel.grid(row=0, column=1)

            button6 = Button(self.master, text="Good", bg='green', height=5,  width=20,
                             command=self.write_analysis)
            button6.grid(row=0, column=2, rowspan=3, sticky='NE')

        elif self.tab_no == 2:  # BIAX TAB
            changeLabel = Label(self.master, text="Properties to Change")
            changeLabel.grid(row=0, column=0, sticky='NW')

            button4 = Button(self.master, text="Ultimate Stress", width=20,
                             command=self.get_uts)
            button4.grid(row=1, column=0, sticky='NW')

            button5 = Button(self.master, text="Linear Stiffness", width=20,
                             command=self.get_linear)
            button5.grid(row=2, column=0, sticky='NW')

            spaceLabel = Label(self.master, text="                ")
            spaceLabel.grid(row=0, column=1)

            button6 = Button(self.master, text="Good", bg='green', height=5, width=20,
                             command=self.write_biax_analysis)
            button6.grid(row=0, column=2, rowspan=3, sticky='NE')

    def get_uts(self):

        # get the ultimate stress and strain at ultimate stress on the graph
        utstr, uts = self.props.manual_max(self.props.strain, self.props.stress,
                                           self.plotter.xs, self.plotter.ys)
        self.plotter.set_max_point(utstr, uts)

    def get_linear(self):
        modulusElasticity, regionData = self.props.manual_linear(self.props.strain, self.props.stress,
                                                                 self.plotter.xs, self.plotter.ys)
        self.plotter.set_linear_region(regionData[0], regionData[1])

    def write_analysis(self):
        # import pdb;pdb.set_trace()
        # This function writes the value to a csv and destroys the button object in the GUI

        # Add stiffness to the list, if not append an empty string
        if self.dataInt.stiffness:
            self.dataInt.csvDataParser.outputDict[self.dataInt.sampleName]['Stiffness'] \
                = self.dataInt.stiffness

        else:
            self.dataInt.csvDataParser.outputDict[self.dataInt.sampleName]['Stiffness'] \
                = "NaN"

        # Add strength to the list, if not append an empty string
        if self.dataInt.strength:
            self.dataInt.csvDataParser.outputDict[self.dataInt.sampleName]['Strength'] \
                = self.dataInt.strength
        else:
            self.dataInt.csvDataParser.outputDict[self.dataInt.sampleName]['Strength'] \
                = "NaN"

        # Add all of the transition props to the output
        transitionProps = self.dataInt.TransitionPropsDict

        for prop, val in transitionProps.items():
            self.dataInt.csvDataParser.outputDict[self.dataInt.sampleName][prop] = val
            if prop not in self.dataInt.headersOut:
                self.dataInt.headersOut.append(prop)

        # Write the properties to the csv file specified
        write_props_csv(self.fnameOut, self.dataInt.csvDataParser.outputDict,
                        self.dataInt.sampleName, self.dataInt.headersOut)

        # change the button color after pressed
        self.dataInt.buttonsdict[self.dataInt.sampleName].configure(bg="green")

        del self.dataInt.stiffness, self.dataInt.strength, self.dataInt.sampleName

    def write_biax_analysis(self):
        import csv, os.path
        csv_columns = ['Sample', 'Direction', 'MTMLow_', 'MTMHigh_', 'MaxStress_', 'T_Stress_Start_',
                       'T_Strain_Start_', 'T_Stress_End_', 'T_Strain_End_', 'Elbow_Region_', 'MaxStrain_',
                       'StartStrain', 'StartStress', 'HighStiffness', 'RDP']

        csv_file = self.fnameOut

        transitionProps11 = self.dataInt.TransitionPropsDict11
        transitionProps22 = self.dataInt.TransitionPropsDict22

        if not os.path.isfile(csv_file):
            with open(csv_file, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                writer.writerow(transitionProps11)
                writer.writerow(transitionProps22)

        else:
            with open(csv_file, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writerow(transitionProps11)
                writer.writerow(transitionProps22)

        # change the button color after pressed
        self.dataInt.buttonsdict[self.dataInt.sampleName].configure(bg="green")





