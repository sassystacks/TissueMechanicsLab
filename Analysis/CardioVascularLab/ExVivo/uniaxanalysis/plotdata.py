from matplotlib import pyplot as plt


class DataPlotter:
    def __init__(self, cls, sampleName="No Name"):

        # create a class variable that is the class passed to the funciton
        self.cls = cls

        # initial variables for plotting stress and strain
        self.x = cls.strain
        self.y = cls.stress

        # Name of the the current sample
        self.sampleName = sampleName

        # Create figure for instance of class
        self.get_fig()

        # initialize lists to store x and y data created in function get_fig
        self.xs = list(self.range.get_xdata())
        self.ys = list(self.range.get_ydata())

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
        print "Killing plot instance of: ", self.sampleName

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

    def get_fig(self):
        # this function returns a figure for further analysis
        self.fig = plt.figure(1)
        self.ax = self.fig.add_subplot(111)  # create an axis over the subplot
        self.ax.set_title(self.sampleName)  # set the title to the current sample
        self.ax.set_xlabel('Engineering Strain')
        self.ax.set_ylabel('Cauchy Stress (MPa)')
        self.ax.plot(self.x, self.y)  # plot the x and y data
        self.range, = self.ax.plot([0], [0])  # empty line
        # plot based on the values passed by the class
        self.maxPoint, = self.ax.plot([0], [0], marker="o")
        self.linearRegion, = self.ax.plot([0], [0])

        self.fig.canvas.callbacks.connect('button_press_event', self)

    def on_click(self, event):

        if event.inaxes is not None:
            print event.xdata, event.ydata
        else:
            print 'Clicked ouside axes bounds but inside plot window'

    def plot_graph(self, frame1, frame2, Row=1, Col=1):
        # this method builds the canvas for the plot and the navigation toolbar
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

        # Make the canvas to put the plot on
        canvas = FigureCanvasTkAgg(self.fig, frame1)

        # attach a mouse click
        self.range.figure.canvas.mpl_connect('button_press_event', self)
        canvas.get_tk_widget().grid(row=Row, column=Col)
        canvas._tkcanvas.grid(row=(Row+1), column=Col)
        NavigationToolbar2TkAgg(canvas, frame2)
        canvas.show()


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
