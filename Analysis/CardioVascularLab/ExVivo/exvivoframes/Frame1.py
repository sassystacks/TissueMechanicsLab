import tkinter as tk
from tkinter import ttk
'''
This frame contains all the folder selection and data parsing functions.
'''
class Frame_1(tk.Frame):

    def __init__(self,master, tab, tab_no):
        tk.Frame.__init__(self, master)
        self.master = master
        self.tab = tab
        self.tab_no = tab_no

        if self.tab_no == 1:
            ttk.Label(self.tab, text='tab1 test').grid(column=0, row=0, padx=30, pady=30)
        elif self.tab_no == 2:
            ttk.Label(self.tab, text='tab2 test').grid(column=0, row=0, padx=30, pady=30)
