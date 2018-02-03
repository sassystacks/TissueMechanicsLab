#! /usr/bin/python
import os
import psycopg2
import csv
import pandas as pd;

class uniaxAnalysis:

    def __init__(self,**kwargs):

        #pass info as dict to function from App
        self.importFolder = kwargs["importFolder"]
        self.stepforward = kwargs["stepforward"]
        self.stepback = kwargs["stepback"]
        self.rsquared = kwargs["rsquared"]

        # #connect to database
        # try:
        #     self.dbConn = psycopg2.connect(kwargs["connectString"])
        # except:
        #     print "can't connect to the database"

        #run performAnalysis() to push dict to database
        spec_dict = self.extractCSV()
        self.performAnalysis(spec_dict)

        # #close database connection
        # self.dbConn.close()

    def extractCSV(self,*args):

        # #define cursor
        # self.dbConn.crsr()

        #look in folder/database for csv to pull data
        items = os.listdir(self.importFolder)


        filelist = []
        #Takes importFolder and makes list of all data for each sample parsing extension from filename and just extracting force and displacement
        for name in items:
            if name.endswith(".CSV"):
                #Join importFolderwith filelist
                fullName = os.path.join(self.importFolder,name)
                headers = ['time','displacement','force']
                df = pd.read_csv(fullName,sep="\s+",names=headers,header=None)
                filelist.append([name[:-4],df[['displacement','force']]])



        #pull force and displacement data as list of list

        #saved_column = df.column_name
        print(filelist)

        #zip lists of force, displacement, and specimen_id
        keys = ['specimen_id','force','displacement']


        #pass connection and specimen_id list to extractDimension()

        #parse list of dimensions to dict including force, displacement and specimen_id

        #calculate strain

        #calculate stress

        #close cursor

        #return dict of specimen_id, stress and strain

    def extractDimension(self,*args):
        pass
        #define cursor

        #build query statement to get dimensional data

        #query database based on csv filenames to get dimensions

        #close cursor

        #return list of dimensions

    def calc_uts_utstr(self, *args):
        pass
        #for loop to iterate forward by stepforward value find a point
        #where second is less than first

        #find strain at that point

        #return the index of uts

    def calc_slopeAt15(self, *args):
        pass
        #take points from 10% to 20% strain

        #fit curve to points

        #take derivative of curve

        #get value of derivative at 15%

        #return value of derivative at 15%

    def fit_neohookean(self, *args):
        pass
        #take points from 5% to 15% strain

        #fit neohookean model sigma = 2C0(lambda^2 - 1/lambda)

        #get r-squared value of curve fit to data

        #return r-squared value and C0

    def performAnalysis(self, *args):
        pass
        #run extractCSV create variable to store dict

        #run loop - inside loop run calc_slopeAt15, calc_uts_utstr, fit_neohookean
        #build dict for export

        #define a query statement to insert data to db

        #define cursor

        #push dict containing project,specimen_id, uts, utstr, 15% strain,
        #neohookean, r-squared to database

        #close cursor

if __name__ == '__main__':
    uniaxAnalysis(importFolder='rawCSVfail',stepforward=1,stepback=1,rsquared=.99)
