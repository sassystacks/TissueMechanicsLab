import sys
sys.path.append('..')

from RunBiaxElbowAnalysis import _getBinIndexOfNumpyArrays, \
                                 _binDataFromIndices, _processBiaxData, \
                                 _plotter, _propsBothDirections


from Analyzer.DataFilter import ExVivoDataUtils
from BiaxDataHandler import BiaxDataParser, BiaxDataOutput

import os
import numpy as np

def _truncateDataAbove(dataDict, dataKey, threshold=0):
    for key, v in dataDict.items():
        for i in range(2):
            indxs = np.where(dataDict[key][dataKey][:,i] > threshold)[0]
            dataDict[key][dataKey] = dataDict[key][dataKey][indxs]
    return dataDict

def _OutputBiaxData(dataDict,folderName, filename):
    import pandas as pd

    outputDict = _BuildBiaxOutput(dataDict)
    fullfname = os.path.join(folderName,filename)

    if not os.path.isdir(folderName):
        os.mkdir(folderName)

    # outputDF = pd.DataFrame().from_dict(outputDict)
    outputDF = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in outputDict.items() ]))
    outputDF.to_csv(fullfname,index=False)



def _BuildBiaxOutput(dataDict):

    outputDict = {}
    for key in dataDict:
        outputKey1 = "E" + key + "(dots)"
        outputkey2 = "S" + key
        outputDict[outputKey1] = dataDict[key]['Binned Data'][:,0]
        outputDict[outputkey2] = dataDict[key]['Binned Data'][:,1]
    return outputDict

def _BinData(folderIn, folderOut, filename):
    fullfname = os.path.join(folderIn, filename)
    stressStrainDict = BiaxDataParser()._buildStressStrain(fullfname,skip=1)

    testDict = {direction:_processBiaxData(stressStrainDict, direction,
                    eps_raw = 0.08, windowWidth = 31, bin_size=0.0005) \
                    for direction in directions}
    testDict = ExVivoDataUtils()._truncateDataAbove(testDict, 'Binned Data')

    for key in testDict:
        maxIndex =  np.argmax(testDict[key]['Binned Data'][:,1])
        testDict[key]['Binned Data'] = testDict[key]['Binned Data'][:maxIndex]

    output = _propsBothDirections(testDict, epsilon=0.01, datakey='Binned Data')


    _OutputBiaxData(testDict, folderOut, fname)

    return testDict

if __name__ == "__main__":

    directions = ['11','22']
    rdp_epsilon = 0.01

    # Stuff for file inputs
    MechanicalDataFolder = '/home/richard/MyData/MechanicalData/'
    topDirBiax = os.path.join(MechanicalDataFolder,'Biax/RawData/Medtronic')
    subDirs = os.listdir(topDirBiax)


    # Stuff for Outputs
    outputTopDir = os.path.join(topDirBiax,"Binned")
    if not os.path.isdir(outputTopDir):
        os.mkdir(outputTopDir)

    for sub in subDirs:
        fullSubDir = os.path.join(topDirBiax,sub)
        fnameList = os.listdir(fullSubDir)


        for fname in fnameList:
            if "2PK" in fname:
                try:

                    outputFolder = os.path.join(outputTopDir,sub)
                    outputDict = _BinData(fullSubDir, outputFolder, fname)
                    # _plotter(outputDict)
                except Exception as e:
                    print(e)
                    continue
