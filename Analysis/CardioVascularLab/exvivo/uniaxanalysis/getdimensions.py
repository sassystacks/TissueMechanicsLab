import pandas as pd
from generalformat import parsecsv
from numpy import genfromtxt

'''
Reads in dimensions and extracts the necessary information from it
'''
class getdata(parsecsv):

    def __init__(self, **kwargs):

        super(getdata, self).__init__(**kwargs)
        self.fullDF = self.readDimsFile()
        self.skip = kwargs['skipheader']

    def getdimensions(self, *args):
        #opens Csv and reads all of the entries. Returns a dict of sample specimen
        #width, length, and grip to grip distance at the time of testing

        dims =self.fullDF.loc[:,"G-G":"Thickness"]
        dims = dims.values.tolist()

        return dims

    def getRawDataFiles(self, *args):

        files = fullDF.loc[:,"Filename"]
        files = files.tolist()

        return files

    def getForceStrain(self, *args):

        filename = args[0]
        my_data = genfromtxt(filename, delimiter=',', skip_header= = self.skip)

if __name__ == '__main__':
    #this is a sample to test outputs
    args_dict = {'readfrom': '/home/richard/MyProjects/TissueMechanicsLab/RawData/rawCSVfail/AAA20171003',
                'dimensions': '/home/richard/MyProjects/TissueMechanicsLab/RawData/Allfiles.csv',
                'topdir': '/home/richard/MyProjects/TissueMechanicsLab/RawData/Test Data',
                'writeto': 'Test','identifier': '_Fail','skiprows': 5, 'ignore': '.tdf', 'project': 'AAA'}
    getdimensions(**args_dict )
