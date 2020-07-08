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

class Widgets:

    def __init__(self, master, tab1, tab2):

        self.master = master
        self.tab1 = tab1
        self.tab2 = tab2
        self.plotter = DataPlotter()

        border = 3

        '''
        #~~~~~~~~~~~~~~~~~~~~~~~~~ Build Tab 1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        '''

        self.t_frame1_t1 = ttk.Frame(self.tab1, borderwidth=border, relief='raised')
        self.frame1_t1 = Frame1.Frame_1(self.t_frame1_t1, self.tab1, 1)
        self.t_frame1_t1.grid(row=0, column=0, sticky='NEWS')

        self.t_frame2_t1 = ttk.Frame(self.tab1, borderwidth=border, relief='raised')
        self.frame2_t1 = Frame2.Frame_2(self.t_frame2_t1, self.tab1, 1)
        self.t_frame2_t1.grid(row=4, column=0, sticky='NEWS', ipady=20)

        self.t_frame3_t1 = ttk.Frame(self.tab1, borderwidth=border, relief='raised')
        self.frame3_t1 = Frame3.Frame_3(self.t_frame3_t1, self.tab1, 1)
        self.t_frame3_t1.grid(row=6, column=0, sticky='EW', ipady=20)

        self.t_frame4_t1 = ttk.Frame(self.tab1, borderwidth=border, relief='raised')
        self.frame4_t1 = Frame4.Frame_4(self.t_frame4_t1, self.tab1, 1)
        self.t_frame4_t1.grid(row=0, column=6, columnspan = 5, rowspan = 5, sticky='EW', ipady=20)

        self.t_frame6_t1 = ttk.Frame(self.tab1, borderwidth=border, relief='raised')
        self.frame6_t1 = Frame6.Frame_6(self.t_frame6_t1, self.tab1, 1)
        self.t_frame6_t1.grid(row=0, column=2, sticky='NEWS', ipady=20)

        self.t_frame7_t1 = ttk.Frame(self.tab1, borderwidth=border, relief='raised')
        self.frame7_t1 = Frame7.Frame_7(self.t_frame7_t1, self.tab1, 1, self.plotter)
        self.t_frame7_t1.grid(row=0, column=12, rowspan = 5, sticky='NEWS', ipady=20)

        '''
        #~~~~~~~~~~~~~~~~~~~~~~~~~ Build Tab 2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        '''

        self.t_frame1_t2 = ttk.Frame(self.tab2,  borderwidth=border, relief='raised')
        self.frame1_t2 = Frame1.Frame_1(self.t_frame1_t2, self.tab2, 2)
        self.t_frame1_t2.grid(row=1, column=0, sticky='NEWS')

        self.t_frame2_t2 = ttk.Frame(self.tab2,  borderwidth=border, relief='raised')
        self.frame2_t2 = Frame2.Frame_2(self.t_frame2_t2, self.tab2, 2)
        self.t_frame2_t2.grid(row=2, column=0, sticky='NEWS')

        self.t_frame3_t2 = ttk.Frame(self.tab2,  borderwidth=border, relief='raised')
        self.frame3_t2 = Frame3.Frame_3(self.t_frame3_t2, self.tab2, 2)
        self.t_frame3_t2.grid(row=2, column=0, sticky='EW')

        self.t_frame4_t2 = ttk.Frame(self.tab2,  borderwidth=border, relief='raised')
        self.frame4_t2 = Frame4.Frame_4(self.t_frame4_t2, self.tab2, 2)
        self.t_frame4_t2.grid(row=1, column=6, columnspan = 5, rowspan = 5, sticky='EW')

        self.t_frame6_t2 = ttk.Frame(self.tab1, borderwidth=border, relief='raised')
        self.frame6_t2 = Frame6.Frame_6(self.t_frame6_t2, self.tab2, 2)
        self.t_frame6_t2.grid(row=0, column=2, sticky='NEWS', ipady=20)

def main():

    root = Tk()
    root.title("Exvivo Analysis")
    tabControl = ttk.Notebook(root)

    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)

    tabControl.add(tab1, text ='Uniax')
    tabControl.add(tab2, text ='Biax')
    tabControl.pack(expand = 1, fill ="both")

    Widgets(root, tab1, tab2) # widgets class - contains all frames to add in each tab

    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))

    root.mainloop()

if __name__ == '__main__':
    main()
