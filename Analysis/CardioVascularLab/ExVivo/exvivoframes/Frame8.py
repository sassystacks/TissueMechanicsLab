import tkinter as tk

class Frame_8(tk.Frame):
    '''
    Frame 8, at the moment, is only for changing the value of the epsilon to
    change the fit of the rdp algorithm to the data.
    '''

    def __init__(self, master, transitionclass):
        tk.Frame.__init__(self,master)

        self.master = master
        self.transition = transitionclass

        self.canvas = tk.Canvas(master)

        defaultTest = tk.StringVar(value="0.01")
        self.epsilonEntry = tk.Entry(self.canvas,
                                    textvariable=defaultTest)
        # self.epsilonEntry.setvar("0.01")
        self.epsilonTitle = tk.Label(self.canvas, text="RDP Epsilon")

        self.canvas.pack(fill='both',expand=True)
        self.epsilonTitle.grid(row=0,column=0,sticky='nw')
        self.epsilonEntry.grid(row=0,column=1,sticky='nw')
        print("epsilon",self.epsilonEntry.get())

        self._UpdateEpsilonCallback()

    def _UpdateEpsilonCallback(self):

        self.transition.epsilon = float(self.epsilonEntry.get())
