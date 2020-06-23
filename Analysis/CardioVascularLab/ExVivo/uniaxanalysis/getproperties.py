
'''
This class inherits from the parsecsv module to extract properties
in the uniax data. It also converts the force Displacement data into
Stress and strain.  The program finds a linear region before the point of Failure
a neohookean fit, and a slope of a tangent line at 15 percent of the strain.

To Do:

-Make 15 percent tangent function
-Make NeoHookean fit function
-vary targetVal in reduceData()
-Plot Fig function

Notes:
-Turned off print
'''


from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import uniaxanalysis.parsecsv  # homemade module
from scipy import signal


class getproperties(object):

    def __init__(self, fileDimslist, stresstype='cauchy', straintype='engineering', targetReduction=1000, **kwargs):
        # Inherit from parsecsv to be able to extract data
        # super(getproperties,self).__init__(**kwargs)

        # These variables are specific to the getproperties() class
        self.smooth_width = kwargs.get('smooth_width', 101)  # for smoothing the curve
        self.chkderivative = kwargs.get('chkderivate', .05)
        self.timeStep = kwargs.get("timestep", None)
        self.stresstype = stresstype
        self.straintype = straintype

        # The standard deviation for the windowed gaussian function
        self.std = kwargs.get('std', 7)

        # Parse fileDimslist for values needed. input format for fileDimslist:
        # ["Sample_Specimen","Filename","Width","Thickness","G-G"]
        self.sample = fileDimslist[0]
        self.fname = fileDimslist[1]

        # Only needed for a single calculation each
        width = fileDimslist[2]
        thickness = fileDimslist[3]
        initialLength = fileDimslist[4]

        [force, displacement, time] = self.getForceDisplacement(skip=5)  # Get from CSV
        if targetReduction is not None:
            [displacement, force] = self.reduceData(
                targetReduction, displacement, force)  # reduce number of data points

        self.calcStrain(displacement,initialLength)

        self.calcStress(force, width, thickness, displacement, initialLength)


        # use moving average to smooth data
        self.stress = self.applySavgol(self.stress)

        #self.strain = self.movingAverage(self.strain)

        # Index where failure occurs
        self.failIndx = self.findFailure(self.stress)

        # Get the second derivative of the gaussian convolution of the curve
        self.secondDer = self.convolveWithGauss(self.stress[:self.failIndx], smooth_width=101, bounds=3)

        # returns a list of 2 numbers linearRange[0] is the start of the linear range
        # linearRange[1] is the end of the linear range

        self.linearRange = self.getlinearRange(self.secondDer)
        start = self.linearRange[0]
        end = self.linearRange[1]

        # This is a little messy but returns the function of the line, and the coefficients
        func,linearCoefficients = self.fitlineToData(self.strain[start:end],self.stress[start:end])

        # build the line for the linear region
        self.xline = np.linspace(self.strain[start],self.strain[end],100)
        self.yline = self.yValuesFromPolyFit(self.xline, func)

        # get the slope of the line for the stiffness
        self.stiffness = linearCoefficients[0]

        # get the failure point and set as the strength
        self.strength = self.stress[self.failIndx]

        #find maximum
        #self.maxInd = self._findMax(self.stress, index=10)

        # truncate data
        # self.strain, self.stress = self.truncData(self.strain, self.stress, self.maxInd)

        #normalize
        self.stress_norm, self.strain_norm = self._normalizeData(self.stress, self.strain, self.failIndx)

        # Use the Ramer-Douglas-Peucker Algorithm to create a linear representaiton
        # self.rdpOutput = self.testRDP(self.stress[:self.failIndx], .1)


    def testRDP(self,data,eps):
        from .rdp import rdp

        output = rdp(data, eps)

        return output

    def getlinearRange(self,data,derivativecutoff=0.1,closeToZero=0.003):


        # find the most minimum point on the second derivative curve
        # step back to a point that is at some cuttoff


        index2 = np.argmin(data) - 1
        val = data[index2]

        while abs(val) < closeToZero:
            index2 -= 1
            val = data[index2]

        index2 += 1
        der = 10000

        t_index = index2 - 1

        while abs(der) > closeToZero:
            t_index -= 1
            der = (data[t_index] - data[t_index-1])

        # set the minimum index to a quarter of the data set
        minIndex = int(t_index*.25)
        maxDer = 0

        # step backwards until the minimum index in the range is reached
        while t_index > minIndex:

            der = (data[t_index] - data[t_index-1])
            # if der < 0:
            #     print("The index is {0}... the derivative is... {1} and the current minimum is... {2}.".format(t_index,der,Minder))
            # check if the change in values is steeper than the previous
            if abs(der) > maxDer:

                maxDer = der
                index1 = t_index

            t_index -= 1

        index1 = self.stepTillMax(data, index1)

        return [index1,index2]

    def stepTillMax(self,data,index):
        currentValue = data[index]
        nextValue= data[index+1]

        while currentValue < nextValue:
            index += 1
            currentValue = data[index]
            nextValue = data[index + 1]

        return index -1

    def fitlineToData(self,x,y):

        # fit a line from the first index to the last
        coefficients = np.polyfit(x, y, 1)
        f = np.poly1d(coefficients)

        return f,coefficients

    def yValuesFromPolyFit(self,x,f):

        return np.polyval(f,x)


    def applySavgol(self,data,winlen=71,porder=2):
        from scipy import signal
        # smooth the data
        data = signal.savgol_filter(data, winlen, porder, deriv=0,
                                      delta=1.0, axis=-1, mode='interp', cval=0.0)
        return data

    def getForceDisplacement(self, skip=None, *args):
        # get the Force and Displacement Data from csv
        # Read csv dimensions and populate list of patient and specimen concantenated

        df = pd.read_csv(self.fname, index_col=False, skiprows=skip)  # CSV to full pandas dataframe

        # Convert dataframe to numpy arrays
        try:  # Use this if the columns have labels
            force = df.loc[:, "Force"].values  # extract force from full pandas dataframe
            displacement = df.loc[:, "Displacement"].values  # extract Displacement
            time = df.loc[:, "Time"].values  # extract Displacement

        # then try this.... columns need to be time,displacement, force in that order
        except KeyError:

            force = df.iloc[:, 2].values  # extract force from full pandas dataframe
            displacement = df.iloc[:, 1].values  # extract Displacement
            time = df.iloc[:, 0].values  # extract Displacement

        return force, displacement, time

    def reduceData(self, target, x, y):

        # reduce the data to a target number of points

        reduceData = int(np.ceil(len(y)/target))

        # Reduce the data by a number so every nth reduceData
        x = x[::reduceData]
        y = y[::reduceData]

        return x, y

    def calcStress(self, force, width, thickness,displacement,initialLength):

        # Calulate the cauchy stress if specified defaults to the 1st Piola-Kirchoff
        # aka engineering stress
        if self.stresstype == "cauchy":
            stretch = (displacement - displacement[0])/initialLength + 1
            self.stress = force/(width*thickness)*stretch

        elif self.stresstype == "firstpiola":
            self.stress = force/(width*thickness)

        else:
            # 1st Piola stress
            print("hmmm need to pass in (firstpiola or cauchy)")

    def calcStrain(self, disp, g_g):

        disp = disp-disp[0]  # Zero the displacement for the first measurement
        strain = disp/g_g  # engineering strain

        if self.straintype == 'engineering':
            self.strain = strain  # Get strain
        elif self.straintype == 'stretch':
            self.strain = strain + 1
        else:
            print("What the fuck are you doing.... (engineering or stretch)")

    def _findMax(self, data, index):

        currVal = data[index]
        nextVal = data[index + 1]

        while currVal < nextVal:
            index += 1

            currVal = data[index]
            nextVal = data[index + 1]

            maxInd = index

        return maxInd

    def _normalizeData(self, ydata, xdata,ind):
        '''
        This function normalizes x and y data between 0 and 1.
        Inputs: numpy arrays (x and y) and starting index.
        Returns: normalized data (as 2 separate arrays)
        '''

        x_norm = (xdata - np.min(xdata[:ind])) / (np.max(xdata[:ind]) - np.min(xdata[:ind]))
        y_norm = (ydata - np.min(ydata[:ind])) / (np.max(ydata[:ind]) - np.min(ydata[:ind]))

        return y_norm, x_norm

    def fitRange(self, *args):

        minRange = args[0]
        maxRange = args[1]

        fitRange = np.logical_and(self.epsilon > minRange, self.epsilon <
                                  maxRange)  # Get range to fit (logical array)

        xFit = self.epsilon[fitRange]  # range of strain between min and max range
        yFit = self.sigma[fitRange]  # range of stress for the the same range

        return xFit, yFit

    def firstDerivative15percent(self, *args):
        pass

    def fitCurve15percent(self, *args):
        pass
        # Fits a 2nd order olynomial between 10 an 10 percent strain then finds the linear
        # tangent from derivative at 15 percent
        xFit, yFit = self.fitRange(0.10, 0.20)  # find values in the range
        coeff = np.polyfit(xFit, yFit, 2)  # return coeffiecient of line from derivative
        d_dx = 2*coeff[0]*xFit - coeff[1]

        return xFit

    def fitNeoHookean(self, *args):
        from scipy.optimize import curve_fit
        # Fit the neohookean model sigman = 2*c*(lamda-1/lamda^2) calls fitRange function

        xFit, yFit = self.fitRange(0.05, 0.15)
        lamda = xFit + 1  # convert strain to stretch

        # Fit the data to the nonlinear curve_fit
        popt, pcov = curve_fit(neoHookeanCurve, xFit, yFit)
        # get the values of stress for coresponding parameters
        yNH = self.neoHookeanCurve(xFit, *popt)

        return popt, xFit, yNH  # return the c_0 parameter and the values of fit

    def neoHookeanCurve(self, x, c):
        # The model to be fit to the Data

        return 2*c*(x-x ^ -2)

    def calcDerivative(self, indx, y, h):
        # Calculates a simple numerical derivative based on a single stepbackward
        # inputs :
        #       - indx the point to start the numberical
        #       - y is the array that represents the values of the function
        #   `   - h is the step size in the numberical derivative`

        der = (y[indx]-y[indx-1])/h  # numerical derivative

        return der

    def convolveWithGauss(self, data, smooth_width=101, bounds=3):

        padder = int(smooth_width/2)

        # pad the data
        paddedData = np.pad(data, (padder, padder), 'edge')

        # convolve the data with the second derivative of a gaussian distribution

        # Create the x values to apply to the gaussian distribution
        x1 = np.linspace(-bounds, bounds, smooth_width)
        norm = np.sum(np.exp(-x1**2)) * (x1[1]-x1[0])  # ad hoc normalization

        y1 = (4*x1**2 - 2) * np.exp(-x1**2) / smooth_width * 8  # norm*(x1[1]-x1[0])

        # # Create a gaussian distribution to convolve the data with
        # window = signal.gaussian(201, std=3)

        # calculate second order deriv.
        y_convPadded = np.convolve(paddedData, y1, mode="same")

        y_conv = y_convPadded[padder:-padder]

        return y_conv

    def findLinear(self, disp, force, minimumSlope=0.05):


        # create convolution kernel for calculating
        # the smoothed second order derivative

        # inputs  -
        #           disp = displacement array
        #           force = force array

        indx = np.argmax(self.stress)
        x = self.strain[:indx]
        y = self.stress[:indx]

        # smooth_width = self.smooth_width
        # x1 = np.linspace(-3, 3, smooth_width)
        # norm = np.sum(np.exp(-x1**2)) * (x1[1]-x1[0])  # ad hoc normalization
        #
        # y1 = (4*x1**2 - 2) * np.exp(-x1**2) / smooth_width * 8  # norm*(x1[1]-x1[0])

        # Create a gaussian distribution to convolve the data with
        window = signal.gaussian(self.smooth_width, std=self.std)

        # calculate second order deriv.
        y_conv = np.convolve(y, window, mode="same")

        # convolve the 2nd derivative curve to determine points where the curve changes
        conv_array = np.convolve(y_conv, [-1, 0, 1])

        # Get the points where the convolution changes signs.... this is when it does to linear
        zero_crossings = np.where(np.diff(np.sign(conv_array)))[0]

        while minimumSlope > 0.0001:

            for num, crossing in enumerate(zero_crossings):

                if conv_array[zero_crossings[num]-1] < 0 and x[zero_crossings[num]] > 0.2:

                    # set the minimum point in the range as the first maxima
                    minrange = zero_crossings[num]

                    # set the minimum point in the range as the first minima
                    maxrange = zero_crossings[num+1]

                    # Find the slope of the line at the local maxima
                    a = self.calcDerivative(minrange, y_conv, x[1])

                    if a > minimumSlope:  # if the slope is greater than this value break the loop

                        # get the stress where the loop broke
                        stressAtstart = self.stress[zero_crossings[num]]
                        stressAtstart = np.around(stressAtstart, 3)
                        print ("The derivate for {} was {} at {} MPa".format(
                            self.sample, np.around(a, 3), stressAtstart))  # print the stress at that point
                        break
            minimumSlope /= 10  # reduce slope criteria by one order if magnitude if it has not convergedd

        # calculate polynomial
        x_fit = x[minrange:maxrange]
        y_fit = y[minrange:maxrange]

        plt.plot(x_fit, y_fit, color="b", linewidth=8, label="stuff that fits")
        plt.plot(x, y, color="r")
        plt.show()

        print ("Linear region starts at ... {} MPa".format(np.around(self.stress[minrange], 3)))
        print ("Linear region ends at   ... {} MPa".format(np.around(self.stress[maxrange], 3)))
        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        z = np.polyfit(x_fit, y_fit, 1)
        f = np.poly1d(z)

        # calculate new x's and y's
        self.xline = np.linspace(x[minrange-100], x[maxrange+100], 50)  # test
        # self.xline = np.linspace(x_fit[0], x_fit[-1], 50) # original
        self.yline = f(self.xline)

        return x, y_conv

    def plotTitle(self, nameparts):

        import os
        import re

        a = os.path.basename(nameparts)
        a = re.split(r'[ ,_]', a)
        title = a[0] + "_" + a[1]

        return title

    def findFailure(self, data):

        # convolve the data with kernel
        # pick out the points where the sign changes

        indxArray = signal.argrelmax(data, axis=0, order=1, mode='clip')
        # return index of the point of failure

        if indxArray[0].any():
            indx = indxArray[0][0]
        else:
            indx = np.argmax(data)
        return indx

    def movingAverage(self, a, n=3):
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n

    def truncData(self, xdata, ydata, index):
        # Truncate the data based on the maximum value in ydata


        xTrunc = xdata[:(index+1)]
        yTrunc = ydata[:(index+1)]

        return xTrunc, yTrunc

    def get_closest(self, data, val):
        # function used to find the closest values given to the values in the data
        # set
        # minus the x value from the data set
        minValIndex = np.argmin(abs(data - val))
        # return the value
        return minValIndex

    def sort_data(self, xdata, ydata, xvals=[], yvals=[]):
        # Takes 2 inputs and 2 arrays of data and finds the range that
        # is within the 2 input values

        # get the indices of the data to values to use, x data is used to create the range
        Index = [self.get_closest(xdata, val) for val in xvals]

        # sort the array in ascending order
        Index = np.sort(np.array(Index))

        # define the data from the indices provided
        xFit = xdata[Index[0]:Index[1]]
        yFit = ydata[Index[0]:Index[1]]

        return xFit, yFit

    def manual_max(self, xdata, ydata, xvals=[], yvals=[]):
        # finds the maximum value in an array from a larger data set given 2 indices
        # to mark the beginning and end of a range

        # Call class method sort_data to return the data set from minimum to
        # maximum values
        xFit, yFit = self.sort_data(xdata, ydata, xvals, yvals)

        # Find the indes of the maximum value in the data set
        maxIndx = np.argmax(yFit)

        # Define the maximum value in y and x
        xAtMax = xFit[maxIndx]
        yAtMax = yFit[maxIndx]

        # set the class variable of strength as the max from user input
        self.strength = yAtMax

        return xAtMax, yAtMax

    def manual_linear(self, xdata, ydata, xvals=[], yvals=[]):
        # fit a line between the two points in the data

        # Call class method sort_data to return the data set from minimum to
        # maximum values
        xFit, yFit = self.sort_data(xdata, ydata, xvals, yvals)

        # fit a line from the first index to the last
        z = np.polyfit(xFit, yFit, 1)
        f = np.poly1d(z)

        # get the y values that correspond to the line
        yLine = np.polyval(f, xFit)

        # get the value of the slope of the linea
        slope = f[1]

        # Set the class variable of stiffness to the slope of the line
        self.stiffness = slope

        return slope, [xFit, yLine]  # return the x and y values of the line

    def return_XYdata(self, *args):

        return {'x': self.x, 'y': self.y, 'xMax': self.xMax,
                'yMax': self.yMax, 'title': self.pltTitle,
                'xline': self.xline, 'yline': self.yline}
