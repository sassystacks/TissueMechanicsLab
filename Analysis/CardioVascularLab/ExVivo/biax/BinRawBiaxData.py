import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class ReadParams:

    def __init__(self):
        self.DotFileHeaders = [ 'FrameTime', 'X0', 'Y0', 'X1', 'Y1', 'X2', 'Y2',
                            'X3', 'Y3', 'X4', 'Y4', 'E11', 'E22', 'E12',
                            'PS1', 'SA1', 'PS2', 'SA2']
        self.Directions = ['X0', 'Y0', 'X1', 'Y1', 'X2', 'Y2',
                            'X3', 'Y3', 'X4', 'Y4']
        self.HeadersToPop = ['E11', 'E22', 'E12', 'PS1', 'SA1', 'PS2', 'SA2']

def _plotXYPairs(df,params):


    fig, axes = plt.subplots(nrows=int(len(params)/2), ncols=2)
    fig.subplots_adjust(hspace=0.5)
    fig.suptitle('Each point vs time')
    # ax = axes.flatten()
    time = df['FrameTime']


    for ax, direction in zip(axes.flatten(),df[params]):

        ax.scatter(time,df[direction])
        ax.set(title=direction.upper(), xlabel='time')

    plt.show()


def _BuildFileList(f):

    if os.path.isdir(f): # if f is a directory
        topDir = f
        t_fileList = os.listdir(f)
        fileList = [os.path.join(topDir,file) for file in t_fileList]

    elif os.path.isfile(f): # if f is just a file
        fileList = [f]

    else:
        fileList  = [] # if f isn't either a file or a directory
        print("This isn't a file or a directory")

    return fileList

def _ConvertTimeToFloatStartingZero(df):
    # Convert the time to time delta type
    df['FrameTime'] = pd.to_timedelta(df['FrameTime'])
    df = df.assign(FrameTime = [x.seconds * 1.0 for x in df['FrameTime']] )
    df['FrameTime'] = df['FrameTime'] - df['FrameTime'][0]

    return df

def _main(f):

    files = _BuildFileList(f)

    try:
        # Read the csv
        df  = pd.read_csv(f,skiprows=1,header=None)
        # Set the column names from
        df.columns = ReadParams().DotFileHeaders
        # Remove all the columns that aren't position or time
        [df.pop(x) for x in ReadParams().HeadersToPop]

        df = _ConvertTimeToFloatStartingZero(df)

        # _plotXYPairs(df,['Y0','Y1','Y2','Y3'])
        _plotXYPairs(df,['X0','X1','X2','X3'])


    except Exception as e:
        print(e)



if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-fo','--folder',help="Enter an entire folder to have the data binned")
    group.add_argument('-f','--file',help="Enter a single file to have the data binned")

    args = parser.parse_args()
    if args.folder:
        f = args.folder
    else:
        f = args.file

    _main(f)
    #
    # df = pd.read_csv(f)
    #
    # df = df[['Sample','Specimen','Width','Thickness']]
    # df = df.iloc[::2,:]
    #
    # df.to_csv("AAAMissingDimensions_Jan2018.csv",index=False)
