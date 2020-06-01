import sys
sys.path.append('..')
from Analyzer.TransitionProperties import ProcessTransitionProperties

from rdp import rdp
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from biax.BiaxDataHandler import BiaxDataParser, BiaxDataOutput
# from BiaxProperties import ProcessBiaxProperties

from Analyzer import DataFilter

def _getBinIndexOfNumpyArrays(data, binsize=0.01):

    bins=np.arange(min(data), max(data) + binsize/2, binsize)
    inds = np.digitize(data, bins, right=True)

    return inds, bins

def _prepValuesForExport(filename):
    fileparts = BiaxDataParser()._breakDownFileName(filename, 2)
    entryDict = BiaxDataParser()._getDataEntries(fileparts[8])
    entryDict['Direction'] = 'U2'

    return entryDict

def _binDataFromIndices(data,indices, bins):

    keys = np.unique(indices)
    keys = np.sort(keys)
    binDict = {k:[] for k in keys}
    for i in range(data.size):
        binDict[indices[i]].append(data[i])

    outputArray = [np.mean(binDict[key]) for key in binDict]
    #
    # for key in binDict:
    #     outputArray.append(np.mean(binDict[key]))

    return np.array(outputArray), bins[keys-1]

def _buildPlottingParameters(label):

    outputParameters = {}
    if label == 'Raw Data':
        outputParameters = {'label':label, 'alpha':0.5, 'zorder':1,
                                'marker':'o', 'color':'y','linewidth': 2}
    elif label == 'Raw RDP':
        outputParameters = {'label':label, 'alpha':0.2, 'zorder':3,
                                'marker':'o', 'color':'m','linewidth': 3}

    elif label == 'Binned Data':
        outputParameters = {'label':label, 'alpha':0.8, 'zorder':2,
                                'marker':'o', 'color':'r','linewidth': 2}

    elif label == 'Binned RDP':
        outputParameters = {'label':label, 'alpha':0.7, 'zorder':4,
                                'marker':'h', 'color':'k','linewidth': 3}

    else:
        print("The label was not recognized")

    return outputParameters

def _processBiaxData(stressStrainDict, direction_key, eps_raw = 0.1,
                eps_binned = 0.05, startStrainValue = 0.05, windowWidth = 21,
                bin_size = 0.002):

    testPointsX = stressStrainDict[direction_key][0]
    testPointsY = stressStrainDict[direction_key][1]

    rawDataPoints = np.stack((testPointsX,testPointsY),axis=-1)

    # Bin the data values
    indx_bins, bins = _getBinIndexOfNumpyArrays(testPointsX, binsize=bin_size)
    testArray, used_bins = _binDataFromIndices(testPointsY, indx_bins, bins)
    if len(testArray) > windowWidth:
        testArray = signal.savgol_filter(testArray, windowWidth, 2, deriv=0,
                                             delta=1.0, axis=-1, mode='interp', cval=0.0)

    # bins = (bins[1:] + bins[:-1]) / 2.
    # print("number of bins: ", used_bins.shape)

    binnedData = np.stack((used_bins,testArray),axis=-1)
    outputDict = {'Raw Data': rawDataPoints, 'Binned Data': binnedData}
    # print("number of points: ", testArray.shape)
    # binnedRDP = rdp(binnedData,epsilon=eps_binned)

    # Get the linear parts of the data
    # rawRDP = rdp(rawDataPoints,epsilon=eps_raw)
    # print("Number of Points: ", binnedRDP.shape[0]self.propertiesDict)
    #
    # # 'Raw Data':rawDataPoints,'Raw RDP':rawRDP,
    # outputDict = {'Binned Data':binnedData,'Binned RDP':binnedRDP,
    #             'Raw Data':rawDataPoints,'Raw RDP':rawRDP}

    return outputDict

def _propsBothDirections(dataDicts,epsilon=0.01,datakey='Binned Data'):
    fullprops = {}

    fullprops = _getProperties(dataDicts['11'], datakey=datakey, eps=epsilon,
                                direction='11')

    fullprops = _getProperties(dataDicts['22'], datakey=datakey, eps=epsilon,
                                direction='22',inputDict=fullprops)

    return fullprops

def _getProperties(dataDict, datakey='Binned Data', eps=0.08, direction='11',
                    inputDict=None):

    props = ProcessTransitionProperties(stress_strain = dataDict[datakey], identifier=direction,
                                                                    eps=eps)
    props._setAllValues()
    propDict = props._outputAllValues(outputDict=inputDict)

    return propDict

def _plotter(dataDict):
    import random
    # {'Raw Data':rawDataPoints,'Raw RDP':rawRDP,
    # 'Binned Data':binnedData,'Binned RDP':binnedRDP}

    colors = ['r','b','y','g']
    colorCount = 0

    fig, ax = plt.subplots(figsize=(10,20))

    for data in dataDict:
        for key in dataDict[data]:

            params = _buildPlottingParameters(key)

            if 'RDP' in key:
                ax.plot(dataDict[data][key][...,0],dataDict[data][key][...,1],
                            label=params['label'],
                            alpha=params['alpha'], marker=params['marker'],
                            color=params['color'],zorder=params['zorder'],
                            linewidth=params['linewidth'])
            else:
                # Change colors from params['color']
                ax.scatter(dataDict[data][key][...,0],dataDict[data][key][...,1],
                            label=params['label'],
                            alpha=params['alpha'], marker=params['marker'],
                            color=colors[colorCount],zorder=params['zorder'],
                            linewidth=params['linewidth'])
                colorCount += 1

    ax.legend()
    plt.show()

if __name__ == "__main__":

    # topDir = '/home/richard/MyData/MechanicalData/Miriam_self.propertiesDictArticle/Biax/Biax_for_Elbow/AllSamples'
    # fnameList = os.listdir(topDir)
    MechanicalDataFolder = '/home/richard/MyData/MechanicalData/'
    DataSheet = os.path.join(MechanicalDataFolder,
                        'Uniax/DataSheets/UniaxNov28Presentation.csv')
    topDirBiax = os.path.join(MechanicalDataFolder,'Biax/RawData/')
    fnameList = BiaxDataParser()._getAllBiaxFiles(topDirBiax)

    # Use this to organize the 2 curves
    directions = ['11','22']
    rdp_epsilon = 0.01

    # For testing purpose
    # fnameList = fnameList[:5]
    # fnameList = [fnameList[9]]

    additionalColumns = ['MTMLow_','MaxStress_','MTMhigh_','T_Stress_Start_',
                        'T_Strain_Start_','T_Stress_End_','T_Strain_End_']
    additionalColumns = [col + d for col in additionalColumns for d in directions]
    dataSaver = BiaxDataOutput(DataSheet, checkCols={}, propertiesDict={},
                                addCols=additionalColumns)
    # print(len(dataSaver.outputDf))
    for fname in fnameList:

        try:

            print("Processing Sample: ", fname.split(".")[0])
            fullfname = os.path.join(topDirBiax, fname)

            stressStrainDict = BiaxDataParser()._buildStressStrain(fname)

            testDict = {direction:_processBiaxData(stressStrainDict, direction,
                            eps_raw = 0.08) \
                            for direction in directions}
            test = _propsBothDirections(testDict,epsilon=rdp_epsilon)

            columnEntries = _prepValuesForExport(fullfname)

            dataSaver.checkCols = columnEntries
            dataSaver.propertiesDict = test
            dataSaver._checkEntries()


        except Exception as e:
            print('Something is wrong with: ', fname)
            print(e)
    # print(len(dataSaver.outputDf))
    dataSaver._writeData("../../../DataSheets/checkMissing.csv")
