
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
import parsecsv #homemade module

class getproperties(object):

    def __init__(self, fileDimslist, **kwargs):
        #Inherit from parsecsv to be able to extract data
        #super(getproperties,self).__init__(**kwargs)

        #These variables are specific to the getproperties() class
        self.smooth_width = kwargs.get('smooth_width',101)#for smoothing the curve
        self.chkderivative = kwargs.get('chkderivate',.05 )
        self.timeStep = kwargs.get("timestep",.2)

        #Parse fileDimslist for values needed. input format for fileDimslist:
        # ["Sample_Specimen","Filename","Width","Thickness","G-G"]
        self.sample = fileDimslist[0]
        self.fname = fileDimslist[1]

        #Only needed for a single calculation each
        width = fileDimslist[3]
        thickness = fileDimslist[2]
        gtog = fileDimslist[2]



        [force,displacement,time] = self.getForceDisplacement() #Get from CSV
        [displacement,force] = self.reduceData(time,displacement,force) # reduce number of data points

        self.strain = self.calcStrain(displacement,gtog) # Get strain
        self.stress = self.calcStress(force,width,thickness) # Get Stress
        self.stress = self.movingAverage(self.stress)

        #Index where failure occurs
        self.failIndx = self.findFailure(self.strain,self.stress) - 1

        #The second order gradient of a gaussian kernel
        #Shows where graphs deviates and returns to linearity
        [self.xlinear,self.ylinear] = self.findLinear(displacement,force)

        self.visualizeData(displacement-displacement[0],force)#Just for comparison to raw data

    def getForceDisplacement(self,*args):
        # get the Force and Displacement Data from csv
        #Read csv dimensions and populate list of patient and specimen concantenated

        df =pd.read_csv(self.fname,index_col=False) #CSV to full pandas dataframe

        #Convert dataframe to numpy arrays
        force = df.loc[:,"Force"].values # extract force from full pandas dataframe
        displacement = df.loc[:,"Displacement"].values # extract Displacement
        time = df.loc[:,"Time"].values # extract Displacement

        return force,displacement,time

    def reduceData(self, time, x, y):

        x,y  = self.truncData(x,y)
        #Reduce the number of data points by a certain step value
        targetVal = self.timeStep
        step = int(targetVal/time[1]) #divide the target time by first value in time
        print "The data have been reduced by ....", step
        #Reduce the data in both x and y
        x = x[0::step]
        y = y[0::step]

        return x,y

    def calcStress(self, force, width, thickness):

        stress = force/(width*thickness)

        return stress

    def calcStrain(self, disp, g_g):

        disp = disp-disp[0]# Zero the displacement for the first measurement
        strain = disp/g_g #engineering strain

        strain=strain[1:-1] #Reduce the points by 1 on either side to keep consistent
                            #vector size with stress after moving average

        return strain

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

    def findLinear(self,disp,force):

        # create convolution kernel for calculating
        # the smoothed second order derivative

        indx = np.argmax(self.stress)
        x = self.strain[:indx]
        y = self.stress[:indx]

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

                a = self.calcDerivative(minrange,y_conv,x[1]) #Find the slope of the line at the local maxima

                if a > .01: #if the slope is greater than this value break the loop
                    stressAtstart = self.stress[zero_crossings[num]] #get the stress where the loop broke
                    stressAtstart = np.around(stressAtstart,3)
                    print "The derivate for {} was {} at {} MPa".format(self.sample,np.around(a,3),stressAtstart) #print the stress at that point
                    break

        # calculate polynomial
        x_fit = x[minrange:maxrange]
        y_fit = y[minrange:maxrange]
        print "Linear region starts at ... {} MPa".format(np.around(self.stress[minrange],3))
        print "Linear region ends at   ... {} MPa".format(np.around(self.stress[maxrange],3))
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        z = np.polyfit(x_fit, y_fit, 1)
        f = np.poly1d(z)


        # calculate new x's and y's
        self.xline= np.linspace(x_fit[0], x_fit[-1], 50)
        self.yline = f(self.xline)

        return x, y_conv

    def plotTitle(self, nameparts):

        import os
        import re

        a = os.path.basename(nameparts)
        a = re.split(r'[ ,_]',a)
        title = a[0] + "_" + a[1]

        return title

    def findFailure(self, x, y):

        #start at 10 percent of the data set to avoid noise at beginning of curve
        start = int(len(y)/10)
        ydata = y[int(start):]
        conv_array = np.convolve(ydata,[-1,0,1])
        zero_crossings = np.where(np.diff(np.sign(conv_array)))[0]

        #Find the zero crossings where maxima occurs in the graph
        for num in zero_crossings:
            chkslope = self.calcDerivative(num+start,y,x[1])

            if abs(chkslope) > self.chkderivative:
                print "broke loop at index .... "  + str(num)
                break

        return num + start

    def movingAverage(self, a, n=3):
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n

    def truncData(self, xdata,ydata):

        maxindx = np.argmax(ydata)
        xTrunc = xdata[:maxindx-1]
        yTrunc = ydata[:maxindx-1]
        return xTrunc, yTrunc

    def visualizeData(self, disp, force, *args):

        #Creates a plot based on the analysis
        #Main plotting features
        fig = plt.figure(1) #initialize figure
        plt.plot(self.strain, self.stress, label="raw") #plot main data set
        plt.plot(self.strain[self.failIndx], self.stress[self.failIndx], "o",label="Fail") #plot main data set
        #plt.plot(disp, force, label="raw") #plot main data set
        plt.plot(self.xlinear, self.ylinear, label="FitCurve") #plots the gradient curve right now
        plt.plot(self.xline, self.yline, label="linearStrain") #plots linear part of curve


        plt.title(self.sample)
        # plt.hlines([-0.5],min(self.x),max(self.x),'m')
        # plt.hlines([0],min(self.x),max(self.x),'m')
        # plt.vlines([0.5],-0.5,max(self.y),'m')

        plt.legend(loc=0)

        return fig

    def plotFig(self):
        pass

    def returnXYData(self,*args):


        return {'x':self.x, 'y':self.y, 'xMax':self.xMax,
                'yMax':self.yMax,'title':self.pltTitle,
                'xline':self.xline,'yline':self.yline}


if __name__ == '__main__':

    testList =  ['RSAA20160621_U1',
                '/home/richard/MyProjects/TissueMechanicsLab/CleanSheets/RSAA20160621_U1.CSV',
                4.62, 2.365, 5.0]
    #this is a sample to test outputs
    args_dict = {
                'dimsfile': '/home/richard/MyProjects/TissueMechanicsLab/RawData/Allfiles.csv',
                'topdir': '/home/richard/MyProjects/TissueMechanicsLab/CleanSheets',
                'writeto': 'Test','identifier': '_Fail','skiprows': 5, 'ignore': '.tdf',
                'smooth_width': 59, 'project': 'AAA',',step': 20}
    a = getproperties(fileDimslist = testList,**args_dict)
    # d = a.getMatchingData('/home/richard/MyProjects/TissueMechanicsLab/CleanSheets',
    #                     '/home/richard/MyProjects/TissueMechanicsLab/RawData/Allfiles.csv')
    # args_dict = {
    #             'directory' : '/home/richard/MyProjects/TissueMechanicsLab/RawData/cp_Test_Data'
    #             }
    #
    # a = getproperties(directory='/home/richard/MyProjects/Analysis/CardioVascularLab/rawCSVfail/AAA20171003/AAA20171003_LA2L.CSV',smooth_width=79).visualizeData()
