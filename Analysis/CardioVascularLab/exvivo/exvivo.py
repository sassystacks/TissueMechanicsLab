# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import Tkinter as tk
import ttk
from tkFileDialog   import askopenfilename,askdirectory

LARGE_FONT= ("Verdana", 12)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):

        print "Main class started"
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Sea of BTC client")



        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage(container,self)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        # for F in (StartPage, PageOne, PageTwo, PageThree):
        #
        #     frame = F(container, self)
        #
        #     self.frames[F] = frame
        #
        #     frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        print "Start Page class started"
        tk.Frame.__init__(self,parent)

        #These attributes are passed to parsecsv
        self.fname = '/home/richard/MyProjects/TissueMechanicsLab/RawData/Allfiles.csv'
        self.dirname = '/home/richard/MyProjects/TissueMechanicsLab/CleanSheets'

        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Dimensions File",
                                command = self.chooseDims)
        button1.pack()

        button2 = ttk.Button(self, text="Top Directory",
                                command = self.chooseDir)
        button2.pack()

        button3 = ttk.Button(self, text="Run SetupData",
                                command = self.setupData)
        button3.pack()

        # button = ttk.Button(self, text="Visit Page 1",
        #                     command=lambda: controller.show_frame(PageOne))
        # button.pack()


    def chooseDims(self):

        self.fname = askopenfilename()

    def chooseDir(self):

        self.dirname = askdirectory()

    def setupData(self):
        import uniaxanalysis.parsecsv
        #Dictionary to pass to parsecsv for obtaining dta on specimen
        args_dict = {
                    'dimsfile':self.fname,
                    'topdir':self.dirname
                    }
        inst =  uniaxanalysis.parsecsv(**args_dict)
        #Create the list of specimens to be tested from Dimensions file
        self.sampleList =inst.getMatchingData(inst.dimsFile,inst.topDir)
        self.addButtons()


    def addButtons(self):

        import math
        buttonnames = [name[0] for name in self.sampleList]

        sqr = math.sqrt(len(buttonnames))
        sqr = int(math.ceil(sqr))

        padlist = [(i,j) for i in range(sqr) for j in range(sqr)]
        diff = len(padlist) - len(buttonnames)

        if diff > 0:
            padlist = padlist[:-diff]

        fullList = zip(buttonnames,padlist)

        for name, indx in fullList:
            ttk.Button(self,text=name).pack()






class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        print "Start Page 1 class started"
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        print "Start Page 2 class started"
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
        print "This started"



        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



app = SeaofBTCapp()
app.mainloop()
