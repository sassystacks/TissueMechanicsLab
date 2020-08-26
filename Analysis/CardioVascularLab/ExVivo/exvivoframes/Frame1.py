import sys, os
sys.path.append('..')

import tkinter as tk
from tkinter import ttk, filedialog
from Data.DataInterface import DataInterfacer

'''
This frame contains folder selection and data parsing. It interacts with DataInterface.py to get the
sample list. 
'''

class Frame_1(tk.Frame):

    def __init__(self, master, tab, tab_no, dataInterface):

        tk.Frame.__init__(self, master)

        self.master = master
        self.tab = tab
        self.tab_no = tab_no
        self.dataInt = dataInterface
        self.dataInt.setTabNumber(self.tab_no)

        #make buttons
        label = ttk.Label(self.tab, text="Start").grid(sticky = "N")

        button2 = ttk.Button(self.tab, text="Top Directory",
                         width = 20, command=self.chooseDir)
        button2.grid(sticky = 'N')

        #separate functions for tabs
        if self.tab_no == 1:  # UNIAX TAB
            self.dim_fname = '/Volumes/Biomechanics_LabShare/NIH_BAV_Project/NIH_BAV_Data/Uniaxial\ Data/NIH_Dimensions.csv'
            self.dirname = '/Volumes/Biomechanics_LabShare/NIH_BAV_Project/NIH_BAV_Data/Uniaxial\ Data/FAIL'

            button1 = ttk.Button(self.tab, text="Dimensions File", width = 20,
                                 command=self.chooseDims)
            button1.grid(sticky='N')

            button3 = ttk.Button(self.tab, text="Run SetupData", width = 20,
                                 command=self.getData_uniax)
            button3.grid(sticky='N')

        elif self.tab_no == 2:  # BIAX TAB
            self.ftype = '4Dots_Strain_2PK_1_1.txt'
            self.dirname = '/Volumes/Biomechanics_LabShare/NIH_BAV_Project/NIH_BAV_Analysis/Biaxial 1st Analysis/NIH_BAV_013'
            self.dataType = 'Binned'

            self.OPTIONS = ["Analysis Type", "2PK Strain", "1PK Stretch", "Cauchy Strain"]
            self.variable = tk.StringVar(self.tab)
            self.variable.set(self.OPTIONS[0])  # default value

            w = ttk.OptionMenu(self.tab, self.variable, *self.OPTIONS)
            w.grid(row=2, column=0)
            w.config(width=15)

            button1 = ttk.Button(self.tab, text="OK", width = 20, command=self.variable.trace("w", self.set_type))
            button1.grid(row=2, column=1, sticky='W')

            self.dataOPTIONS = ["Data Type", "Binned", "Unbinned"]
            self.dataVariable = tk.StringVar(self.tab)
            self.dataVariable.set(self.dataOPTIONS[0])

            w = ttk.OptionMenu(self.tab, self.dataVariable, *self.dataOPTIONS)
            w.grid(row=3, column=0)
            w.config(width=15)

            button3 = ttk.Button(self.tab, text="OK", width=20,
                                 command=self.dataVariable.trace("w", self.set_dataType))
            button3.grid(row=3, column=1, sticky='W')

            button4 = ttk.Button(self.tab, text="Run SetupData", width = 20,
                                 command=self.getData_biax)
            button4.grid(row=4, column=0)

    def chooseDims(self):
        self.dim_fname = filedialog.askopenfilename()

    def chooseDir(self):
        self.dirname = filedialog.askdirectory()

    def getData_uniax(self): #TAB1

        # check if there is an filename for dimensions and Directory

        if self.dim_fname and self.dirname:
            import uniaxanalysis.parsecsv

            # Read in Headers for parsecsv
            self.specimenHeaders = ["Sample", "Zone", "Region", "Specimen", "Direction"]
            self.dimensionHeaders = ["Width", "Thickness", "Length"]
            self.headersOut = ["Sample", "Zone", "Region", "Specimen", "Direction", "PointID", "Strength", "Stiffness"]
            self.fileform = ["Sample", "_", "Z", "Zone", "Region", "Specimen", "_", "Direction"]  # NIH BAV data

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

            # set data interface sample list and csv data parser
            self.dataInt.setSampleList(self.sampleList)
            self.dataInt.setCSVDataParser(self.csvDataParser, self.specimenHeaders,
                                          self.dimensionHeaders, self.headersOut, self.fileform)

        else:
            print("please get a directory and a dimensions file for the analysis")

    def set_type(self, *args):
        ss_type = self.variable.get()
        if ss_type == "2PK Strain":
            self.ftype = '4Dots_Strain_2PK_1_1.txt'
            self.stresstype = '2PK (Pa)'
            self.straintype = 'Strain'
        elif ss_type == "1PK Stretch":
            self.stresstype = '1PK (Pa)'
            self.straintype = 'Stretch'
            self.ftype = '4Dots_Stretch_1PK_1_1.txt'
        elif ss_type == "Cauchy Strain":
            self.ftype = '4Dots_Strain_Cauchy_1_1.txt'
        self.dataInt.setftypeBiax(self.ftype)
        self.dataInt.setStressStrainType(self.stresstype, self.straintype)
        return self.ftype

    def set_dataType(self, *args):
        inputData = self.dataVariable.get()
        if inputData == "Binned":
            self.dataType = "Binned"
        elif inputData == "Unbinned":
            self.dataType = "Unbinned"
        self.dataInt.setDataTypeBiax(self.dataType)
        return self.dataType

    def getData_biax(self):
        if self.dirname:
            from biax.GetBiaxData import ReadBiaxData

            # read in headers for ReadBiaxData (need to run setupData binned vs unbinned
            # to get the correct headers)
            self.biaxHeaders = []
            self.biaxHeadersOut = []

            if self.dataType == "Binned":
                self.setupData_biax_binned()
            elif self.dataType == "Unbinned":
                self.setupData_biax_unbinned()

            # dictionary to pass to ReadBiaxData for obtaining data on specimen
            args_dict = {
                'topdir': self.dirname,
                'timestep': 0.05,
                'headersOut': self.biaxHeadersOut,
                'specimenHeaders': self.biaxHeaders,
                'ftype': self.ftype,
                'datatype': self.dataType
            }

            # instantiate biaxDataReader class to get the data to plot and analyze
            self.BiaxDataParser = ReadBiaxData(**args_dict)

            # create list of specimens
            self.sampleList = self.BiaxDataParser._makeSampleList(self.BiaxDataParser.sampleNames,
                                                                 self.BiaxDataParser.fileList)

            self.dataInt.setSampleList(self.sampleList)

        else:
            print("Please choose a directory for analysis")


    def setupData_biax_binned(self):

        # read in headers
        self.biaxHeaders = ["Time", "E11(dots)", "E22(dots)", "S11", "S22"]
        self.biaxHeadersOut = ["Sample", "Direction", "LTM_", "HTM_", "MaxStress_", "T_Stress_Start_",
                                   "T_Strain_Start_", "T_Stress_End_", "Elbow_Region_"]

        return self.biaxHeaders, self.biaxHeadersOut

    def setupData_biax_unbinned(self):

        # read in headers
        self.biaxHeaders = ["Time", "E11(dots)", "E22(dots)", "T11", "T22"]
        self.biaxHeadersOut = ["Sample", "Direction", "LTM_", "HTM_", "MaxStress_", "T_Stress_Start_",
                                   "T_Strain_Start_", "T_Stress_End_", "Elbow_Region_"]

        return self.biaxHeaders, self.biaxHeadersOut





