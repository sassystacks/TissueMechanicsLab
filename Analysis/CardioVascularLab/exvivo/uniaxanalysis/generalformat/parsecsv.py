#!/home/richard/anaconda2/bin/python

import pandas as pd
import os
import csv

'''
This class is used to get all of the info from user inputs to extract information from .csv files
and change the saved names to usable entries in a database.
'''


class parsecsv(object):

    def __init__(self, **kwargs):

        self.readDir = kwargs['readfrom']
        self.writeDir =kwargs['writeto']
        self.topDir = kwargs['topdir']
        self.identifier = kwargs['identifier']
        self.skiprows = kwargs['skiprows']
        self.project = kwargs['project']
        self.dimensions = kwargs['dimensions']

        self.fnames =

        #Check if there is a filetype to ignore
        if 'ignore' in kwargs:
            for name in self.fnames:
                if name.endswith(kwargs['ignore']):
                    self.fnames.remove(name)

    def parseNames(self, *args):
        #Takes a list of filenames and parses the time stamp and other data to obtain patient id and Specimen

        #Makes a list of the names with the identifier removed. Only works if identifier is on the end of
        #the name. Need to change this to make it mover robust. Probably use import re
        try:
            sampleNames = [name.split(" ")[0][:-len(self.identifier)] for name in self.fnames]
        except:
            sampleNames = [name.split(" ")[0] for name in self.fnames]

        return sampleNames

    def getTestDims(self,*args):
        #get width thickness and G-G from csv file
        fullDF = self.readDimsFile()

        dims = fullDF[["Width","Thickness","G-G"]]
        dims = dims.values.tolist()

        return dims

    def makeSearchNames(self, *args):
        #reads information from dimensions sheet and creates a list of patients to be analyzed
        fullDF = self.readDimsFile()

        nameparts = fullDF[["Sample","Specimen"]]
        nameparts = nameparts.values.tolist()
        searchNames = ["{}_{}".format(name[0],name[1]) for name in nameparts]

        return searchNames

    def dataEntry(self, *args):
        #returns the general info about the test, sample and speciment id
        fullnames = args[0]
        specimendata = [name.split("_") for name in fullnames]

        return specimendata

    def txtTocsv(self, *args):
        pass

    def readDimsFile(self, *args):
        #This should be changed to a cached class only if using
        #Read csv dimensions and populate list of patient and specimen concantenated
        df = pd.read_csv(self.dimensions)

        return df #Return pandas dataframe

    def findFile(self, *args):
        import time
        t0 =time.clock()
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print "starting loop at......." + str(t0)

        fileTofind = args[0]
        print "finding file ....... ",fileTofind

        for root,dirs,fname in os.walk(self.topDir):
            for f in fname:
                try:
                    if fileTofind in f and self.identifier in f:
                        found = f
                        print "found file..... ",f
                        return f
                        break
                except TypeError:
                    if fileTofind in f:
                        found = f
                        print "found file..... ",f
                        return f
                        break

    def getFnames(self, *args):

        searchNames = self.makeSearchNames()
        #files = files.tolist()
        b = [a.findFile(f) for f in d]

        if kwargs['identifier']:
            self.fnames = [name for name in os.listdir(self.readDir) if kwargs['identifier'] in name]

        else:
            self.fnames = [name for name in os.listdir(self.readDir)]


if __name__ == '__main__':
    #this is a sample to test outputs
    args_dict = {'readfrom': '/home/richard/MyProjects/TissueMechanicsLab/RawData/rawData',
                'dimensions': '/home/richard/MyProjects/TissueMechanicsLab/RawData/Allfiles.csv',
                'topdir': '/home/richard/MyProjects/TissueMechanicsLab/RawData/Test Data',
                'writeto': 'Test','identifier': '_Fail','skiprows': 5, 'ignore': '.tdf', 'project': 'AAA'}
    a = parsecsv(**args_dict )


    c = a.getTestDims()
    d = a.makeSearchNames()

    b = [a.findFile(f) for f in d]

    print(b)
    print(len(b))
