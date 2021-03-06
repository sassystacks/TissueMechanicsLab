from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import numpy as np

class DataPlotter:
    def __init__(self, cls=None, sampleName="No Name", props={}):

        # create a class variable that is the class passed to the funciton
        self.cls = cls
        self.sampleName = sampleName

        self.props = props
        self.activePropPlot = {}

        # Create a blank plot
        self.fig = plt.figure(1)
        self.ax = self.fig.add_subplot(111)  # create an axis over the subplot
        self.range, = self.ax.plot([0], [0])


        if self.cls:
            self.setVars()

    def __call__(self, event):
        # run this when a call to this function is made, by clicking inside the graph

        # check if the mouse click is in
        if event.inaxes != self.range.axes:
            return

        # if the length of the points returned by clicking is more than 2,
        # replace the second click with the newest click
        if len(self.xs) >= 2 or len(self.ys) >= 2:
            self.xs[0] = self.xs[1]
            self.ys[0] = self.ys[1]
            self.xs[1] = event.xdata
            self.ys[1] = event.ydata

        # if haven't made 2 clicks just append the data
        else:
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)

        # update the range with the new data

        self.range.set_data(self.xs, self.ys)
        self.range.figure.canvas.draw()

    def __del__(self):
        # destructor to make sure everything is getting destroyed as should be
        print("Killing plot instance of: ", self.sampleName)

    def setVars(self):
        # initial variables for plotting stress and strain
        self.x = self.cls.strain
        self.y = self.cls.stress

        # get the variables of interest from the class passed to the function
        self.secondDer = self.cls.secondDer

        # Get the index of the failure point
        self.failIndx = self.cls.failIndx

        # Get the indices of the linear region
        linRegion = self.cls.linearRange
        self.startLin = linRegion[0]
        self.endLin = linRegion[1]


        # get the values for the linear region
        self.xLine = self.cls.xline
        self.yLine = self.cls.yline

        # Create figure for instance of class
        self.get_fig()

        # initialize lists to store x and y data created in function get_fig
        self.xs = list(self.range.get_xdata())
        self.ys = list(self.range.get_ydata())

    def setClass(self,cls):
        self.cls = cls

        self.setVars()

    def setSample(self,sample):
        self.sampleName = sample

    def set_max_point(self, x, y):
        # draw the point on the graph based on the input data
        self.maxPoint.set_data([x], [y])
        print(x, y)
        # print(self.maxPoint.get_data())
        self.maxPoint.set(marker="o", markersize=8)
        self.maxPoint.figure.canvas.draw()

    def set_linear_region(self, x, y):

        self.linearRegion.set_data([x], [y])
        self.linearRegion.figure.canvas.draw()

    def set_props(self,props):
        self.props = props

    def remove_prop_plot(self, key):

        if key in self.activePropPlot:
            self.activePropPlot[key].remove()
            del self.activePropPlot[key]
            self.canvas.draw()

    def plot_prop(self,key,propMap,plotparams):
        '''
        Function to parse the checkboxes in the GUI and see which props to plot.
        Properties must be 2 d numpy array where array[..,0] is x value
        '''
        propMap = np.array(propMap)
        val = np.vectorize(self.props.get)(propMap)

        # if plotparams['plottype'] == 'line':
        self.activePropPlot[key], = self.ax.plot(val[...,0],val[...,1],
                                    color=plotparams['color'],
                                    marker=plotparams['marker'],
                                    linewidth=plotparams['linewidth'],label='Raymer-Douglas-Peucker Fit')

        '''
        Plot some vertical lines to show where stuff is.... delete after thesis
        is written.
        '''
        # self.ax.vlines(val[...,0][1],min(val[...,1]),max(val[...,1]),
        #                     color='m',
        #                     linestyle='--',linewidth=3,label="Transition Start")
        # self.ax.vlines(val[...,0][-2],min(val[...,1]),max(val[...,1]),
        #                     linestyle='--',linewidth=3,label="Transition End",
        #                     color='r')
        # self.ax.legend(loc='best')
        # elif plotparams['plottype'] == 'scatter':
        #     self.activePropPlot[key], = self.ax.scatter(val[...,0],val[...,1])

        # print('In Plotter {0}:{1}'.format(key,val))

        self.canvas.draw()


    def get_fig(self):
        # this function returns a figure for further analysis

        self.fig = plt.figure(1)
        self.ax = self.fig.add_subplot(111)  # create an axis over the subplot

        self.ax.set_title(self.sampleName)  # set the title to the current sample

        # These are the titles Muba
        self.ax.set_xlabel('Engineering Strain')
        self.ax.set_ylabel('Cauchy Stress (MPa)')

        self.ax.plot(self.x, self.y)  # plot the x and y data

        '''
        This commented out part runs the original strength and stiffness calcs
        '''
        # self.ax.scatter(self.x[self.failIndx],self.y[self.failIndx], c="m", s=150,
        #                 marker="+", linewidths=8,label='Failure')
        # self.ax.plot(self.x[:self.failIndx],self.secondDer,label='Gaussian Convolution')
        # self.ax.plot(self.xLine,self.yLine,c="r",label='Linear Prior To Failure')
        # self.ax.vlines(self.xLine[0],min(self.secondDer),self.y[self.failIndx],linestyle='--',color='k')
        # self.ax.vlines(self.xLine[-1],min(self.secondDer),self.y[self.failIndx],linestyle='--',color='k')
        # self.ax.legend()
        # comment to here

        self.range, = self.ax.plot([0], [0])  # empty line
        # plot based on the values passed by the class
        self.maxPoint, = self.ax.plot([0], [0], marker="o")
        self.linearRegion, = self.ax.plot([0], [0])

        self.fig.canvas.callbacks.connect('button_press_event', self)



    def on_click(self, event):

        if event.inaxes is not None:
            print(event.xdata, event.ydata)
        else:
            print('Clicked ouside axes bounds but inside plot window')

    def plot_graph(self, frame1, frame2, Row=1, Col=1):
        # import matplotlib as mpl
        # mpl.use("TkAgg")
        # this method builds the canvas for the plot and the navigation toolbar

        # Make the canvas to put the plot on
        self.canvas = FigureCanvasTkAgg(self.fig, frame1)

        # attach a mouse click
        self.range.figure.canvas.mpl_connect('button_press_event', self)
        self.canvas.get_tk_widget().grid(row=Row, column=Col)
        self.canvas._tkcanvas.grid(row=(Row+1), column=Col)
        # self.nav = None
        # self.nav = NavigationToolbar2Tk(self.canvas, frame2)
        self.canvas.draw()

'''
 def main(self):
        self.fig = plt.figure()
        self.fig = plt.figure(figsize=(3.5,3.5))

        self.frame = Tkinter.Frame(self)
        self.frame.pack(padx=15,pady=15)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)

        self.canvas.get_tk_widget().pack(side='top', fill='both')

        self.canvas._tkcanvas.pack(side='top', fill='both', expand=1)

        self.toolbar = NavigationToolbar2TkAgg( self.canvas, self )
        self.toolbar.update()
        self.toolbar.pack()

        self.btn = Tkinter.Button(self,text='button',command=self.alt)
        self.btn.pack(ipadx=250)

        self.draw_sphere()
'''
