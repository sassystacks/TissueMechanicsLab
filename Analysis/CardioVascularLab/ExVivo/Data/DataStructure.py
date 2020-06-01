'''
This class is built to structure data types for each step in the mechanical
testing analysis pipeline. The class returns a data container in the form
of a python dictionary and is dependent on the parameters input. Biax data
has 2 direction components, uniax data has 1. And therefore the biax data is a
dictionary containing 2 data structures in the form. Each data container
contains a data structure which is determined by the data container parameters:

Example dataContainer:

Biax Data - {'DataType': 'Biax', 'Project': 'NIH',
             'Sample': 'Z2GC5', Direction: 'Both', '11': {datastructure},
             '22': {datastructure}}

Uniax Data - {'DataType': 'Uniax','Project': 'NIH','Sample': 'Z2GC5',
              'Direction': '11', '11': {datastructure}}

Parameters:
    dataType: {'Raw','Processed','Analyzed'... default = 'Analyzed'}
    testtype: {'Biax','Biax',... default = 'Uniax'}

    kwargs:
    project: {eg ... 'AAA','NIH'}
    sample: {eg... 'Z2GC7'}
    direction: {'11','22'}

    datastructure:

    stresstype: {'PK1','PK2','Cauchy'... default = 'cauchy'}
    straintype: {'Green','Stretch','Engineering'... default = 'Engineering'}


Returns:

_RawData is data directly from the testing sources,
_ProcessedData is data that has been converted into stress and strain,
_AnalyzedData is data that has been analyzed with the properties attached
'''

import numpy as np

class ExVivoData:

    def __init__(self, datatype='Analyzed', testtype='Uniax',
                    stresstype='cauchy',straintype='Engineering', **kwargs):


        self.dataContainer = {'DataType':dataType, 'TestType':testtype,
                              'Project':project, 'Sample':sample,
                              'Direction':direction}


        self.datastructure = {}


    def _initializeFields(self, fields, valueType):

        for field in fields:
            self.datastructure[fields] = valueType

    def _RawData(self, fields=['Force','Displacement']):

        self._initializeFields(fields, np.array([]))

    def _ProcessedData(self,fields=['Stress','Strain']):

        self._initializeFields(fields, np.array([]))

    def _AnalyzedBiaxData(self,fields=['LTM','HTM','RDP','MaxStress',
                            'T_strain_start','T_stress_start',
                            'T_strain_end','T_strain_end']):

        self._initializeFields(fields, valueType)
