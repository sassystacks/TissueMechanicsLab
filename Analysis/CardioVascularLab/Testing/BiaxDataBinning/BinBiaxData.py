import sys
sys.path.append('../../ExVivo')


'''

'''
from biax.RunBiaxElbowAnalysis import _getBinIndexOfNumpyArrays, \
                                 _binDataFromIndices, _processBiaxData, \
                                  _propsBothDirections



from Analyzer.DataFilter import ExVivoDataUtils
from Analyzer.DataClusters import DataClusterAnalysis as Clusterer

from biax.BiaxDataHandler import BiaxDataParser, BiaxDataOutput

from Visualizer.PlotsForBinnedData import BinnedDataPlotter as plotter

import os
import numpy as np


class BiaxDataBinner:

    def __init__(self):
        pass

    def _OutputBiaxData(self,dataDict,fullfname):
        import pandas as pd

        outputDict = self._BuildBiaxOutput(dataDict)



        # outputDF = pd.DataFrame().from_dict(outputDict)
        outputDF = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in outputDict.items() ]))
        outputDF.to_csv(fullfname,index=False)


    def _BuildBiaxOutput(self, dataDict):

        outputDict = {}
        for key in dataDict:
            outputKey1 = "E" + key + "(dots)"
            outputkey2 = "S" + key
            outputDict[outputKey1] = dataDict[key]['Binned Data'][:,0]
            outputDict[outputkey2] = dataDict[key]['Binned Data'][:,1]
        return outputDict

    def _BuildReadFormat(self, fname):
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

    def _BinByCluster(self, stressStrainDict,clusterWidth):
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

    def _BinData(self, stressStrainDict, clusterWidth):
        outputDict = {k:{} for k in stressStrainDict}

        t_dict = self._BinByCluster(stressStrainDict, clusterWidth)



        for k in stressStrainDict:
            outputDict[k]['Raw Data'] =  np.stack((stressStrainDict[k][0],
                                                   stressStrainDict[k][1]),axis=-1)
            outputDict[k]['Binned Data'] =  np.stack((t_dict[k]['Binned Data'][0],
                                                   t_dict[k]['Binned Data'][1])
                                                                          ,axis=-1)
            outputDict[k]['Clusters'] =  t_dict[k]['Clusters']

        return outputDict

    def _RunBiaxBinData(self, filename, clusterWidth=[0.001, 0.01],
                    fullfnameOut="",
                    analyze=False, readformat = {'11':['E11(dots)','S11'],
                                                '22':['E22(dots)','S22']}):


        stressStrainDict = BiaxDataParser()._buildStressStrain(filename,skip=1,
                                                            pairs=readformat)


        outputDict = self._BinData(stressStrainDict, clusterWidth)

        if analyze:
            outputProps = _propsBothDirections(outputDict,
                                               epsilon=0.01, datakey='Binned Data')


        if fullfnameOut:
            self._OutputBiaxData(outputDict, fullfnameOut)

        return outputDict

def _BuildInputFolderFilenames(f,ftype):
    if ftype == 'fof': # Folder of Folders
        # Stuff for file inputs
        # MechanicalDataFolder = '/home/richard/MyData/MechanicalData/'
        # topDirBiax = os.path.join(MechanicalDataFolder,'Biax/RawData/Medtronic')
        topDir = f
        subDirs = [os.path.join(f,sub) for sub in os.listdir(f)]

        # Create a list of lists for the files in each subdirectory
        fnameList = [os.listdir(os.path.join(f,sub)) for sub in subDirs]

    elif ftype == 'fo': # single folder

        # if it is a single folder set the filenames list to all files in the
        # folder
        topDir = f
        subDirs = [f]
        fnameList = os.listdir(f)

    else: # Single file

        fileparts = os.path.split(f)

        topDir = fileparts[0]
        subDirs = [fileparts[0]]
        fnameList = [fileparts[1]]

    return topDir, subDirs, fnameList

def _BuildOutputFileNames(outputTopDir, sub, fname, ftype):
    '''
    Mainly for creating the folder of folders in the directory.... stores each
    in the 'Binned_AllFiles' directory under the top directory. If it does not
    exist then it creates it.
    '''
    if ftype == 'fof': # Folder of Folders
        outputDir = os.path.join(outputTopDir,os.path.split(sub)[1])

        if not os.path.isdir(outputDir):
            os.mkdir(outputDir)

        fnameOut = os.path.join(outputDir,fname)

    else: # Single file
        fnameOut = os.path.join(outputTopDir,fname)

    return fnameOut

def main(f, ftype, save_output=False, clusterParams=[0.001, 0.005],
                                    directions=['11','22'], visualize=False):

    '''
    Main function to run the binning of the biax data. Pass in a folder of
    folders holding biax data, a folder holding biax data, or an individual file
    of biax data. Folders can only have biax data in them... no other file or
    folder types

    Parameters:
        Required:
            f - <string> folder of folders, folder, or file to bin
            ftype - <string> that specifies which type f is <'fof','fo','f'>
        Optional:
            save_files - <bool> whether or not to save the outputs
            directions - <list of strings> which directions to analyze
            visualize - <bool> whether or not to plot and show the outputs

    Returns:
        None
    '''

    # sort out these variables based on the input type
    topDir, subDirs, t_fnameList = _BuildInputFolderFilenames(f, ftype)


    # if saving the outputs create the directory to output to
    if save_output:
        # Stuff for Outputs
        outputTopDir = os.path.join(topDir,"Binned_AllFiles")
        if not os.path.isdir(outputTopDir):
            os.mkdir(outputTopDir)




    # enumerate the list for a folder of folders
    for i,sub in enumerate(subDirs):
        if ftype == 'fof':
            # if it is a folder of folders get all files for each folder
            fnameList = t_fnameList[i]
        else:
            fnameList = t_fnameList

        for fname in fnameList:
            try:
                # set the filename out to be an empty string,
                # and only change it if asked to
                # save the output... ie save_output=True
                if save_output:
                    fnameOut = _BuildOutputFileNames(outputTopDir, sub,
                                                                fname, ftype)
                else:
                    fnameOut = ""

                Binner = BiaxDataBinner()
                format = Binner._BuildReadFormat(fname)
                fullFileName = os.path.join(sub,fname)
                outputDict = Binner._RunBiaxBinData(fullFileName,
                                                    readformat=format,
                                            clusterWidth=clusterParams,
                                            fullfnameOut=fnameOut)
                if visualize:
                    a = plotter(outputDict)
                    a._plot(title=fname.split(".")[0])

            except Exception as e:
                print("Exception in {0} for sample {1}".format(fname,sub))
                print(e)
                continue

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(prog='BinBiaxData', description="""
                                        This is a command line based
                                        program that can be used to bin biaxial
                                        data that has been analyzed previously.
                                        Example usage: python BinBiaxData.py
                                        -f <path to file> -t 0.001 -m 0.01 -v""")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-fof','--folder_of_folders',
                        help="""Enter a folder of folders to have the data
                                binned""")
    group.add_argument('-fo','--folder',
                        help="Enter an entire folder to have the data binned")
    group.add_argument('-f','--file',
                            help="Enter a single file to have the data binned")
    parser.add_argument('-t','--threshold',default=0.001,type=float,
                        help="""maximum distance between points that includes
                                points in a cluster, if exceded a new cluster
                                is created""")
    parser.add_argument('-m','--maximum',default=0.01,type=float,
                        help="""maximum distance that the first point in a
                                cluster and the nth point in a cluster are
                                considered to be contained within the cluster
                                """)
    parser.add_argument('-v','--visualize',action='store_true',help="""
                                    pass this argument to visualize the data
                                    it will visualize each plot so it is
                                    best used with individual files or one
                                    folder of data, not folder of folders""")
    parser.add_argument('-s','--save',action='store_true',
                        help="""pass this argument to save the binned data""")
    # parser.add_argument('-h','--help', )

    args = parser.parse_args()
    if args.folder_of_folders:
        f = args.folder_of_folders
        ftype = 'fof'
    elif args.folder:
        f = args.folder
        ftype = 'fo'
    else:
        f = args.file
        ftype = 'f'

    main(f,ftype,clusterParams=[args.threshold, args.maximum],
                    visualize=args.visualize, save_output=args.save)
