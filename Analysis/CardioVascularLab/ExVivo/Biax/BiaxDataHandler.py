import os
import pandas as pd
import numpy as np
#
# topDir = '/home/richard/MyData/MechanicalData/Biax/RawData/'

class BiaxDataParser:
    def __init__(self):
        pass

    def _getAllBiaxFiles(self,topDir):

        dirList = os.listdir(topDir)

        allFiles = []
        for d in dirList:
            checkDir = os.path.join(topDir,d)
            if os.path.isdir(checkDir):
                subDirList = os.listdir(checkDir)
                for s in subDirList:
                    fullfname = os.path.join(checkDir, s, 'all',
                                            '4Dots_Strain_2PK_1_1.txt')
                    if os.path.isfile(fullfname):
                        allFiles.append(fullfname)
        return allFiles

    def _breakDownFileName(self,fname,topPath='RawData',subdirIndices=2):
        fnameParts = fname.split(os.path.sep)

        return fnameParts

    def _getSubString(self, filepiece, forward=True):

        if forward:
            i = 0
            character = filepiece[i]
            while not filepiece[i+1].isdigit():
                i += 1
                character += filepiece[i]
        else:
            i = len(filepiece)-1
            character = filepiece[i]
            while filepiece[i-1].isdigit():
                i -= 1
                character += filepiece[i]
            # flip the order so that it matches the file and convert it
            # to a string
            character = int(character[::-1])
        return character

    def _getDataEntries(self, filepart):

        # breakdown the file parts into the parts we want for data export
        # this is super specific to the formating here
        patient = filepart.split("_")[2]
        zone = filepart.split("_")[3][1]
        region = self._getSubString(filepart.split("_")[3][2:])
        specimen  = self._getSubString(filepart.split("_")[3], forward=False)

        outDict = {'Patient':int(patient),'Zone':int(zone),'Region':region,
                            'Specimen':specimen}
        return outDict

    def _buildStressStrain(self, fname, skip=1, pairs={'11':['E11(dots)','S11'],
                                                    '22':['E22(dots)','S22']}):
        rawDataDF = pd.read_csv(fname, skiprows=skip)

        outputDict = {}
        for pair in pairs:
            # Set the value as the list of the the strain values
            testPointsX = rawDataDF[pairs[pair][0]].values
            testPointsY = rawDataDF[pairs[pair][1]].values

            # Truncate the data removing everything before 0.05
            # indices = BiaxDataFilter()._truncateDataIndices(testPointsX,
            #                                                 threshold=0.01)

            t_list = [testPointsX,testPointsY]
            # t_list = [BiaxDataFilter()._normalize(x) for x in t_list]
            # t_list = [x[indices] for x in t_list]
            outputDict[pair] = t_list

        return outputDict


class BiaxDataOutput:
    def __init__(self, fnameIn, checkCols={}, addCols = [], propertiesDict={}):

        self.outputDf = pd.read_csv(fnameIn)
        if addCols:
            headers = self.outputDf.columns.to_list() + addCols

            self.outputDf = self.outputDf.reindex(columns = headers)

        self.checkCols = checkCols
        self.propertiesDict = propertiesDict

        # Create an empty dictionary for all the columns in dataframe
        self.row_dict = {k:None for k in self.outputDf.columns.to_list()}

    def _fillRowDict(self,entries):
        for entry in entries:
            if entry in self.row_dict.keys():
                self.row_dict[entry] = entries[entry]

    def _checkEntries(self):


        if self.checkCols and self.propertiesDict:
            keys = [k for k in self.propertiesDict]
            vals = [self.propertiesDict[val] for val in self.propertiesDict]

            pd_index = (self.outputDf[list(self.checkCols)] == \
                    pd.Series(self.checkCols)).all(axis=1)
            if pd_index.any():
                self.outputDf.loc[pd_index,keys] = vals
            else:
                # print("Wasn't in there")
                self.checkCols.update(self.propertiesDict)
                self._fillRowDict(self.checkCols)
                # appender = pd.Series(self.row_dict)
                # appender.name = "Temp"
                self.outputDf = self.outputDf.append(self.row_dict,
                                                            ignore_index=True)


    def _writeData(self,fname):

        self.outputDf.to_csv(fname,index=False)

    def _setValues(self):
        pass

class BiaxDataFilter:

    def __init__(self):
        pass

    def _normalize(self,data):
        return (data - np.min(data))/(np.max(data) - np.min(data))

    def _truncateDataIndices(self, data, threshold=0.01):
        return np.where(data > threshold)[0]
