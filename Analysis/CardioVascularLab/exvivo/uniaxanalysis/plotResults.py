
from getproperties import getproperties
import os
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

directory = '/home/richard/MyProjects/TissueMechanicsLab/RawData/rawCSVfail/AAA20171003'

fstep = 4

items = os.listdir(directory)
a = []
print(items)
for item in items:

    if "dimensions" not in item and ".CSV" in item:

        fname = os.path.join(directory,item)
        #try
        a.append(getproperties(directory=fname,step=fstep,smooth_width=79).returnXYData())
        # except:
        #     continue

# for item in a:
#
#     item.visualizeData()
#
# '''
#creates an animation of the plots
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], animated=True)
mx, = plt.plot([], [], 'ro', animated=True)
e, = plt.plot([],[], 'k', animated=True)

def init():
    ax.set_xlim(0, 12)
    ax.set_ylim(0,22)
    return ln, mx, e

def update(frame):

    xdata = (a[frame]['x'])
    ydata = (a[frame]['y'])
    xMax = (a[frame]['xMax'])
    yMax = (a[frame]['yMax'])
    xline = (a[frame]['xline'])
    yline = (a[frame]['yline'])
    # ax.set_xlim(0, max(xdata))
    # ax.set_ylim(0, max(xdata))

    ln.set_data(xdata, ydata)
    mx.set_data(xMax, yMax)
    e.set_data(xline, yline)

    return ln, mx, e

ani = FuncAnimation(fig, update, frames=len(a),
                    init_func=init, blit=True)
plt.show()
