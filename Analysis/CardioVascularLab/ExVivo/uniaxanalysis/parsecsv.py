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

        self.dimsFile = kwargs['dimsfile']
        self.topDir = kwargs['topdir']

        self.identifier = kwargs.get('identifier', None)
        self.ignore = kwargs.get('ignore', '.tdf')
        if 'writeto' in kwargs:  # Directory to write
            self.writeDir = kwargs['writeto']
        if 'project' in kwargs:  # Project type
            self.project = kwargs['project']
        if 'identifier' in kwargs:
            self.identifier = kwargs['identifier']
        if 'skiprows' in kwargs:
            self.skiprows = kwargs['skiprows']

        self.sampleNames = self.makeSearchNames()  # get specimen and sample names

    def parseNames(self, *args):
        # Takes a list of filenames and parses the time stamp and other data to obtain patient id and Specimen

        # Makes a list of the names with the identifier removed. Only works if identifier is on the end of
        # the name. Need to change this to make it mover robust. Probably use import re
        try:
            sampleNames = [name.split(" ")[0][:-len(self.identifier)] for name in self.fnames]
        except:
            sampleNames = [name.split(" ")[0] for name in self.fnames]

        return sampleNames

    def getTestDims(self, dimsFile):
        # get width thickness and G-G from csv file
        # uses the readDimsFile function to parse a pandas dataframe

        fullDF = pd.read_csv(dimsFile)  # get a pandas dataframe for full csv file



        try:
            dims = fullDF[["Patient", "Zone","Region","Specimen","Direction", "Width",
                            "Thickness", "Length"]]
        except KeyError:

            try:
                dims = fullDF[["Patient", "Specimen", "Width", "Thickness", "Length"]]
            # If there is no Specimen sample difference use this
            except KeyError:
                dims = fullDF[["Sample", "Width", "Thickness", "Length"]]

        if not dims.empty:
            dims = dims.values.tolist()  # Converst dataframe to list
            return dims  # return list

        # If there isn't a list of dimensions
        else:
            print("The CSV file is not formated correctly see the docs for more info")

    def makeSearchNames(self, *args):
        # reads information from dimensions sheet and creates a list of sample and specimen
        # concantenated with an underscore Sample_Specimen. Used to search for raw data file
        fullDF = self.readDimsFile()

        try:
            nameparts = fullDF[["Patient", "Specimen"]]
            nameparts = nameparts.values.tolist()
            searchNames = ["{}_{}".format(name[0], name[1]) for name in nameparts]
        except KeyError:
            nameparts = fullDF[["Sample"]]
            searchNames = nameparts.values.tolist()
        if searchNames:
            return searchNames
        else:
            print("The CSV file is not formated correctly see the docs for more info")

    def dataEntry(self, *args):
        # returns the identifier in the test file as a list
        # sample and speciment id
        fullnames = args[0]
        specimendata = [name.split("_") for name in fullnames]

        return specimendata

    def cleanCsv(self, fnamelist, root):
        import csv
        from itertools import islice

        # Takes a list of files, finds the text files and replicates the data as
        # a csv file specified in the directory specified in root. The new names
        # is then <sample>_<specimen>.CSV in root

        try:
            os.mkdir(root)
        except OSError:
            print ("directory exists..... writing to existing directory")

        newfNamelist = []
        for f in fnamelist:

            fullFname = os.path.join(root, f[1] + ".CSV")

            # Based on the format that comes out of our machine
            with open(f[0]) as inTxt, open(fullFname, "w") as outCsv:
                r = csv.reader(islice(inTxt, 5, None))
                outCsv = csv.writer(outCsv)
                outCsv.writerow(["time", "Displacement", "Force"])
                outCsv.writerows(r)
            newfNamelist.append([fullFname, f[1]])

        # return newfNamelist took out this return.... might want to put back
        # returns the filenames and sample_specimen matching it

    def readDimsFile(self, *args):
        # This should be changed to a cached class only if using
        # Read csv dimensions and populate list of patient and specimen concantenated

        df = pd.read_csv(self.dimsFile)

        return df  # Return pandas dataframe

    def findFile(self, fileTofind, topDir, *args):

        # Finds files matching a substring. Recursively searches directory to find
        # The first file that matches while ignoring the ignore specified in __init__()
        # pass
        # fileTofind : takes a substring to find matching files in the topDir
        # topDir : point to the top directory to search Recursively from

        for root, dirs, fname in os.walk(topDir):
            for f in fname:
                try:  # This will
                    if fileTofind in f and self.identifier in f and not f.endswith(self.ignore):

                        return os.path.join(root, f), fileTofind
                        break

                    elif args[0] and fileTofind in f:

                        return os.path.join(root, f), fileTofind
                        break

                except TypeError:  # None type causes error in the above if statement so
                                  # this will avoid that problem
                    if fileTofind in f:

                        return os.path.join(root, f), fileTofind
                        break

    def getFnames(self, *args):
        # Returns a list of file names that match the sample and specimen names
        # Calls makeSearchNames to get the info

        searchNames = self.sampleNames  # get specimen and sample names
        # search the directories for matching sample/specimen
        fnames = [self.findFile(f, self.topDir) for f in searchNames]
        fnames = [f for f in fnames if f is not None]  # Remove NoneType

        return fnames  # return list of full file names with root attached

    def getMatchingData(self, dimsfile, topDir):
        # uses the dimensions file specifed by user to obtain dimensions
        # use a clean directory with all outlier files removed

        dimslist = self.getTestDims(dimsfile)  # Get the dimesions of the sample and specimen

        fullList = []

        for dims in dimslist:

            try:
                sampleSpecimen = dims[0] + "_Z" + str(dims[1]) + str(dims[2]) + str(dims[3]) + "_" + str(dims[4])  # join sample and specimen to compare
                width = 5
                thickness = 6
                g_g = 7

            except TypeError:
            
                try:
                    sampleSpecimen = dims[0] + "_" + dims[1]  # join sample and specimen to compare
                    width = 1
                    thickness = 2
                    g_g = 3
                except TypeError:
                    sampleSpecimen = dims[0]
                    width = 1
                    thickness = 2
                    g_g = 3

            if dims:
                fname = self.findFile(sampleSpecimen, topDir, 'Noidentifier')
                if fname is not None:
                    # Make list of sample_specimen, filename of CSV,
                    fullList.append([sampleSpecimen, fname[0], dims[width],
                                     dims[thickness], dims[g_g]])
                    print([sampleSpecimen, fname[0], dims[width],
                                     dims[thickness], dims[g_g]])
            else:
                print("Something is wrong with format of CSV, look at the docs ")
        return fullList


if __name__ == '__main__':
    # this is a sample to test outputs
    args_dict = {
        'dimsfile': '/home/richard/MyProjects/TissueMechanicsLab/RawData/Allfiles.csv',
        'topdir': '/home/richard/MyProjects/TissueMechanicsLab/RawData/cp_Test_Data',
        'writeto': 'Test', 'identifier': '_Fail', 'skiprows': 5, 'ignore': '.tdf', 'project': 'AAA'}
    a = parsecsv(**args_dict)
    d = a.getMatchingData(
        '/home/richard/MyProjects/TissueMechanicsLab/RawData/Allfiles.csv',
        '/home/richard/MyProjects/TissueMechanicsLab/CleanSheets'
    )
    print(d)
