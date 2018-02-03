import kivy
kivy.require('1.10.0') # replace with your current kivy version !


from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
from exctractRawCSV import extract_raw
import os

plt.plot([1, 23, 2, 4])
plt.ylabel('some numbers')

directory = '/home/richard/MyProjects/Analysis/CardioVascularLab/rawCSVfail'
#direct = '/home/richard/MyProjects/Analysis/CardioVascularLab/rawCSVfail/AAA20171003_LA2L.CSV'
step = 3

#extract_raw(directory=direct,stepforward='20').visualizeData()

items = os.listdir(directory)
a = []
for item in items:

    if "dimensions" not in item:
        fname = os.path.join(directory,item)
        try:
            a.append(extract_raw(directory=fname,stepforward=step))
        except:
            continue

class MyApp(App):

    def build(self):
        box = BoxLayout()
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        return box

MyApp().run()
