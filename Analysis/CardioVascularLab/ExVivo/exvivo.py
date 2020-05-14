import sys
sys.path.append('..')

from Analyzer.TransitionProperties import ProcessTransitionProperties

from tkinter import *
from tkinter import messagebox, ttk, filedialog
# from tkFileDialog import *
import uniaxanalysis.getproperties as getprops
from uniaxanalysis.plotdata import DataPlotter
from uniaxanalysis.saveproperties import write_props_csv
from exvivoframes import *


from matplotlib import pyplot as plt

import time

'''
The GUI for uniax data analysis of soft tissue.

inputs:
    - Dimensions file - a file with format: sample name, width, thickness and initial distance
    - directory - Folder with raw uniax data files in csv format with format: time, distance, force

To Do:
    - polymorphic method for handling input data (variable names to get) <done>
    - control when line for manual control shows up <done>
    - test rdp for finding linear region - done (check implementation)
    - fix point picking on plot so that can work in desceding order of x value - <done>
    - tick boxes for properties
    - config file
    - scroll bar for large data sets

Bugs:
    - work out bug in the 2nd order gaussian - done
    - work out bug in the display for automatic linear find
    - destroy instance of toolbar on graph create
    - destroy instance of plot everytime
'''

class StartPage:

    def __init__(self, master):
        # print "Start Page class started"

        # Some properties that Rubab and Mohammaded complained soooooooooo much
        # to get..... jesus Muba
        self.straintype = 'engineering' # can change to engineering, and lamda
        self.stresstype = 'cauchy' # can change between cauchy and piola

        self.master = master
        self.buttonsdict = {}
        self.fig = plt.figure(1)
        self.transitionProps = ProcessTransitionProperties(eps=0.008)
        self.plotter = DataPlotter()



        # For Data Extraction
        self.specimenHeaders = ["Sample", "Zone", "Region", "Specimen", "Direction"]
        self.dimensionHeaders = ["Width","Thickness","Length"]

        self.headersOut = ["Sample", "Zone", "Region", "Specimen", "Direction",
                            "PointID","Strength","Stiffness"]

        # this is the format of file so
        self.fileform = ["Sample", "_", "Zone", "Region","Specimen", "Direction"] #AAA data
        # self.fileform = ["Sample", "_","Z", "Zone", "Region","Specimen", "_","Direction"] #NIH BAV data




        self.fname = '/Volumes/Biomechanics_LabShare/Abdominal\ Aortic\ Aneurysms\ Ex-vivo\ testing/Mechanical\ Testing/Uniaxial/2016-Jun10/AAA_Dimensions_2016-Jun10.csv'


        self.dirname = '/Volumes/Biomechanics_LabShare/Abdominal\ Aortic\ Aneurysms\ Ex-vivo\ testing/Mechanical\ Testing/Uniaxial/2016-Jun10/FAIL'

        # test things
        self.fnameOut = 'TestOutputs.csv'

        '''
        #~~~~~~~~~~~~~~~~~~~~~~~~~ Main Layout ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        '''

        border = 3
        self.frame1 = Frame(self.master, borderwidth=border, relief='raised')
        self.frame1.grid(row=0, column=0, sticky='news')

        self.frame2 = Frame(self.master, borderwidth=border, relief='raised')
        self.frame2.grid(row=1, column=0, sticky='news', ipady=20)

        self.frame3 = Frame(self.master, borderwidth=border, relief='raised')
        self.frame3.grid(row=2, column=0, sticky='ew', ipady=20)

        self.frame4 = Frame(self.master, borderwidth=border, relief='raised')
        self.frame4.grid(row=1, column=1, sticky='ew', ipady=20)

        self.frame5 = Frame(self.master, borderwidth=border, relief='raised')
        self.frame5.grid(row=0, column=1, sticky='nsew', ipady=20)

        self.t_frame6 = Frame(self.master, width=200,height=150, relief='raised')
        self.frame6 = Frame6.Frame_6(self.t_frame6)
        self.t_frame6.grid(row=0, column=2,sticky='news')

        self.t_frame7 = Frame(self.master,  borderwidth=border, relief='raised')
        self.frame7 = Frame7.Frame_7(self.t_frame7,self.plotter)
        self.t_frame7.grid(row=1, column=2,sticky='ns', ipady=20)

        self.t_frame8 = Frame(self.master,  borderwidth=border, relief='raised')
        self.frame8 = Frame8.Frame_8(self.t_frame8, self.transitionProps)
        self.t_frame8.grid(row=2, column=2,sticky='ns', ipady=20)

        '''
        ~~~~~~~~~~~~~~~~~~~~~~  Frame 1 Widgets  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        '''

        label = Label(self.frame1, text="Start Page")
        label.grid(row=0, column=0)

        button1 = Button(self.frame1, text="Dimensions File",
                         command=self.chooseDims)
        button1.grid(row=1, column=0)

        button2 = Button(self.frame1, text="Top Directory",
                         command=self.chooseDir)
        button2.grid(row=2, column=0)

        button3 = Button(self.frame1, text="Run SetupData",
                         command=self.setupData)
        button3.grid(row=3, column=0)

        '''
        ~~~~~~~~~~~~~~~~~~~~~~  Frame 2 Widgets  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        '''
        # self.frame2.grid_rowconfigure(0, weight=1)
        # self.frame2.grid_columnconfigure(0, weight=1)
        # self.frame2.grid_propagate(False)


        self.buttonCanvas = Canvas(self.frame2)
        self.xButtonScroller = Scrollbar(self.frame2,orient="horizontal",
                                        command=self.buttonCanvas.xview)
        self.yButtonScroller = Scrollbar(self.frame2,
                                            command=self.buttonCanvas.yview)
        self.buttonFrame = Frame(self.buttonCanvas)

        self.buttonCanvas.create_window((4,10), window=self.buttonFrame, anchor="nw",
                                  tags="self.frame")

        self.buttonFrame.bind("<Configure>", self.onFrameConfigure)

        self.buttonCanvas.config(yscrollcommand=self.yButtonScroller.set)
        self.buttonCanvas.config(xscrollcommand=self.xButtonScroller.set)

        self.buttonCanvas.grid(row=0,column=0,sticky='nwse')
        self.yButtonScroller.grid(row=0,column=1,sticky='ns')
        self.xButtonScroller.grid(row=1,column=0,sticky='ew')


        '''
        ~~~~~~~~~~~~~~~~~~~~~~  Frame 3 Widgets  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        '''

        button4 = Button(self.frame3, text="Good", bg='green',
                         command=self.write_analysis)
        button4.grid(row=0, column=0, sticky='w')

        changeLabel = Label(self.frame3, text="Properties to Change")
        changeLabel.grid(row=0, column=1)

        button5 = Button(self.frame3, text="Ultimate Stress",
                         command=self.get_uts)
        button5.grid(row=1, column=1)

        button5 = Button(self.frame3, text="Linear Stiffness",
                         command=self.get_linear)
        button5.grid(row=2, column=1)

        '''
        ~~~~~~~~~~~~~~~~~~~~~~  Frame 4 Widgets  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        '''
        canvas = self.plotter.plot_graph(self.frame4, self.frame5, Row=0, Col=0)
        '''
        ~~~~~~~~~~~~~~~  key Bindings ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        '''

        self.master.bind('<Escape>', lambda e: self.master.destroy())
        self.master.bind('<Return>', self.frame8._UpdateEpsilonCallback())

    '''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~ Frame 1 functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''

    def chooseDims(self):

        self.fname = filedialog.askopenfilename()

    def chooseDir(self):

        self.dirname = filedialog.askdirectory()

    def setupData(self):
        # check if there is an filename for dimensions and Directory
        # name for the corresponding raw data files
        if self.fname and self.dirname:
            import uniaxanalysis.parsecsv
            # Dictionary to pass to parsecsv for obtaining data on specimen
            args_dict = {
                'dimsfile': self.fname,
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

            self.addButtons()
        else:
            print("please get a directory and a dimensions file for the analysis")

    '''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~ Frame 2 functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''
    def addButtons(self):
        # place a button for each sample in a panel
        import math

        # create button names from each sample in the list
        buttonnames = [name[0] for name in self.sampleList]

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
            self.buttonsdict[name] = Button(self.buttonFrame, text=name)
            self.buttonsdict[name]['command'] = lambda sample = name: self.getGraph(sample)
            self.buttonsdict[name].grid(row=indx[0], column=indx[1])

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.buttonCanvas.configure(scrollregion=self.buttonCanvas.bbox("all"))

    '''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~ Frame 3 functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''


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

        # destroy the button
        self.buttonsdict[self.props.sample].destroy()

        del self.props

        # This is a hack and could be done better.... just need to get analysis done right now

        # Destroy frame5 to get rid of the toolbar
        self.frame5.destroy()

        # Remake the frame to add another toolbar to
        self.frame5 = Frame(self.master, borderwidth=5, relief='raised')
        self.frame5.grid(row=0, column=1, sticky='nsew', ipady=20)

    '''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~ Frame 4 functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''
    def getTransitionProperties(self):
        '''
        This sets all the transition properties for plotting
        '''
        import numpy as np
        stress_strain = np.stack((self.props.strain[:self.props.failIndx],
                                    self.props.stress[:self.props.failIndx]),
                                    axis=-1)
        self.transitionProps._setStressStrain(stress_strain)
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

        canvas = self.plotter.plot_graph(self.frame4, self.frame5, Row=0, Col=0)


def main():

    root = Tk()
    mainApp = StartPage(root)
    root.attributes('-fullscreen', True)
    # root.geometry("500x500")

    root.mainloop()


if __name__ == '__main__':
    main()
