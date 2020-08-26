from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk, filedialog
import numpy as np
from Data.DataInterface import DataInterfacer

import numpy as np

class BiaxPlotter:
    def __init__(self, dataInterface, tab_no, cls=None, sampleName="No Name"):
        # create a class variable that is the class passed to the function
        self.tab_no = tab_no
        self.cls = cls
        self.sampleName = sampleName
        self.dataInt = dataInterface
        self.TransitionProps = self.dataInt.transitionProps

        self.activePropPlot = {}

        #create a blank plot
        self.fig = plt.figure(1)
        self.ax = self.fig.add_subplot(111)
        self.range, = self.ax.plot([0], [0])

        if self.cls:
            self.setVars()

    def __del__(self):
        #destructor to make sure everything is getting destroyed as it should be
        print("Killing plot instance of: ", self.sampleName)

    def setVars(self):
        #initialize variables for plotting stress and strain
        self.x11 = self.cls.strain[:,0]
        self.x22 = self.cls.strain[:,1]
        self.y11 = self.cls.stress[:,0]
        self.y22 = self.cls.stress[:,1]

        self.failIndx11 = self.cls.failIndx[0]
        self.failIndx22 = self.cls.failIndx[1]

        # create figure for instance of class
        self.get_fig()

        #initialize lists to store x and y data created in function get_fig
        self.xs = list(self.range.get_xdata())
        self.ys = list(self.range.get_ydata())

    def setClass(self, cls, master):
        self.cls = cls
        self.master = master
        BiaxPlotter.master = self.master

        self.setVars()

    def setSample(self, sample):
        self.sampleName = sample

    def set_max_points(self, x11, y11, x22, y22):
        # draw the point on the graph based on the input data
        self.maxPoint11.set_data([x11], [y11])
        self.maxPoint22.set_data([x22], [y22])

        self.maxPoint11.set(marker="o", markersize=8)
        self.maxPoint22.set(marker="o", markersize=8)

        self.maxPoint11.figure.canvas.draw()
        self.maxPoint22.figure.canvas.draw()

    def set_linear_region(self, x, y):

        self.linearRegion.set_data([x], [y])
        self.linearRegion.figure.canvas.draw()

    def remove_prop_plot(self, key):

        if key in self.activePropPlot:
            self.activePropPlot[key].remove()
            del self.activePropPlot[key]
            self.canvas.draw()

    def plot_prop(self,key,propMap,plotparams,direction):
        '''
        Function to parse the checkboxes in the GUI and see which props to plot.
        Properties must be 2 d numpy array where array[..,0] is x value
        '''

        propMap = np.array(propMap)

        if direction == 11:

            val = np.vectorize(self.dataInt.TransitionPropsDict11.get)(propMap)


            # if plotparams['plottype'] == 'line':
            self.activePropPlot[key], = self.ax.plot(val[...,0],val[...,1],
                                    color=plotparams['color'],
                                    marker=plotparams['marker'],
                                    linewidth=plotparams['linewidth'],label='Raymer-Douglas-Peucker Fit')

        elif direction == 22:
            val = np.vectorize(self.dataInt.TransitionPropsDict22.get)(propMap)

            # if plotparams['plottype'] == 'line':
            self.activePropPlot[key], = self.ax.plot(val[...,0],val[...,1],
                                    color=plotparams['color'],
                                    marker=plotparams['marker'],
                                    linewidth=plotparams['linewidth'],label='Raymer-Douglas-Peucker Fit')
        self.canvas.draw()

    def get_fig(self):
        # this function returns a figure for further analysis

        self.fig = plt.figure(1)
        self.ax = self.fig.add_subplot(111)  # create an axis over the subplot

        self.ax.set_title(self.sampleName)  # set the title to the current sample

        # axes titles
        self.ax.set_xlabel(self.dataInt.straintype)
        self.ax.set_ylabel(self.dataInt.stresstype)

        self.ax.plot(self.x11, self.y11, color='red', label='E11')  # plot the x and y data
        self.ax.plot(self.x22, self.y22, color='blue', label='E22')
        self.ax.legend()

        self.range, = self.ax.plot([0], [0])  # empty line

        # plot based on the values passed by the class
        self.maxPoint11, = self.ax.plot([0], [0], marker="o")
        self.maxPoint22, = self.ax.plot([0], [0], marker="o")
        self.linearRegion, = self.ax.plot([0], [0])

        self.fig.canvas.callbacks.connect('button_press_event', self)

    def on_click(self, event):

        if event.inaxes is not None:
            print(event.xdata, event.ydata)
        else:
            print('Clicked ouside axes bounds but inside plot window')

    def plot_graph(self, frame1, Row=1, Col=1):
        # Make the canvas to put the plot on
        self.canvas = FigureCanvasTkAgg(self.fig, frame1)
        # attach a mouse click
        self.range.figure.canvas.mpl_connect('button_press_event', self)
        self.canvas.get_tk_widget().grid(row=Row, column=Col)
        self.canvas._tkcanvas.grid(row=(Row+1), column=Col)
        # self.nav = None
        # self.nav = NavigationToolbar2Tk(self.canvas, frame2)
        self.canvas.draw()
        BiaxPlotter.canvas = self.canvas

    def SetCheckState(self):
        '''
        Callback attached to the check boxes. This runs when a box is checked.
        Runs through all the boxes and updates the plot
        '''

        for property in self.dataInt.CheckboxProps:

            self.remove_prop_plot(property)

            if self.dataInt.CheckboxProps[property].get():

                self._UpdatePlotter(property)

    def _UpdatePlotter(self, prop):

        array = self.dataInt.propertyMap[prop]
        self.plot_prop(prop, array, self.dataInt.propertyPlotArgs[prop], direction=11)
        self.plot_prop(prop, array, self.dataInt.propertyPlotArgs[prop], direction=22)
