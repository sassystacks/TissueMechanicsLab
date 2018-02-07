from Tkinter import *
import ttk
import uniaxanalysis.getproperties as up
from matplotlib import pyplot as plt

class StartPage:

    def __init__(self, master):
        print "Start Page class started"

        self.master = master
        self.buttonsdict = {}
        self.fig = plt.figure(1)

        #These attributes are passed to parsecsv
        self.fname = '/home/richard/MyProjects/TissueMechanicsLab/RawData/Allfiles.csv'
        self.dirname = '/home/richard/MyProjects/TissueMechanicsLab/CleanSheets'

        #~~~~~~~~~~~~~~~~~~~~~ Initialize Frames ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.frame1 = Frame(self.master,borderwidth =5,relief='raised')
        self.frame1.grid(row=0,column=0,sticky='ew')

        self.frame2 = Frame(self.master,borderwidth =5,relief='raised')
        self.frame2.grid(row=1,column=0,sticky='N',ipady=20)

        self.frame3 = Frame(self.master,borderwidth =5,relief='raised')
        self.frame3.grid(row=1,column=1,sticky='ew',ipady=20)

        self.frame4 = Frame(self.master,borderwidth =5,relief='raised')
        self.frame4.grid(row=2,column=0,sticky='ew',ipady=20)


        #~~~~~~~~~~~~~~~~~~~~~~~~~ Widgets ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        label = Label(self.frame1, text="Start Page")
        label.grid(row=0,column=0)

        button1 = Button(self.frame1, text="Dimensions File",
                                command = self.chooseDims)
        button1.grid(row=1,column=0)

        button2 = Button(self.frame1, text="Top Directory",
                                command = self.chooseDir)
        button2.grid(row=2,column=0)

        button3 = Button(self.frame1, text="Run SetupData",
                                command = self.setupData)
        button3.grid(row=3,column=0)

        button4 = Button(self.frame4, text="Too Shitty",
                                command = self.destroyPlot)
        button4.grid(row=0,column=0)

        '''
        ~~~~~~~~~~~~~~~  close program with escape key  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        '''
        self.master.bind('<Escape>', lambda e: self.master.destroy())

    def chooseDims(self):

        self.fname = askopenfilename()

    def chooseDir(self):

        self.dirname = askdirectory()

    def setupData(self):
        import uniaxanalysis.parsecsv
        #Dictionary to pass to parsecsv for obtaining dta on specimen
        args_dict = {
                    'dimsfile':self.fname,
                    'topdir':self.dirname,
                    'timestep': 0.15
                    }
        inst =  uniaxanalysis.parsecsv(**args_dict)
        #Create the list of specimens to be tested from Dimensions file
        self.sampleList =inst.getMatchingData(inst.dimsFile,inst.topDir)
        self.addButtons()


    def addButtons(self):

        import math
        buttonnames = [name[0] for name in self.sampleList]

        #Make 3 columns of buttons
        row = math.ceil(len(buttonnames)/3)
        col = 3
        padlist = [(i,j) for i in range(int(row)) for j in range(col)]
        diff = len(padlist) - len(buttonnames)

        if diff > 0:
            padlist = padlist[:-diff]

        fullList = zip(buttonnames,padlist)


        for name, indx in fullList:
            self.buttonsdict[name] = Button(self.frame2,text=name)
            self.buttonsdict[name]['command'] = lambda sample = name: self.getGraph(sample)
            self.buttonsdict[name].grid(row=indx[0],column=indx[1])

    def getGraph(self,samplename):
        self.fig.clear()
        #Iterate through sample list to find matching sample
        for item in self.sampleList:

            if samplename == item[0]:            
                self.fig= up(fileDimslist = item,smooth_width=59).visualizeData(1,2)# Call uniaxanalysis.properties()
                break
        else:
            print "Couldn't find the file"

        self.plotGraph()



    def plotGraph(self):
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


        self.frame3 = Frame(self.master,borderwidth =5,relief='raised')
        self.frame3.grid(row=1,column=1,sticky='ew',ipady=20)

        canvas = FigureCanvasTkAgg(self.fig, self.frame3)
        canvas.show()
        canvas.get_tk_widget().grid(row=0, column=0)

    def destroyPlot(self):
        for widget in self.frame3.winfo_children():
            widget.destroy()
        #Destroy frame3 and rebuild
        self.frame3.destroy()

def main():

    root = Tk()
    mainApp = StartPage(root)
    #root.attributes('-fullscreen',True)
    root.geometry("500x500")
    root.mainloop()

if __name__ == '__main__':
    main()
