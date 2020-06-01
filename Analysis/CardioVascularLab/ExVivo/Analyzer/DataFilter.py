import numpy as np

class ExVivoDataUtils:

    def __init__(self):
        pass

    def _getBinIndexOfNumpyArrays(self, data, binsize=1):

        bins=np.arange(min(data), max(data) + binsize/2, binsize)
        inds = np.digitize(data, bins, right=True)

        return inds, bins

    def _binDataFromIndices(self, data, indices, bins):

        keys = np.unique(indices)
        keys = np.sort(keys)
        binDict = {k:[] for k in keys}
        for i in range(data.size):
            binDict[indices[i]].append(data[i])

        outputArray = [np.mean(binDict[key]) for key in binDict]

        return np.array(outputArray), bins[keys-1]

    def _truncateDataAbove(self, dataDict, dataKey, threshold=0):

        for key, v in dataDict.items():
            for i in range(2):
                indxs = np.where(dataDict[key][dataKey][:,i] > threshold)[0]
                dataDict[key][dataKey] = dataDict[key][dataKey][indxs]

        return dataDict

    def _normalizeData(self, xdata, ydata):
        '''
        This normalize 2 numpy arrays and normalize them
        Some ideas: numpy.linalg.normalize(x) ... look up
                    x - min / (max-min)

        returns:
            numpy arrays
        '''
        # not sure how to reference the correct arrays here
        xdata = DataStructure._ProcessedData[0,:]
        ydata = DataStructure._ProcessedData[:,0]

        x_norm = [xdata/np.linalg.norm(xdata)]
        y_norm = [ydata/np.linalg.norm(ydata)]

        # Normalize them
        normArray1 = []
        normArray2 = []

        return x_norm, y_norm
