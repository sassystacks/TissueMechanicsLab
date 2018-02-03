#!/usr/bin/env python

'''
MDSC 689.03

Advanced Medical Image Processing

Assignment #01 - Load Image Data & Display Imageds
Richard_Beddoes
January 19th, 2018

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This program take a directory input and additional arguments
listed below. It opens the the file and displays the central image in
the stack. To navigate through the images use the scrollwheel on the mouse.

Example command line of how to run script:
    python assignment1_Richard.py --additional arguments

For a list of all commands type:
    python assignment1_Richard.py --help to obtain the output:

optional arguments:
  -h, --help            show this help message and exit
  -w [WINDOW], --window [WINDOW]
                        This changes the grey scale value (default is 1000)
  -l [LEVEL], --level [LEVEL]
                        This changes the window level value (default is 0)
  -z [ZSLICE], --zslice [ZSLICE]
                        This changes the initial slice value (default is 0)
  -wd [WIDTH], --width [WIDTH]
                        This changes the width of display (default is 512)
  -ht [HEIGHT], --height [HEIGHT]
                        This changes the height of display (default is 512)
  -sj [SLICEJUMP], --slicejump [SLICEJUMP]
                        This changes the number of slices to scroll (default
                        is 1)
  -f [FOLDER], --folder [FOLDER]
                        This changes the folder to look in (default is None)
  -d [DIRECTORY], --directory [DIRECTORY]
                        This changes the directory to look in (default is
                        current directory)
'''

import vtk
import os

# Sub-Class to be used for defining controls in the render window
class scrollControl:

    def __init__(self, parent=None):
        #Bind 2 events to methods in this class
        self.AddObserver('MouseWheelForwardEvent', self.moveUPfunc)
        self.AddObserver('MouseWheelBackwardEvent', self.moveDOWNfunc)

    def moveUPfunc(self, *args):
        #This function moves up in the slices increasing the Number

        #increase the slice number by a user defined number or default number 1
        self.zSlice = self.zSlice + self.sliceJump

        #change the image to the new slice Number
        self.updateWindow()

    def moveDOWNfunc(self, *args):

        #increase the slice number by a user defined number or default number 1
        self.zSlice = self.zSlice - self.sliceJump

        #change the image to the new slice Number
        self.updateWindow()

    def updateWindow(self, *args):
        #create mapper
        self.actor.SetMapper(self.mapFunc())

        # self.interactor.SetRenderWindow(self.renWin)
        self.ren.AddActor(self.actor)
        self.renWin.AddRenderer(self.ren)
        self.renWin.Render()

class loadAndView:

    def __init__(self,**kwargs):

        #Set parameters for Script
        #window
        self.win = kwargs['window']
        #level for DICOM
        self.lev = kwargs['level']

        #slice Number
        self.zSlice = kwargs['zslice']
        #width
        self.width = kwargs['width']
        #height
        self.height = kwargs['height']
        #data set to load
        self.sliceJump = kwargs['slicejump']

        #directory to look in for the data set
        try:
            self.directory = os.path.join(kwargs['directory'],kwargs['folder'])

        except:
            self.directory = os.path.join(kwargs['directory'])
        #Read first file in the directory and Determine if it is a DICOM type or NIFTI type folder
        chkFtype = os.listdir(self.directory)[0]

        #if it is a DICOM folder set the filetype and define an actor
        if chkFtype.endswith(".dcm"):
            self.ftype = 'DCM'
            self.actor = self.readDICOM()

        #if it is a DICOM folder set the filetype and define an actor
        elif chkFtype.endswith(".nii"):
            self.ftype = 'NII'
            self.actor = self.readNIFTI(chkFtype)

        else:
            print("The folder specified won't work with this application")
            exit()

    def readDICOM(self,*args):

        #create reader
        self.reader = vtk.vtkDICOMImageReader()
        self.reader.SetDirectoryName(self.directory)
        self.reader.Update()

        #create mapper
        mapper = self.mapFunc()

        # Create actor and set the mapper and the texture
        actor = vtk.vtkActor2D()
        actor.SetMapper(mapper)

        return actor

    def readNIFTI(self,*args):

        #create reader
        self.reader = vtk.vtkNIFTIImageReader()
        self.reader.SetFileName(os.path.join(self.directory,args[0]))
        self.reader.Update()

        #create mapper
        mapper = self.mapFunc()

        #create slice1
        slice1 = vtk.vtkImageSlice()
        slice1.SetMapper(mapper)
        slice1.GetProperty().SetColorWindow(self.win)
        slice1.GetProperty().SetColorLevel(self.lev)

        return slice1

    def mapFunc(self, *args):

        #Check filetype to see if is DICOM or NIFTI
        if self.ftype is 'DCM':
            t_map = vtk.vtkImageMapper()
            t_map.SetZSlice(int(self.zSlice))
            t_map.SetColorWindow(self.win)
            t_map.SetColorLevel(self.lev)
            t_map.SetInputConnection(self.reader.GetOutputPort())


        elif self.ftype is 'NII':

            #create mapper
            t_map = vtk.vtkImageSliceMapper()
            t_map.SetSliceNumber(self.zSlice)
            t_map.SetInputConnection(self.reader.GetOutputPort())

        return t_map

    def renderImage(self,*args):

        # Create a render window
        self.ren = vtk.vtkRenderer()
        self.renWin = vtk.vtkRenderWindow()
        self.renWin.AddRenderer(self.ren)
        self.renWin.SetSize(self.width,self.height)
        iren = vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(self.renWin)

        #Check filetype to see if is DICOM or NIFTI
        if self.ftype is 'DCM':
            #if DICOM add actor
            self.ren.AddActor(self.actor)

        elif self.ftype is 'NII':
            #if NIFTI add view Prop
            self.ren.AddViewProp(self.actor)

        return iren

    def interactorImage(self,*args):

        interactor = self.renderImage()

        interactor.Initialize()
        interactor.SetInteractorStyle(None)
        interactor.AddObserver('MouseWheelForwardEvent', self.moveUPfunc)
        interactor.AddObserver('MouseWheelBackwardEvent', self.moveDOWNfunc)

        self.renWin.Render()
        interactor.Start()

    def moveUPfunc(self, *args):

        self.zSlice = self.zSlice + self.sliceJump
        self.updateWindow()

    def moveDOWNfunc(self, *args):

        self.zSlice = self.zSlice - self.sliceJump
        self.updateWindow()

    def updateWindow(self, *args):
        #create mapper
        self.actor.SetMapper(self.mapFunc())

        # self.interactor.SetRenderWindow(self.renWin)
        self.ren.AddActor(self.actor)
        self.renWin.AddRenderer(self.ren)
        self.renWin.Render()

if __name__ == '__main__':
    import argparse
    cwd = os.getcwd()
    parser = argparse.ArgumentParser()
    parser.add_argument('-w','--window', nargs='?', default=1000, type=int, help='This changes the grey scale value (default is 1000)')
    parser.add_argument('-l','--level', nargs='?', default=0, type=int, help='This changes the window level value (default is 0)')
    parser.add_argument('-z','--zslice', nargs='?', default=0, type=int, help='This changes the initial slice value (default is 0)')
    parser.add_argument('-wd','--width', nargs='?', default=512, type=int, help='This changes the width of display (default is 512)')
    parser.add_argument('-ht','--height', nargs='?', default=512, type=int, help='This changes the height of display (default is 512)')
    parser.add_argument('-sj','--slicejump', nargs='?', default=1, type=int, help='This changes the number of slices to scroll (default is 1)')
    parser.add_argument('-f','--folder', nargs='?', help='This changes the folder to look in (default is None)')
    parser.add_argument('-d','--directory', nargs='?', default=cwd, help='This changes the directory to look in (default is current directory)')
    args = parser.parse_args()
    args_dict = vars(args)

    #run main class and run the renderer to visualize image
    loadAndView(**args_dict).interactorImage()
