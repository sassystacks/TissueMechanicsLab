from Tkinter import *
import tkMessageBox
import ttk
from tkFileDialog import *
import uniaxanalysis.getproperties as getprops
from uniaxanalysis.plotdata import DataPlotter
from uniaxanalysis.saveproperties import write_props_csv

from matplotlib import pyplot as plt

'''
The GUI for uniax data analysis of soft tissue.

inputs:
    - Dimensions file - a file that is formated with the sample name, width, thickness and grip to grip
                        distance
    - directory - Folder with raw uniax data files in csv format

To Do:
    - control when line for manual control shows up
    - work out bug in the 2nd order gaussian
    - work out bug in the display for automatic linear find
    - test rdp for finding linear region
    - fix point picking on plot so that can work in desceding order of x value
'''


class StartPage:

    def __init__(self, master):
        print "Start Page class started"

        self.master = master
        self.buttonsdict = {}
        self.fig = plt.figure(1)

        self.fname = '/home/richard/Documents/School/Research/Uniax/SampleDimensions/dimensions.csv'
        self.dirname = '/home/richard/Documents/School/Research/Fail_files/'
        self.fnameOut = '/home/richard/MyProjects/Mechanical_Testing/TissueMechanicsLab/Analysis/CardioVascularLab/exvivo/MissingSamples.csv'

        '''
        #~~~~~~~~~~~~~~~~~~~~~~~~~ Main Layout ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        '''

        self.frame1 = Frame(self.master, borderwidth=5, relief='raised')
        self.frame1.grid(row=0, column=0, sticky='ew')

        self.frame2 = Frame(self.master, borderwidth=5, relief='raised', height=640)
        self.frame2.grid(row=1, column=0, sticky='N', ipady=20)

        self.frame3 = Frame(self.master, borderwidth=5, relief='raised')
        self.frame3.grid(row=2, column=0, sticky='ew', ipady=20)

        self.frame4 = Frame(self.master, borderwidth=5, relief='raised')
        self.frame4.grid(row=1, column=1, sticky='ew', ipady=20)

        self.frame5 = Frame(self.master, borderwidth=5, relief='raised')
        self.frame5.grid(row=0, column=1, sticky='nsew', ipady=20)

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
        ~~~~~~~~~~~~~~~  close program with escape key  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        '''

        self.master.bind('<Escape>', lambda e: self.master.destroy())

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
        # This function writes the value to a csv and destroys the button object in the GUI

        # Add the sample name to the front of the row
        row_for_csv = [self.props.sample]

        # Add stiffness to the list, if not append an empty string
        if self.props.stiffness:
            row_for_csv.append(self.props.stiffness)
        else:
            row_for_csv.append("NaN")
            tkMessageBox.showwarning("Warning", "No property was specified for stiffness")

        # Add strenght to the list, if not append an empty string
        if self.props.strength:
            row_for_csv.append(self.props.strength)
        else:
            row_for_csv.append("NaN")
            tkMessageBox.showwarning("Warning", "No property was specified for strength")

        # Write the properties to the csv file specified
        write_props_csv(self.fnameOut, row_for_csv)

        # destroy the button
        self.buttonsdict[self.props.sample].destroy()

        # This is a hack and could be done better.... just need to get analysis done right now

        # Destroy frame5 to get rid of the toolbar
        self.frame5.destroy()

        # Remake the frame to add another toolbar to
        self.frame5 = Frame(self.master, borderwidth=5, relief='raised')
        self.frame5.grid(row=0, column=1, sticky='nsew', ipady=20)

    def chooseDims(self):

        self.fname = askopenfilename()

    def chooseDir(self):

        self.dirname = askdirectory()

    def setupData(self):
        # check if there is an fname and a dirname
        if self.fname and self.dirname:
            import uniaxanalysis.parsecsv
            # Dictionary to pass to parsecsv for obtaining dta on specimen
            args_dict = {
                'dimsfile': self.fname,
                'topdir': self.dirname,
                'timestep': 0.05

            }

            # instantiate parsecsv class to get the data to plot and analyze
            inst = uniaxanalysis.parsecsv(**args_dict)

            # Create the list of specimens to be tested from Dimensions file
            self.sampleList = inst.getMatchingData(inst.dimsFile, inst.topDir)

            self.addButtons()
        else:
            print("please get a directory and a dimensions file for the analysis")

    def addButtons(self):

        # place a button for each sample in a panel

        import math
        # create button names from each sample in the list
        buttonnames = [name[0] for name in self.sampleList]

        # Make 3 columns of buttons
        row = math.ceil(len(buttonnames)/3)
        col = 3
        padlist = [(i, j) for i in range(int(row)) for j in range(col)]
        diff = len(padlist) - len(buttonnames)

        if diff > 0:
            padlist = padlist[:-diff]

        # Create a rectangular list of objects to store all of the sample names as
        # tk button objects
        fullList = zip(buttonnames, padlist)

        for name, indx in fullList:
            self.buttonsdict[name] = Button(self.frame2, text=name)
            self.buttonsdict[name]['command'] = lambda sample = name: self.getGraph(sample)
            self.buttonsdict[name].grid(row=indx[0], column=indx[1])

    def getGraph(self, samplename):
        self.fig.clear()

        # Iterate through sample list to find matching sample
        for sample in self.sampleList:

            if samplename == sample[0]:
                # Get all of the properties for this sample
                self.props = getprops(fileDimslist=sample, smooth_width=29,
                                      std=7, chkderivate=0.04, stresstype="Cauchy")

                # create an instance of DataPlotter class and pass instance of
                # getproperties
                self.plotter = DataPlotter(self.props,  sample[0])

                break
        else:
            print "Couldn't find the file"

        canvas = self.plotter.plot_graph(self.frame4, self.frame5, Row=0, Col=0)


def main():

    root = Tk()
    mainApp = StartPage(root)
    root.attributes('-fullscreen', True)
    # root.geometry("500x500")

    root.mainloop()


if __name__ == '__main__':
    main()
