import tkinter as tk
from PIL import ImageTk, Image

class Frame_6(tk.Frame):

    def __init__(self,master, tab, tab_no):

        tk.Frame.__init__(self, master)
        self.master = master
        self.tab = tab
        self.tab_no = tab_no
        self.canvas = tk.Canvas(self.master)
        self.button = tk.Button(self.canvas,text='')
        self.imageFname = "exvivoframes/noun_Major Axis_409453.png"
        self.image = None

        self.canvas.pack(fill='both',expand=True)
        self.button.pack(fill='both',expand=True)


        # self.panel.grid(row=0, column=0)

    def _OpenAndResizeImage(self):

        img = Image.open(self.imageFname)
        img = img.resize((100,100), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(img)
