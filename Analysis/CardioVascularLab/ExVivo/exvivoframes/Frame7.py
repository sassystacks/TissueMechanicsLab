import tkinter as tk
'''
This frame contains all the check box properties. The class also maps the
checkbox to the properties in the dictionary containing them. Dictionary is
output from the TransitionProperties class.
'''

class Frame_7(tk.Frame):

    def __init__(self,master,cls,defaultState=0):
        tk.Frame.__init__(self, master)
        self.master = master

        self.plotter = cls

        self.title = "Output Properties"
        self.canvas = tk.Canvas(self.master)

        self.varState = defaultState

        self.properties = {}

        self.propertyMap = {'Strength':       ['MaxStrain_',
                                                'MaxStress_'],
                            'High Stiffness': 'HighStiffness',
                            'Low Stiffness':  [['StartStrain',
                                               'StartStress'],
                                              ['T_Strain_Start_',
                                               'T_Stress_Start_']],
                           'Transition Start':['T_Strain_Start_',
                                               'T_Stress_Start_'],
                           'Transition End':  ['T_Strain_End_',
                                                'T_Stress_End_'],
                           'Raymer-Douglas-Peucker':'RDP'
                           }
        self.propertyPlotArgs = {'Strength':  {'color': 'c', 'marker': 'x',
                                          'plottype':'scatter','linewidth':7,
                                          'tkColor':'cyan'},
                        'High Stiffness': {'color': 'm', 'marker': None,
                                            'plottype':'line','linewidth':5,
                                            'tkColor':'magenta'},
                        'Low Stiffness':  {'color': 'g', 'marker': None,
                                            'plottype':'line','linewidth':5,
                                            'tkColor':'green'},
                        'Transition Start':{'color': 'r', 'marker': 'o',
                                            'plottype':'scatter','linewidth':5,
                                            'tkColor':'red'},
                        'Transition End':  {'color': 'r', 'marker': 'o',
                                            'plottype':'scatter','linewidth':5,
                                            'tkColor':'red'},
                        'Raymer-Douglas-Peucker':{'color': 'b', 'marker': None,
                                            'plottype':'line','linewidth':4,
                                            'tkColor':'blue'}
                           }
        self.checkButtons = {}

        self._CreateCheckButtons()


    def _CreateCheckButtons(self):

        for i,property in enumerate(self.propertyMap):

            self.properties[property] = tk.IntVar(value=self.varState)
            self.checkButtons[property] = tk.Checkbutton(
                self.canvas, text=property,
                variable=self.properties[property],
                command=self._SetCheckState,
                activebackground=self.propertyPlotArgs[property]['tkColor'],
                anchor='w')
            self.checkButtons[property].grid(row=i,column=0,sticky='we',ipady=20)


        self.canvas.grid(row=0,column=0)

    def _BuildColorCircle(self):
        self.master.update()
        for prop in self.checkButtons:
            x = self.checkButtons[prop].winfo_x()
            y = self.checkButtons[prop].winfo_y()
            # widgetWidth = self.checkButtons[prop].winfo_width()

            radius = 5

            offset = 160
            x0 = x - radius + offset
            x1 = x + radius + offset
            y0 = y - radius
            y1 = y + radius

            color = self.propertyPlotArgs[prop]['circleColor']

            self.canvas.create_oval(x0, y0, x1, y1, fill=color)

    def _SetCheckState(self):
        '''
        Callback attached to the check boxes. This runs when a box is checked.
        Runs through all the boxes and updates the plot
        '''

        for property in self.properties:

            self.plotter.remove_prop_plot(property)

            if self.properties[property].get():

                self._UpdatePlotter(property)



    def _UpdatePlotter(self, prop):
        array = self.propertyMap[prop]
        self.plotter.plot_prop(prop,array,self.propertyPlotArgs[prop])

        # val = np.vectorize(self.propertyMap.get)(array)
        # print(val)
        # self.plotter.plot_prop(prop,val)
