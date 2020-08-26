import sys
sys.path.append('..')

from Analyzer.TransitionProperties import ProcessTransitionProperties

from tkinter import *
from tkinter import messagebox, ttk, filedialog
# from tkFileDialog import *
import uniaxanalysis.getproperties as getprops
from uniaxanalysis.plotdata import DataPlotter
from biax.biaxPlotter import BiaxPlotter
from uniaxanalysis.saveproperties import write_props_csv
from exvivoframes import *
from Data.DataInterface import DataInterfacer


from matplotlib import pyplot as plt

import time

class Widgets:

    def __init__(self, master, tab1, tab2):

        self.master = master
        self.tab1 = tab1
        self.tab2 = tab2

        self.dataInt = DataInterfacer()
        self.plotter = DataPlotter(self.dataInt, self.tab1)
        self.biaxplotter = BiaxPlotter(self.dataInt, self.tab2)

        self._buildFrame1()
        self._buildFrame2()
        self._buildFrame3()
        self._buildFrame4()
        self._buildFrame6()
        self._buildFrame7()

    def _buildFrame1(self, border = 3):

        #TAB1
        self.t_frame1_t1 = ttk.Frame(self.tab1, borderwidth=border, relief='raised')
        self.frame1_t1 = Frame1.Frame_1(self.t_frame1_t1, self.tab1, 1, self.dataInt)
        self.t_frame1_t1.grid(row=0, column=0, sticky='NEWS')

        #TAB2
        self.t_frame1_t2 = ttk.Frame(self.tab2, borderwidth=border, relief='raised')
        self.frame1_t2 = Frame1.Frame_1(self.t_frame1_t2, self.tab2, 2, self.dataInt)
        self.t_frame1_t2.grid(row=0, column=0, sticky='NEWS')

    def _buildFrame2(self, border = 3):

        #TAB1
        self.t_frame2_t1 = ttk.Frame(self.tab1, borderwidth=border, relief='raised')
        self.frame2_t1 = Frame2.Frame_2(self.t_frame2_t1, self.tab1, 1, self.dataInt)
        self.t_frame2_t1.grid(row=4, column=0, sticky='NEWS', ipady=20)

        #TAB2
        self.t_frame2_t2 = ttk.Frame(self.tab2, borderwidth=border, relief='raised')
        self.frame2_t2 = Frame2.Frame_2(self.t_frame2_t2, self.tab2, 2, self.dataInt)
        self.t_frame2_t2.grid(row=5, column=0, columnspan=2, sticky='NEWS')

    def _buildFrame3(self, border = 3):

        #TAB1
        self.t_frame3_t1 = ttk.Frame(self.tab1, borderwidth=border, relief='raised')
        self.frame3_t1 = Frame3.Frame_3(self.t_frame3_t1, self.tab1, 1, self.dataInt)
        self.t_frame3_t1.grid(row=5, column=0, sticky='EW', ipady=20)

        #TAB2
        self.t_frame3_t2 = ttk.Frame(self.tab2, borderwidth=border, relief='raised')
        self.frame3_t2 = Frame3.Frame_3(self.t_frame3_t2, self.tab2, 2, self.dataInt)
        self.t_frame3_t2.grid(row=6, column=0, columnspan=2, sticky='EW', ipady=20)

    def _buildFrame4(self, border = 3):

        #TAB1
        self.t_frame4_t1 = ttk.Frame(self.tab1, borderwidth=border, relief='raised')
        self.frame4_t1 = Frame4.Frame_4(self.t_frame4_t1, self.tab1, 1, self.dataInt)
        self.t_frame4_t1.grid(row=0, column=1, rowspan= 10, sticky='EW', ipady=20)

        #TAB2
        self.t_frame4_t2 = ttk.Frame(self.tab2, borderwidth=border, relief='raised')
        self.frame4_t2 = Frame4.Frame_4(self.t_frame4_t2, self.tab2, 2, self.dataInt)
        self.t_frame4_t2.grid(row=0, column=2, rowspan=10, sticky='EW')

    def _buildFrame6(self, border = 3):

        #TAB1
        self.t_frame6_t1 = ttk.Frame(self.tab1, borderwidth=border, relief='raised')
        self.frame6_t1 = Frame6.Frame_6(self.t_frame6_t1, self.tab1, 1)
        self.t_frame6_t1.grid(row=0, column=2, sticky='NEWS', ipady=20)

        #TAB2
        self.t_frame6_t2 = ttk.Frame(self.tab1, borderwidth=border, relief='raised')
        self.frame6_t2 = Frame6.Frame_6(self.t_frame6_t2, self.tab2, 2)
        self.t_frame6_t2.grid(row=0, column=3, sticky='NEWS', ipady=20)

    def _buildFrame7(self, border = 3):

        #TAB1
        self.t_frame7_t1 = ttk.Frame(self.tab1, borderwidth=border, relief='raised')
        self.frame7_t1 = Frame7.Frame_7(self.t_frame7_t1, self.tab1, 1, self.dataInt, self.plotter)
        self.t_frame7_t1.grid(row=0, column=3, rowspan=11, sticky='NEWS', ipady=40)

        #TAB2
        self.t_frame7_t2 = ttk.Frame(self.tab2, borderwidth=border, relief='raised')
        self.frame7_t2 = Frame7.Frame_7(self.t_frame7_t2, self.tab2, 2, self.dataInt, self.biaxplotter)
        self.t_frame7_t2.grid(row=0, column=4, rowspan=30, sticky='NEWS', ipady=20)


def main():
    root = Tk()
    root.title("Exvivo Analysis")
    tabControl = ttk.Notebook(root)

    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)

    tabControl.add(tab1, text='Uniax')
    tabControl.add(tab2, text='Biax')
    tabControl.pack(expand=1, fill="both")

    Widgets(root, tab1, tab2)  # widgets class - contains all frames to add in each tab

    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)


    root.mainloop()

if __name__ == '__main__':
    main()
