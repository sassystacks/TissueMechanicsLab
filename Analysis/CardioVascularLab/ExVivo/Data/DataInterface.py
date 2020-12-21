import sys, os
sys.path.append('..')

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import *
from Analyzer.TransitionProperties import ProcessTransitionProperties
from matplotlib import pyplot as plt


class DataInterfacer():

    def __init__(self):

        self.straintype = 'engineering' # can change to engineering, and lamda
        self.stresstype = 'cauchy' # can change between cauchy and piola
        self.tab_no = []
        self.sampleList = []
        self.sampleName = {}
        self.CheckboxProps = []
        self.props = []
        self.propertyMap = []
        self.propertyPlotArgs = []
        self.master = {}
        self.buttonsdict = []
        self.TransitionPropsDict = []
        self.transitionProps = ProcessTransitionProperties(self.tab_no, eps=0.025)
        self.dataType = {}
        self.ftype = {}



        self.fig = plt.figure(1)

    def setTabNumber(self, tab_no):
        self.tab_no = tab_no
        DataInterfacer.tab_no = self.tab_no

    # set sample list after data parsing in frame1
    def setSampleList(self, samplelist):
        self.sampleList = samplelist
        DataInterfacer.sampleList = self.sampleList


    def setCSVDataParser(self, csvDataParser, specimenHeaders, dimensionHeaders, headersOut, fileform):
        self.csvDataParser = csvDataParser
        DataInterfacer.csvDataParser = self.csvDataParser

        self.specimenHeaders = specimenHeaders
        DataInterfacer.specimenHeaders = self.specimenHeaders

        self.dimensionHeaders = dimensionHeaders
        DataInterfacer.dimensionHeaders = self.dimensionHeaders

        self.headersOut = headersOut
        DataInterfacer.headersOut = self.headersOut

        self.fileform = fileform
        DataInterfacer.fileform = self.fileform

    # called by frame 2 when clicking a sample button. returns sample name to frame 4 to be matched with dimensions
    # and run through getprops and transitionprops
    def setSample(self, samplename):
        self.sampleName = samplename
        DataInterfacer.sampleName = self.sampleName

    # set buttonsdict for changing config of sample button after pressed
    def setButtonsDict(self, dict):
        self.buttonsdict = dict
        DataInterfacer.buttonsdict = self.buttonsdict

    # set values from GETPROPERTIES
    def setProps(self, stress, strain, stiffness, strength):
        self.stress = stress
        DataInterfacer.stress = self.stress

        self.strain = strain
        DataInterfacer.strain = self.strain

        self.stiffness = stiffness
        DataInterfacer.stiffness = self.stiffness

        self.strength = strength
        DataInterfacer.strength = self.strength

    def setBiaxProps(self, stress, strain):
        self.stress = stress
        DataInterfacer.stress = self.stress

        self.strain = strain
        DataInterfacer.strain = self.strain

    def setStressStrainType(self, stresstype, straintype):
        self.stresstype = stresstype
        DataInterfacer.stresstype = self.stresstype

        self.straintype = straintype
        DataInterfacer.straintype = self.straintype

    # set TRANSITIONPROPERTIES
    def setTransitionProps(self, props):
        self.TransitionPropsDict = props
        DataInterfacer.TransitionPropsDict = self.TransitionPropsDict

    def setBiaxTransitionProps11(self, props):
        self.TransitionPropsDict11 = props
        DataInterfacer.TransitionPropsDict11 = self.TransitionPropsDict11

    def setBiaxTransitionProps22(self, props):
        self.TransitionPropsDict22 = props
        DataInterfacer.TransitionPropsDict22 = self.TransitionPropsDict22

    # set master for data plotting functions to to display in frame4
    def setMaster(self,master):
        self.master = master
        DataInterfacer.master = self.master

    # frame 4 called with "GetGraph" function, sets properties to be used by frame 7
    def setCheckboxProps(self, properties):
        self.CheckboxProps = properties
        DataInterfacer.CheckboxProps = self.CheckboxProps

    # frame 7
    def setPropertyMapandPlotArgs(self, PropertyMap, propertyPlotArgs):
        self.propertyMap = PropertyMap
        DataInterfacer.propertyMap = self.propertyMap

        self.propertyPlotArgs = propertyPlotArgs
        DataInterfacer.propertyPlotArgs = self.propertyPlotArgs

    # biax set analysis file type (cauchy vs 1PK vs 1PK)
    def setftypeBiax(self, ftype):
        self.ftype = ftype
        DataInterfacer.ftype = self.ftype

    # determines whether binned or unbinned data for biax
    def setDataTypeBiax(self, dataType):
        self.dataType = dataType
        DataInterfacer.dataType = self.dataType





