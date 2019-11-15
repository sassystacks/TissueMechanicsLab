
# from tkFileDialog import *
import uniaxanalysis.getproperties as getprops
from uniaxanalysis.saveproperties import write_props_csv
import time

class UniaxAnalysis:

    def __init__(self):
        # print "Start Page class started"

        # Some properties that Rubab and Mohammaded complained soooooooooo much
        # to get..... jesus Muba
        self.straintype = 'engineering' # can change to engineering, and lamda
        self.stresstype = 'cauchy' # can change between cauchy and piola

        # For Data Extraction
        self.specimenHeaders = ["Sample", "Zone", "Region", "Specimen", "Direction"]
        self.dimensionHeaders = ["Width","Thickness","Length"]

        self.headersOut = ["Sample", "Zone", "Region", "Specimen", "Direction",
                            "PointID","Strength","Stiffness"]
        self.fileform = ["Sample", "_", "Z", "Zone", "Region",
                        "Specimen", "_", "Direction"]

        self.fname = '/home/richard/MyData/MechanicalData/Uniax/DimensionsFiles/NIH_Dimensions_newest.csv'
        self.dirname = '/home/richard/MyData/MechanicalData/Uniax/Fail_Files/'

        # test things
        self.fnameOut = 'TestOutputs.csv'

        self.sampleList = []

    def setupData(self):

        # check if there is an fname and a diself.sampleListrname
        if self.fname and self.dirname:
            import uniaxanalysis.parsecsv
            # Dictionary to pass to parsecsv for obtaining data on specimen
            args_dict = {
                'dimsfile': self.fname,
                'topdir': self.dirname,
                'timestep': 0.05,
                'headersOut': self.headersOut,
                'specimenHeaders': self.specimenHeaders,
                'dimsHeaders': self.dimensionHeaders,
                'fileform': self.fileform,
            }

            # instantiate parsecsv class to get the data to plot and analyze
            self.csvDataParser = uniaxanalysis.parsecsv(**args_dict)

            # Create the list of specimens to be tested from Dimensions file
            self.sampleList = self.csvDataParser.getMatchingData(
                                                    self.csvDataParser.dimsFile,
                                                    self.csvDataParser.topDir)
        else:
            print("please get a directory and a dimensions file for the analysis")

    def loopSamples(self):

        for sample in self.sampleList:
            try:
                self.setProps(sample)
                self.writeProps()
            except:
                print("Problem with getting properties for ", sample[0])
                continue

    def writeProps(self):
        # Add stiffness to the list, if not append an empty string
        if self.props.stiffness:
            self.csvDataParser.outputDict[self.props.sample]['Stiffness'] \
                                                        = self.props.stiffness

        else:
            self.csvDataParser.outputDict[self.props.sample]['Stiffness'] \
                                                        = "NaN"

        # Add strenght to the list, if not append an empty string
        if self.props.strength:
            self.csvDataParser.outputDict[self.props.sample]['Strength'] \
                                                        = self.props.strength
        else:
            self.csvDataParser.outputDict[self.props.sample]['Strength'] \
                                                        = "NaN"

        # Write the properties to the csv file specified
        write_props_csv(self.fnameOut, self.csvDataParser.outputDict,
                                        self.props.sample, self.headersOut)

    def setProps(self, sample):

        self.props = getprops(fileDimslist=sample, smooth_width=29,
                              std=7, chkderivate=0.04, stresstype=self.stresstype,
                              straintype=self.straintype)


    def main(self):
        self.setupData()
        self.loopSamples()

if __name__ == "__main__":

    UniaxAnalysis().main()
