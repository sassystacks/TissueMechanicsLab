import sys, os
sys.path.append('..')
import pandas as pd

'''
This class is used to extract the data from the biax .csv files and change saved names to be used
in a database
fname = name of txt file (ex: 4Dots_Strain_2PK_1_1.txt)
allFiles  = full path names down to txt files

'''

class ReadBiaxData(object):

    def __init__(self, **kwargs):

        self.topdir = kwargs['topdir']
        self.identifier = kwargs.get('identifier', None)
        self.specimenHeaders = kwargs.get('specimenHeaders', ['Sample'])
        self.headersOut = kwargs.get('headersOut', ['Sample', 'Stiffness',
                                                    'Strength'])
        self.ftype = kwargs.get('ftype', ["FileType"])
        self.dataType = kwargs.get('datatype', ["DataType"])

        self.fileList = self._getAllBiaxFiles(self.topdir)
        self.sampleNames = self._breakdownFileName(self.fileList)

        # create an empty pandas df to store the returns
        self.outputDict = {}
        self.df = None


    def _123getAllBiaxFiles(self, topdir):

        dirList = os.listdir(topdir)

        allFiles = []
        for d in dirList:
            # this will join the directory path with the subdirectories within
            checkDir = os.path.join(topdir, d)
            # isdir() checks if the specified path is an existing directory or not
            if os.path.isdir(checkDir):
                # listdir() returns a list containing the names of the entries in the directory
                # given by the path
                subDirList = os.listdir(checkDir)
                for s in subDirList:
                    fullfname = os.path.join(checkDir, s, self.ftype)
                    if os.path.isfile(fullfname):
                        allFiles.append(fullfname)
        return allFiles

    def _getAllBiaxFiles(self, topdir):

        dirList = os.listdir(topdir)

        allFiles = []
        for d in dirList:
            # this will join the directory path with the subdirectories within
            checkDir = os.path.join(topdir, d)
            # isdir() checks if the specified path is an existing directory or not
            if os.path.isdir(checkDir):
                # listdir() returns a list containing the names of the entries in the directory
                # given by the path
                subDirList = os.listdir(checkDir)
                if self.dataType == 'Unbinned':
                    # fullfname = os.path.join(checkDir, '40%/all', self.ftype) # FOR AAA
                    fullfname = os.path.join(checkDir, 'all', self.ftype) #FOR NIH-BAV
                    if os.path.isfile(fullfname):
                        allFiles.append(fullfname)
                if self.dataType == 'Binned':
                    # fullfname = os.path.join(checkDir, '40%/Binned_AllFiles', self.ftype) #FOR AAA
                    fullfname = os.path.join(checkDir, 'Binned_AllFiles', self.ftype) # FOR NIH_BAV
                    allFiles.append(fullfname)
        return allFiles

    def _breakdownFileName(self, fileList, topPath='RawData', subdirIndices=2):
        # this function breaks the path name into parts
        fnamePartsDict = []
        for fname in fileList:
            fnameParts = fname.split(os.path.sep)
            fnamePartsDict.append(fnameParts[-3])
        self._nameDataEntries(fnamePartsDict)
        return fnamePartsDict

    def _makeSampleList(self, sampleNames, fileList):
        sampleList = list(zip(sampleNames, fileList))
        print(sampleList)
        return sampleList

    #this function could use some work, but it splits the filename into characters and
    #finds characters to describe zone, region, patient number, specimen number and returns
    #it to _nameDataEntries
    def _getSubString(self, filepiece, forward=False, zone=False):
        filepiece = [char for char in filepiece]
        if zone:
            character = filepiece[1]
        elif forward:
            i=0
            character = filepiece[i]
            while not filepiece[i+1].isdigit():
                i+=1
                character += filepiece[i]
        else:
            i=len(filepiece)-1
            character = filepiece[i]
            while filepiece[i-1].isdigit():
                i-=1
                character += filepiece[i]
            #flip the order so it matches the file and convert to a string
            character = int(character[::-1])

        return character

    def _nameDataEntries(self, filepartList):
        # breakdown file parts into what we need for data export
        patientList = []
        zoneList = []
        regionList = []
        specimenList = []

        for filepart in filepartList:
            splitName = filepart.split("_")

            patientList.append(splitName[-2])

            zoneList.append(self._getSubString(splitName[-1], zone=True))

            # regionList.append(self._getSubString(splitName[-1], forward=True)) #NIHBAV DATA
            regionList.append(splitName[-1]) # AAA DATA

            specimenList.append(self._getSubString(splitName[-1], forward=False))

        outDict = {'Patient': patientList, 'Zone':zoneList, 'Region': regionList, 'Specimen': specimenList}
        return outDict


class BiaxDataOutput:

    def __init__(self, fnameIn, checkCols={}, addCols=[], propertiesDict={}):
        self.outputDf = pd.read_csv(fnameIn)
        if addCols:
            headers = self.outputDf.columns.to_list() + addCols

            self.outputDf = self.outputDf.reindex(columns=headers)

        self.checkCols = checkCols
        self.propertiesDict = propertiesDict

        # Create an empty dictionary for all the columns in dataframe
        self.row_dict = {k: None for k in self.outputDf.columns.to_list()}

    def _fillRowDict(self, entries):
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
                self.outputDf.loc[pd_index, keys] = vals
            else:
                # print("Wasn't in there")
                self.checkCols.update(self.propertiesDict)
                self._fillRowDict(self.checkCols)
                # appender = pd.Series(self.row_dict)
                # appender.name = "Temp"
                self.outputDf = self.outputDf.append(self.row_dict,
                                                     ignore_index=True)

    def _writeData(self, fname):

        self.outputDf.to_csv(fname, index=False)





