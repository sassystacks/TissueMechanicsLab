import numpy as np
import uniaxanalysis.getproperties as getprops
from uniaxanalysis.plotdata import DataPlotter
from uniaxanalysis.saveproperties import write_props_csv
from uniaxanalysis.parsecsv import parsecsv

class mainFunc:

    def __init__(self,failfilesdir=None,measurementsfile=None,outputfile=None,
                    stresstype,straintype):

        # file management
        self.failFilesDir = failfilesdir
        self.measurementsFile = measurementsfile
        self.outputFile = outputfile

        # properties
        self.props = None
        self.stresstype = stresstype
        self.straintype = straintype

        # Things to output
        self.elbowStartIndex = None
        self.elbowEndIndex = None
        self.failure = None
        self.stiffness = None

    def _runOneSample(self,faildir,measurements,outputs={},outputfname=None):
        '''
        This function runs one sample that is passed in as measurements.

        Input:
            - faildir = a directory containing the fail file
            - measurements = a dictionary with a string as sample name and float for rest:
                {sample: 'samplename',length: 12, width: 2, thickness: 2}
            - outputs = Boolean dictionary in the form:
                {strength: True, stiffness: True, elbowregion: True}
        output:
            - a csv file with the sample and the outputs if passed a file
            - prints to the terminal the values
        '''
        pass

    def _runFromCSVandTopDir(self,topdir,measurementfile,outputfile=None,
                            outputs=['Sample','Strength','Stiffness']):
        '''
        This function runs one sample that is passed in as measurements.

        Input:
            - topdir = a directory containing the fail files (searches recursively)
            - measurementfile = a csv file containing information
            - outputs = Boolean dictionary in the form:
                {strength: True, stiffness: True, elbowregion: True}
        output:
            - a csv file with the sample and the outputs appended to existing csv
              if it exists or creates the file
        '''

        # this outputs a list conisting of in the form:
        # [sample,filename,width,thickness,length]
        analysisList = parsecsv().getMatchingData(measurementfile, topdir)

        propList = []
        for analysis in analysisList:

            props = getprops(fileDimslist=analysis, smooth_width=29,
                              std=7, chkderivate=0.04, stresstype=self.stresstype,
                              straintype=self.straintype)

            listToAppend = self._buildOutputListForCSV(props,outputs)

    def _buildOutputListForCSV(self,props,outputs):
        outputList = []
        if 'Sample' in outputs:
            outputList.append(props.sample)
        else:
            print('Need to input a sample name')

        if 'Strength' in outputs:
            outputList.append(props.strength)
        if 'Stiffness' in outputs:
            outputList.append(props.stiffness)
        if 'StartElbow' in outputs:
