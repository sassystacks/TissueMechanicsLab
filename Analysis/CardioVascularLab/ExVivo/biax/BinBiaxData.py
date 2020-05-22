import sys
sys.path.append('..')

from RunBiaxElbowAnalysis import _getBinIndexOfNumpyArrays, \
                                 _binDataFromIndices, _processBiaxData, \
                                  _propsBothDirections


from Analyzer.DataFilter import ExVivoDataUtils
from Analyzer.DataClusters import DataClusterAnalysis as Clusterer

from BiaxDataHandler import BiaxDataParser, BiaxDataOutput

from Visualizer.PlotsForBinnedData import BinnedDataPlotter as plotter

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

def _BuildReadFormat(fname):
    '''
    This is for obtaining the correct column names based on the filenames. This
    is a super rigid way of doing it, so if anything changes in the filenaming
    or column naming it will break.
    '''
    readformat = {'11':[],'22':[]}
    if 'Strain' in fname:
        readformat['11'].append('E11(dots)')
        readformat['22'].append('E22(dots)')
    elif 'Stretch' in fname:
        readformat['11'].append('L11(dots)')
        readformat['22'].append('L22(dots)')
    else:
        print("The filename was not recognized")
        raise ValueError("The filename was not recognized")

    if '2PK' in fname:
        readformat['11'].append('S11')
        readformat['22'].append('S22')
    elif '1PK' in fname:
        readformat['11'].append('P11')
        readformat['22'].append('P22')
    elif 'Cauchy' in fname:
        readformat['11'].append('T11')
        readformat['22'].append('T22')
    else:
        print("The filename was not recognized")
        raise ValueError("The filename was not recognized")

    return readformat

def _BinByCluster(stressStrainDict,clusterWidth):
    '''
    takes the values imput and finds chunks of data along the x axis
    and reduces both x and y data with in the chunk to an average value.

    inputs:
            stressStrainDict - dictionary with form {'11':[stress,strain],
                               '22':[stress,strain]} where stress/strain is a
                               numpy array
            clusterWidth - the width defining connectivity in a cluster, so if
                           a point is within clusterWidth it is considered
                           connected to the cluster
    '''

    outputDict = {k:{} for k in stressStrainDict}

    for i, k in enumerate(stressStrainDict):
        # Sort the data in the strain then sort the stress data based on that
        # sorting
        t_strain = np.sort(stressStrainDict[k][0])
        t_stress = stressStrainDict[k][1][stressStrainDict[k][0].argsort()]

        # Get the clusters of data as a single value for each
        outputDict[k]['Clusters'] = Clusterer()._clusterByData(t_strain, t_stress,
                                                            clusterWidth)
        averageClusters = Clusterer()._clusterDataStat(outputDict[k]['Clusters'], np.mean)


        outputDict[k]['Binned Data'] = [averageClusters[0],averageClusters[1]]





    return outputDict

def _BinData(folderIn, folderOut, filename, clusterWidth=[0.001, 0.01], output=False,
                analyze=False, readformat = {'11':['E11(dots)','S11'],
                                            '22':['E22(dots)','S22']}):

    fullfname = os.path.join(folderIn, filename)


    stressStrainDict = BiaxDataParser()._buildStressStrain(fullfname,skip=1,
                                                        pairs=readformat)
    outputDict = {k:{} for k in stressStrainDict}

    t_dict = _BinByCluster(stressStrainDict, clusterWidth)



    for k in stressStrainDict:
        outputDict[k]['Raw Data'] =  np.stack((stressStrainDict[k][0],
                                               stressStrainDict[k][1]),axis=-1)
        outputDict[k]['Binned Data'] =  np.stack((t_dict[k]['Binned Data'][0],
                                               t_dict[k]['Binned Data'][1])
                                                                      ,axis=-1)
        outputDict[k]['Clusters'] =  t_dict[k]['Clusters']



    if analyze:
        outputProps = _propsBothDirections(outputDict,
                                           epsilon=0.01, datakey='Binned Data')


    if output:
        _OutputBiaxData(outputDict, folderOut, fname)

    return outputDict

if __name__ == "__main__":


    directions = ['11','22']
    rdp_epsilon = 0.01

    # Stuff for file inputs
    MechanicalDataFolder = '/home/richard/MyData/MechanicalData/'
    topDirBiax = os.path.join(MechanicalDataFolder,'Biax/RawData/Medtronic')
    subDirs = os.listdir(topDirBiax)


    # Stuff for Outputs
    outputTopDir = os.path.join(topDirBiax,"Binned_AllFiles")
    # if not os.path.isdir(outputTopDir):
    #     os.mkdir(outputTopDir)

    for sub in [subDirs[0]]:

        # Get all files in the current directory
        fullSubDir = os.path.join(topDirBiax,sub)
        fnameList = os.listdir(fullSubDir)

        count = 0
        for fname in fnameList:
            if not os.path.isdir(fname):
                count += 1
                try:
                    format = _BuildReadFormat(fname)
                    outputFolder = os.path.join(outputTopDir,sub)
                    outputDict = _BinData(fullSubDir, outputFolder,
                                    fname,output=False,readformat=format)
                    if count % 5 ==0:
                        a = plotter(outputDict)
                        a._plot()
                except Exception as e:
                    print("Exception in {0} for sample {1}".format(fname,sub))
                    print(e)
                    continue
