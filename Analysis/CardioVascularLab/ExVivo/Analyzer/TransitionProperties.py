import numpy as np
import matplotlib.pyplot as plt
from rdp import rdp

'''
this class is used in conjunction with the rdp algorithm where the values
from the rdp are used to identify specific points in the graph.
inputs:
    stress_strain = numpy array
'''
class ProcessTransitionProperties:

    def __init__(self, stress_strain=np.array([]), stress_strain_norm=np.array([]), identifier='', eps=0.01):

        # send in the data as a n x 2 numpy array
        self.eps = eps
        self.stress_strain = stress_strain
        self.stress_strain_norm = stress_strain_norm

        self.identifier = identifier

        self.transition_index_start = None
        self.transition_index_end = None

        self.mtm_low = None
        self.mtm_high = None
        self.transition_stress_strain_start = [None,None]
        self.transition_stress_strain_end = [None,None]
        self.max_stress = None
        self.max_stress_indx = None
        self._runTransitionProps()
        # run the RDP algorithm on the normalized data


    def _setStressStrain(self,array1,array2):

        if array1.shape[1] == 2 and array2.shape[1] == 2:
            self.stress_strain = array1
            self.stress_strain_norm = array2
        else:
            print("The stress strain data must be a 2 dimensional numpy array")

    def _invNorm(self, array_norm, array_orig):
        #separate arrays into X and Y components
        x_unzip1, y_unzip1 = map(list,zip(*array_norm))
        x_unzip, y_unzip = map(list,zip(*array_orig))


        xdata = np.array(x_unzip)
        ydata = np.array(y_unzip)

        x_norm = np.array(x_unzip1)
        y_norm = np.array(y_unzip1)


        #unnormalize data
        x_inv = x_norm * (np.max(xdata) - np.min(xdata)) + np.min(xdata)
        y_inv = y_norm * (np.max(ydata) - np.min(ydata)) + np.min(ydata)

        # combine arrays together
        unscaledArray = np.stack((x_inv, y_inv), axis = -1)

        return unscaledArray

    def _runTransitionProps(self):
        if self.stress_strain.size:
            self.rdp_norm = rdp(self.stress_strain_norm,epsilon=self.eps) #
            self.rdp = self._invNorm(self.rdp_norm, self.stress_strain)

            # Filter it to remove lines that are artifacts of the test
            self._filterRDP()

            self._setAllValues()
        else:
            self.rdp = np.array([])

    def _normalizeData(self):

        if self.stress_strain.size:
            pass

    def _outputAllValues(self,outputDict=None):

        # This is to check if there was a dictionary input to append the values
        # to. If there wasn't then create a new one.
        if outputDict is None:
            outputDict = {}

        outputDict['MTMLow_' + self.identifier] = self.mtm_low
        outputDict['MTMhigh_' + self.identifier] = self.mtm_high
        outputDict['MaxStress_' + self.identifier] = self.max_stress
        outputDict['T_Stress_Start_' + self.identifier] = \
                                        self.transition_stress_strain_start[1]
        outputDict['T_Strain_Start_' + self.identifier] = \
                                        self.transition_stress_strain_start[0]
        outputDict['T_Stress_End_' + self.identifier] = \
                                        self.transition_stress_strain_end[1]
        outputDict['T_Strain_End_' + self.identifier] = \
                                        self.transition_stress_strain_end[0]
        outputDict['Elbow_Region_' + self.identifier] = self.elbow

        return outputDict

    def _setAllValues(self):
        #print(self.rdp)
        self._setMaxStress()
        self._setRDP()
        if self.rdp.any():
            self._setTransitionIndexStart(self.rdp[1])
            self._setMTMLow(self.rdp[0],self.rdp[1])
            self.elbow = False

            # Use this to check if the slope of the lines is increasing

            if len(self.rdp) > 2:
                # mtmhighpoint = self._fitLineForMTMHigh(self.rdp[-2],
                #                                                 self.rdp[-1])
                self._setTransitionStressStrainStart()
                self._setMTMHigh(self.rdp[-2],self.rdp[-1]) #get MTMhigh for no elbow as well

            if len(self.rdp) > 3:
                self._setTransitionIndexEnd(self.rdp[-2])
                self._setTransitionStressStrainEnd()
                self.elbow = True

            if len(self.rdp) < 4: # clear transition stress and strain for no elbow
                #print(self.transition_stress_strain_end)
                empty = np.empty(self.transition_stress_strain_end.size)
                empty[:]=np.NaN
                self.transition_stress_strain_end = empty
                self.transition_stress_strain_start = empty

        # self._testPlotter([self.stress_strain,self.rdp])


    def _setTransitionIndexEnd(self,p):

        self.transition_index_end = \
                self._getIndexAtPoint(self.stress_strain[...,[0]],
                                                                    p[0])[0][0]

    def _setTransitionIndexStart(self,p):

        self.transition_index_start = \
                self._getIndexAtPoint(self.stress_strain[...,[0]],p[0])[0][0]

    def _getIndexAtPoint(self,data,value):
        data_round = np.around(data, 3)
        value = round(value, 3)

        return  np.where(data_round == value)

    def _slopeFrom2Points(self,p1,p2):
        slope = 0
        if not np.array_equal(p1,p2):
            slope = (p2[1] - p1[1])/(p2[0] - p1[0])
        return slope

    def _setMTMLow(self,p1,p2):
        # This is the first line identified by RDP algorithm
        self.mtm_low = self._slopeFrom2Points(p1,p2)

    def _setMTMHigh(self,p1,p2):
        # If there are more than 2 lines returned by the RDP then
        # there is an elbow and a second mtm. The furthest point is identified,
        # from the the last line segment and a line segment is fit to that point.
        self.mtm_high = self._slopeFrom2Points(p1,p2)

    def _setRDP(self):
        self.RDP = self.rdp
    # def _setElbow(self):
    #     #If there is an elbow set as true
    #     self.elbow = True

    def _setTransitionStressStrainEnd(self):
        # Stress at the end of the non linear portion of curve.
        # if there are more than 3 lines desribing the curve, this is the stress
        # that is at the beginning of the mtm high

        self.transition_stress_strain_end = \
                                self.stress_strain[self.transition_index_end]

    def _setTransitionStressStrainStart(self):
        # Stress at the onset of the non linear portion of curve.
        # if there are more than 2 lines desribing the curve, this is the stress
        # that is at the end of the MTMLow

        self.transition_stress_strain_start = \
                                self.stress_strain[self.transition_index_start]

    def _setMaxStress(self):
        # This is the maximum stress value in the data.
        self.max_stress = max(self.stress_strain[...,1])
        self.max_stress_indx = np.argmax(self.stress_strain[...,1])

    def _distancesFromLineDefinedByTwoPoints(self, p_line1, p_line2, points):
        lineDistance = np.sqrt((p_line2[1] - p_line1[1])** \
                        + (p_line2[0] - p_line1[0]))
        distances = np.abs((p_line2[1] - p_line2[1])*points[...,0] \
                            -(p_line2[0] - p_line1[0])*points[...,1] \
                            + p_line2[0]*p_line1[1] - p_line2[1]*p_line1[0]) \
                            / lineDistance
        return distances

    def _testPlotter(self,datas):
        fig, ax = plt.subplots(figsize=(10,20))

        for data in datas:
            if len(data) > 1:
                ax.plot(data[...,0], data[...,1])
            else:
                ax.scatter(data[0],data[1])
        plt.show()

    def _fitLineForMTMHigh(self,p1,p2):

        index = self._getIndexAtPoint(self.stress_strain, p1)[0][0]

        pointDistances = self._distancesFromLineDefinedByTwoPoints(p1, p2,
                                        self.stress_strain[index:])


        subIndex = np.argmax(pointDistances)

        fullIndex = index + subIndex


        return self.stress_strain[fullIndex]

    def _fitLineForMTM(self):

        self.LTM_line = np.concatenate((self.rdp[0], self.rdp[1]), axis = 0)
        self.HTM_line = np.concatenate((self.rdp[-2], self.rdp[-1]), axis = 0)

        return self.LTM_line, self.HTM_line

    def _filterRDP(self):

        # Make sure that the second slope isn't less than the first. If
        # it is that means it's not a transition zone
        # import pdb; pdb.set_trace()
        t_rdp = []
        count = 0

        # t_rdp.append(self.rdp[count + 1])
        m1 = 0
        m2 = self._slopeFrom2Points(self.rdp[count], self.rdp[count + 1])
        # count += 1
        # m2 = self._slopeFrom2Points(self.rdp[count], self.rdp[count + 1])
        t_rdp.append(self.rdp[count])
        count += 1
        t_rdp.append(self.rdp[count])

        while (count + 1) < len(self.rdp) :

            m1 = m2
            # m1 = self._slopeFrom2Points(self.rdp[0], self.rdp[1])
            m2 = self._slopeFrom2Points(self.rdp[count], self.rdp[count + 1])
            if m2 > m1:
                count += 1
                t_rdp.append(self.rdp[count])
            else:
                break

        self.rdp = np.array(t_rdp)
        # if m2 > m1:
        #     self.checkTransition = 1
        # return self.checkTransitioncount += 1
