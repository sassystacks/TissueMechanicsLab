import sys, os
sys.path.append('..')

import tkinter as tk
from tkinter import ttk, filedialog
# from exvivoframes.Frame2 import Frame_2
'''
This frame contains all the folder selection and data parsing functions.
'''
class Frame_1(tk.Frame):

    def __init__(self,master, tab, tab_no):
        tk.Frame.__init__(self, master)
        self.master = master
        self.tab = tab
        self.tab_no = tab_no
        self.ftype = '4Dots_Strain_2PK_1_1.txt'

        self.sampleList = []
        # Dimensions and Directory Path
        self.dim_fname = '/Volumes/Biomechanics_LabShare/NIH_BAV_Project/NIH_BAV_Data/Uniaxial\ Data/NIH_Dimensions.csv'
        self.dirname = '/Volumes/Biomechanics_LabShare/NIH_BAV_Project/NIH_BAV_Data/Uniaxial\ Data/FAIL'

        #Make Buttons
        label = ttk.Label(self.tab, text="Start").grid(sticky = "W")

        button2 = ttk.Button(self.tab, text="Top Directory",
                         command=self.chooseDir)
        button2.grid(sticky = 'W')

        #Separate Functions for Tabs
        if self.tab_no == 1: # UNIAX TAB
            button1 = ttk.Button(self.tab, text="Dimensions File",
                             command=self.chooseDims)
            button1.grid(sticky = 'W')

            button3 = ttk.Button(self.tab, text="Run SetupData",
                             command=self.setupData_uniax)
            button3.grid(sticky = 'W')

        elif self.tab_no == 2:#BIAX TAB

            self.OPTIONS = ["2PK Strain","1PK Stretch","Cauchy Strain"]
            variable = tk.StringVar(self.tab)
            variable.set(self.OPTIONS[0]) # default value

            w = ttk.OptionMenu(self.tab, variable, *self.OPTIONS).grid(row=1,column=0)

            button1 = ttk.Button(self.tab, text="OK", command=self.set_type(variable))
            button1.grid(row=1,column=1)

            button3 = ttk.Button(self.tab, text="Run SetupData",
                             command=self.setupData_biax)
            button3.grid(row=3, column=0)

    def set_type(self,variable):

        ss_type = variable.get()
        if ss_type == self.OPTIONS[0]:
            self.ftype = '4Dots_Strain_2PK_1_1.txt'
        elif ss_type == self.OPTIONS[1]:
            self.ftype = '4Dots_Stretch_1PK_1_1.txt'
        elif ss_type == self.OPTIONS[2]:
            self.ftype = '4Dots_Strain_Cauchy_1_1.txt'

        print(self.ftype)

    def chooseDims(self):

        self.dim_fname = filedialog.askopenfilename()

    def chooseDir(self):

        self.dirname = filedialog.askdirectory()

    def setupData_uniax(self):
        # check if there is an filename for dimensions and Directory

        if self.dim_fname and self.dirname:
            import uniaxanalysis.parsecsv

            #Read in Headers for parsecsv
            self.specimenHeaders = ["Sample", "Zone", "Region", "Specimen", "Direction"]
            self.dimensionHeaders = ["Width","Thickness","Length"]
            self.headersOut = ["Sample", "Zone", "Region", "Specimen", "Direction", "PointID","Strength","Stiffness"]
            self.fileform = ["Sample", "_","Z", "Zone", "Region","Specimen", "_","Direction"] #NIH BAV data

            # Dictionary to pass to parsecsv for obtaining data on specimen
            args_dict = {
                'dimsfile': self.dim_fname,
                'topdir': self.dirname,
                'timestep': 0.05,
                'headersOut': self.headersOut,
                'specimenHeaders': self.specimenHeaders,
                'dimsHeaders': self.dimensionHeaders,
                'fileform': self.fileform,
            }

            # instantiate parsecsv class to get the data to plot and analyze
            self.csvDataParser = uniaxanalysis.parsecsv(**args_dict)

            # Create the list of specimens to be tested from Dimensions file
            self.sampleList = self.csvDataParser.getMatchingData(
                                                    self.csvDataParser.dimsFile,
                                                    self.csvDataParser.topDir)



        else:
            print("please get a directory and a dimensions file for the analysis")

    def setupData_biax(self):
        # check if there is an filename for dimensions and Directory
        # name for the corresponding raw data files
        if self.dim_fname and self.dirname:
            print("true")
        else:
            print("please get a directory and a dimensions file for the analysis")

    def _getAllBiaxFiles(self):

        dirList = os.listdir(self.dirname)

        allFiles = []
        for d in dirList:
            checkDir = os.path.join(topDir,d)
            if os.path.isdir(checkDir):
                subDirList = os.listdir(checkDir)
                for s in subDirList:
                    fullfname = os.path.join(checkDir, s, 'all',
                                            self.ftype)
                    if os.path.isfile(fullfname):
                        allFiles.append(fullfname)
        return allFiles
