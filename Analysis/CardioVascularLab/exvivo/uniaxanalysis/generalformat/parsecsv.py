#!/home/richard/anaconda2/bin/python

import pandas as pd
import os


'''
This class is used to get all of the info from user inputs to extract information from .csv files
and change the saved names to usable entries in a database.

Use function getMatchingData(<directory_with_CSVs>,<directory_with_dimensions_file>)

Returns a list of filenames with width, thickness and G-G and sample_specimen for all tests
that match in a given directory.

To Do

'''


class parsecsv(object):

    def __init__(self, **kwargs):

        self.topDir = kwargs['topdir']
        self.identifier = kwargs['identifier']
        self.skiprows = kwargs['skiprows']
        self.dimsdir = kwargs['dimsdir']

        if 'ignore' in kwargs:
            self.ignore = kwargs['ignore']
        if 'writeto' in kwargs:
            self.writeDir = kwargs['writeto']
        if 'project' in kwargs:
            self.project = kwargs['project']

        self.sampleNames = self.makeSearchNames() #get specimen and sample names

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
        #uses the readDimsFile function to parse a pandas dataframe
        dimsFile =args[0]
        fullDF= pd.read_csv(dimsFile)


        dims = fullDF[["Sample","Specimen","Width","Thickness","G-G"]] #These sample values are returned
        dims = dims.values.tolist() #Converst dataframe to list

        return dims #return list

    def makeSearchNames(self, *args):
        #reads information from dimensions sheet and creates a list of sample and specimen
        #concantenated with an underscore Sample_Specimen. Used to search for raw data file
        fullDF = self.readDimsFile()

        nameparts = fullDF[["Sample","Specimen"]]
        nameparts = nameparts.values.tolist()
        searchNames = ["{}_{}".format(name[0],name[1]) for name in nameparts]

        return searchNames

    def dataEntry(self, *args):
        #returns the identifier in the test file as a list
        #sample and speciment id
        fullnames = args[0]
        specimendata = [name.split("_") for name in fullnames]

        return specimendata

    def cleanCsv(self, *args):
        import csv
        from itertools import islice

        #Takes a list of files, finds the text files and creates a .csv files
        #in the directory

        #Calls the get Fnames function to get the filenames list
        fnamelist = args[0]

        root = '/home/richard/MyProjects/TissueMechanicsLab/CleanSheets'
        try:
            os.mkdir(root)
        except OSError:
            print "directory exists..... writing to existing directory"

        newfNamelist = []
        for f in fnamelist:

            fullFname = os.path.join(root,f[1] + ".CSV")

            with open(f[0]) as inTxt, open(fullFname,"w") as outCsv:
                r = csv.reader(islice(inTxt, 5,None))
                outCsv = csv.writer(outCsv)
                outCsv.writerow(["time","Force","Displacement"])
                outCsv.writerows(r)
            newfNamelist.append([fullFname,f[1]])

        #return newfNamelist took out this return.... might want to put back
        #returns the filenames and sample_specimen matching it


    def readDimsFile(self, *args):
        #This should be changed to a cached class only if using
        #Read csv dimensions and populate list of patient and specimen concantenated

        df = pd.read_csv(self.dimsdir)

        return df #Return pandas dataframe

    def findFile(self, *args):

        fileTofind = args[0] #takes a substring to find matching files in the topDir
        topDir = args[1] #point to a directory to search

        for root,dirs,fname in os.walk(topDir):
            for f in fname:
                try:
                    if fileTofind in f and self.identifier in f and not f.endswith(self.ignore):

                        return os.path.join(root,f),fileTofind
                        break

                    elif args[2] and fileTofind in f:

                        return os.path.join(root,f),fileTofind
                        break

                except TypeError:
                    if fileTofind in f:

                        return os.path.join(root,f),fileTofind
                        break

    def getFnames(self, *args):
        #Returns a list of file names that match the sample and specimen names
        #Calls makeSearchNames to get the info

        searchNames = self.sampleNames #get specimen and sample names
        fnames = [self.findFile(f,self.topDir) for f in searchNames] #search the directories for matching sample/specimen
        fnames = [f for f in fnames if f is not None] #Remove NoneType

        return fnames #return list of full file names with root attached

    def getMatchingData(self, *args):
        #uses the dimensions file specifed by user to obtain dimensions
        #use a clean directory with all outlier files removed

        topDir = args[0] #Specify a directory to find files matching sample and specimen
        dimsDir = args[1]
        dimslist = self.getTestDims(dimsDir) #Get the dimesions of the sample and specimen

        fullList = []
        for dims in dimslist:
            sampleSpecimen = dims[0] + "_" + dims[1] # join sample and specimen to compare

            fname = self.findFile(sampleSpecimen,topDir,'Noidentifier')
            if fname is not None:
                # Make list of sample_specimen, filename of CSV,
                fullList.append([sampleSpecimen,fname[0],dims[2],dims[3],dims[4]])

        return fullList

if __name__ == '__main__':
    #this is a sample to test outputs
    args_dict = {
                'dimsdir': '/home/richard/MyProjects/TissueMechanicsLab/RawData/Allfiles.csv',
                'topdir': '/home/richard/MyProjects/TissueMechanicsLab/RawData/cp_Test_Data',
                'writeto': 'Test','identifier': '_Fail','skiprows': 5, 'ignore': '.tdf', 'project': 'AAA'}
    a = parsecsv(**args_dict )
    d = a.getMatchingData('/home/richard/MyProjects/TissueMechanicsLab/CleanSheets',
                        '/home/richard/MyProjects/TissueMechanicsLab/RawData/Allfiles.csv')
    print(len(d))
