import sys
sys.path.append('..')

import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk, filedialog
import uniaxanalysis.getproperties as getprops
from uniaxanalysis.plotdata import DataPlotter
from uniaxanalysis.saveproperties import write_props_csv
import exvivoframes.Frame1 as evf1
from matplotlib import pyplot as plt
from Data.DataInterface import DataInterfacer



import time
'''
This frame makes the buttons for choosing which test you would like to view in the canvas.
Takes sample list from DataInterface.py.
'''
class Frame_2(tk.Frame):

    def __init__(self, master, tab, tab_no, dataInterface):

        tk.Frame.__init__(self, master)
        self.master = master
        self.tab = tab
        self.tab_no = tab_no
        self.dataInt = dataInterface
        self.sampleList = self.dataInt.sampleList
        self.buttonsdict = {}


        self.buttonCanvas = Canvas(self.master)
        self.xButtonScroller = Scrollbar(self.master, orient="horizontal",
                                         command=self.buttonCanvas.xview)
        self.yButtonScroller = Scrollbar(self.master,
                                         command=self.buttonCanvas.yview)
        self.buttonFrame = Frame(self.buttonCanvas)

        self.buttonCanvas.create_window((4, 10), window=self.buttonFrame, anchor="nw",
                                        tags="self.frame")

        self.buttonFrame.bind("<Configure>", self.onFrameConfigure)

        self.buttonCanvas.config(yscrollcommand=self.yButtonScroller.set)
        self.buttonCanvas.config(xscrollcommand=self.xButtonScroller.set)

        self.buttonCanvas.grid(row=0, column=0, sticky='nwse')
        self.yButtonScroller.grid(row=0, column=1, sticky='ns')
        self.xButtonScroller.grid(row=1, column=0, sticky='ew')

        # Separate functions for tabs
        if self.tab_no == 1:  # UNIAX TAB
            global addButton1
            addButton1 = ttk.Button(self.tab, text="Add Buttons", width=20,
                                 command=self.addButtons)
            addButton1.grid(sticky='N', pady = 100)

        elif self.tab_no == 2:  # BIAX TAB
            global addButton2
            addButton2 = ttk.Button(self.tab, text="Add Buttons", width=20,
                                 command=self.addButtons)
            addButton2.grid(sticky='N', pady=100)

    def addButtons(self):
        # place a button for each sample in a panel

        import math

        # create button names from each sample in the list
        buttonnames = [name[0] for name in self.dataInt.sampleList]

        # Make 3 columns of buttons
        row = math.ceil(len(buttonnames)/3.0)
        col = 3
        padlist = [(i, j) for i in range(int(row)) for j in range(col)]
        diff = len(padlist) - len(buttonnames)

        if diff > 0:
            padlist = padlist[:-diff]

        # Create a rectangular list of objects to store all of the sample names as
        # tk button objects
        fullList = zip(buttonnames, padlist)
        #
        for name, indx in fullList:
            self.buttonsdict[name] = tk.Button(self.buttonFrame, text=name)
            self.buttonsdict[name]['command'] = lambda sample = name: self.dataInt.setSample(sample)
            self.buttonsdict[name].grid(row=indx[0], column=indx[1])

        addButton1.destroy()
        addButton2.destroy()
        self.dataInt.setButtonsDict(self.buttonsdict)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.buttonCanvas.configure(scrollregion=self.buttonCanvas.bbox("all"))