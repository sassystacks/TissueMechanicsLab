
'''
This class inherits from the parsecsv module to extract properties
in the uniax data. It also converts the force Displacement data into
Stress and strain.  The program finds a linear region before the point of Failure
a neohookean fit, and a slope of a tangent line at 15 percent of the strain.

To Do:

-Make 15 percent tangent function
-Make NeoHookean fit function
-Convert force/displacement to stress/strain function
-clean up __init__()
'''


from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from generalformat import parsecsv

class getproperties(object):

    def __init__(self, **kwargs):

        #super(getproperties,self).__init__(**kwargs)
        # Read CSV data
        self.rawDat = kwargs['directory']
        self.smooth_width = kwargs['smooth_width']

        self.fnames =
        self.pltTitle = self.plotTitle(rawDat)

        [Force,Displacement] = self.getForceDisplacement()
        self.dimensions = getTestDims()

        indx = self.findFailure() - 1

        self.xMax = x[indx]
        self.yMax = self.y[indx]

        #[self.xfit,self.yfit] = self.fitCurve(indx)

        [self.xGrad,self.yGrad] = self.findLinear(indx)

    def getForceDisplacement(self,*args):
        # get the Force and Displacement Data from csv
        #Read csv dimensions and populate list of patient and specimen concantenated
        df = pd.read_csv(rawDat,skiprows=self.skip)

        x = df.iloc[:,1].values
        y = df.iloc[:,2].values
        x = x[0::step]
        y = y[0::step]
        # [x,y] = self.truncData(x,y)
        x = x-x[0]
        x=x[:-2]

        y = self.moving_average(y)

        return x,y

    def fitRange(self, *args):

        minRange = args[0]
        maxRange = args[1]

        fitRange = np.logical_and(self.epsilon > minRange, self.epsilon < maxRange) #Get range to fit (logical array)
        xFit = self.epsilon[fitRange] #range of strain between min and max range
        yFit = self.sigma[fitRange] # range of stress for the the same range

        return xFit,yFit
    def firstDerivative15percent(self, *args):
        pass

    def fitCurve15percent(self, *args):
        pass
        #Fits a 2nd order olynomial between 10 an 10 percent strain then finds the linear
        #tangent from derivative at 15 percent
        xFit, yFit = self.fitRange(0.10,0.20) #find values in the range
        coeff = np.polyfit(xFit,yFit,2) #return coeffiecient of line from derivative
        d_dx = 2*coeff[0]*xFit - coeff[1]


        return xFit

    def fitNeoHookean(self, *args):
        from scipy.optimize import curve_fit
        #Fit the neohookean model sigman = 2*c*(lamda-1/lamda^2) calls fitRange function

        xFit, yFit = self.fitRange(0.05,0.15)
        lamda = xFit + 1 #convert strain to stretch

        #Fit the data to the nonlinear curve_fit
        popt,pcov = curve_fit(neoHookeanCurve,xFit,yFit)
        yNH = self.neoHookeanCurve(xFit,*popt) #get the values of stress for coresponding parameters

        return popt, xFit, yNH # return the c_0 parameter and the values of fit

    def neoHookeanCurve(self, x, c):
        #The model to be fit to the Data

        return 2*c*(x-x^-2)



    def calcDerivative(self, *args):
        #Calculates a simple numerical derivative based on a single stepbackward
        indx = args[0]-1
        y = args[1]
        h = args[2]

        der = (y[indx]-y[indx-1])/h #numerical derivative

        return der

    def findLinear(self, *args):

        # create convolution kernel for calculating
        # the smoothed second order derivative
        x = self.x[:args[0]]
        y = self.y[:args[0]]

        x = self.x
        #y = self.y[:args[0]]
        y = self.y

        smooth_width = self.smooth_width
        x1 = np.linspace(-3,3,smooth_width)
        norm = np.sum(np.exp(-x1**2)) * (x1[1]-x1[0]) # ad hoc normalization
        y1 = (4*x1**2 - 2) * np.exp(-x1**2) / smooth_width *8#norm*(x1[1]-x1[0])

        # calculate second order deriv.
        y_conv = np.convolve(y, y1, mode="same")

        #convolve the 2nd derivative curve to determine points where the curve changes
        conv_array = np.convolve(y_conv,[-1,0,1])

        zero_crossings = np.where(np.diff(np.sign(conv_array)))[0]


        for num in xrange(0,len(zero_crossings)):

            if  conv_array[zero_crossings[num]-1] < 0 and x[zero_crossings[num]] > 0.2:
                #set the minimum point in the range as the first maxima
                minrange = zero_crossings[num]
                #set the minimum point in the range as the first minima
                maxrange = zero_crossings[num+1]

                a = self.calcDerivative(minrange,y_conv,x[1])
                print "{} : {}".format(self.pltTitle,a)
                if a > .01:
                    break

        # calculate polynomial
        x_fit = x[minrange:maxrange]
        y_fit = y[minrange:maxrange]
        z = np.polyfit(x_fit, y_fit, 1)
        f = np.poly1d(z)


        # calculate new x's and y's
        self.xline= np.linspace(x_fit[0], x_fit[-1], 50)
        self.yline = f(self.xline)

        return x, y_conv

    def plotTitle(self, *args):

        import os
        import re

        fullpath = args[0]
        a = os.path.basename(fullpath)
        a = re.split(r'[ ,_]',a)
        title = a[0] + "_" + a[1]

        return title

    def findFailure(self, *args):

        #start at 10 percent of the data set to avoid noise at beginning of curve
        start = int(len(self.y)/10)
        ydata = self.y[int(start):]
        conv_array = np.convolve(ydata,[-1,0,1])
        zero_crossings = np.where(np.diff(np.sign(conv_array)))[0]

        #Find the zero crossings where maxima occurs in the graph
        for num in zero_crossings:
            chkslope = self.calcDerivative(num+start,self.y,self.x[1])

            if abs(chkslope) > 0.1:
                print(num)
                break

        return num + start

    def moving_average(self, a, n=3):
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n

    def truncData(self, *args):

        xdata = args[0]
        ydata = args[1]
        maxindx = np.argmax(ydata)
        xTrunc = xdata[:maxindx-1]
        yTrunc = ydata[:maxindx-1]
        return xTrunc, yTrunc

    def visualizeData(self, *args):

        #plt.plot(x,y_conv, label = "second deriv")
        # plt.plot(x, y_n,"o", label = "noisy data")
        fig = plt.figure(1)
        plt.plot(self.x, self.y, label="raw")
        plt.plot(self.xMax, self.yMax, "o", label="Failure")
        plt.plot(self.xGrad, self.yGrad, label="FitCurve")
        plt.plot(self.xline, self.yline, label="FitCurve")

        plt.title(self.pltTitle)
        #plt.plot(x, x, "0.3", label = "linear data")
        plt.hlines([-0.5],min(self.x),max(self.x),'m')
        plt.hlines([0],min(self.x),max(self.x),'m')
        plt.vlines([0.5],-0.5,max(self.y),'m')
        # plt.axvspan(0,4, color="y", alpha=0.2)
        # plt.axvspan(6,14, color="y", alpha=0.2)
        # plt.axhspan(-1,1, color="b", alpha=0.2)
        #plt.vlines([0, 4, 6],-10, 10)
        # plt.xlim(-2.5,12)
        # plt.ylim(-2.5,6)
        plt.legend(loc=0)

        plt.show()

    def returnXYData(self,*args):


        return {'x':self.x, 'y':self.y, 'xMax':self.xMax,
                'yMax':self.yMax,'title':self.pltTitle,
                'xline':self.xline,'yline':self.yline}


if __name__ == '__main__':
    args_dict = {
                'directory' : '/home/richard/MyProjects/TissueMechanicsLab/RawData/cp_Test_Data'
                'smooth_width': 79}

    a = getproperties(directory='/home/richard/MyProjects/Analysis/CardioVascularLab/rawCSVfail/AAA20171003/AAA20171003_LA2L.CSV',step=20,smooth_width=79).visualizeData()
