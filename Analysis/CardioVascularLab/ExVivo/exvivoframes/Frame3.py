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

""""This frame creates a "good" button for the user to confirm that the analysis is adequate and save properties to TestOutputs
CSV. It also creates buttons for "Properties to Change" """

class Frame_3(tk.Frame):

    def __init__(self, master, tab, tab_no):

        tk.Frame.__init__(self, master)
        self.master = master
        self.tab = tab
        self.tab_no = tab_no

        #Separate Functions for Tabs
        if self.tab_no == 1: # UNIAX TAB
            button4 = Button(self.master, text="Good", bg='green',
                             command=self.write_analysis)
            button4.grid(row=0, column=0, sticky='w')

            changeLabel = Label(self.master, text="Properties to Change")
            changeLabel.grid(row=0, column=1)

            button5 = Button(self.master, text="Ultimate Stress",
                             command=self.get_uts)
            button5.grid(row=1, column=1)

            button5 = Button(self.master, text="Linear Stiffness",
                             command=self.get_linear)
            button5.grid(row=2, column=1)

        elif self.tab_no == 2:#BIAX TAB
            pass

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
        if self.props.stiffness:
            self.csvDataParser.outputDict[self.props.sample]['Stiffness'] \
                = self.props.stiffness

        else:
            self.csvDataParser.outputDict[self.props.sample]['Stiffness'] \
                = "NaN"

        # Add strength to the list, if not append an empty string
        if self.props.strength:
            self.csvDataParser.outputDict[self.props.sample]['Strength'] \
                = self.props.strength
        else:
            self.csvDataParser.outputDict[self.props.sample]['Strength'] \
                = "NaN"

        # Add all of the trasition props to the output
        transitionProps = self.transitionProps._outputAllValues()

        for prop, val in transitionProps.items():
            self.csvDataParser.outputDict[self.props.sample][prop] = val
            if prop not in self.headersOut:
                self.headersOut.append(prop)

        # print(self.csvDataParser.outputDict[self.props.sample])
        # Write the properties to the csv file specified
        write_props_csv(self.fnameOut, self.csvDataParser.outputDict,
                        self.props.sample, self.headersOut)

        # change the button color after pressed
        self.buttonsdict[self.props.sample].configure(bg="green")

        del self.props

        # Destroy frame5 to get rid of the toolbar
        self.frame5.destroy()

        # Remake the frame to add another toolbar to
        self.frame5 = Frame(self.master, borderwidth=5, relief='raised')
        self.frame5.grid(row=0, column=1, sticky='nsew', ipady=20)
