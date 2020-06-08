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

    def _findMax(self, data, index):

        currVal = data[index]
        nextVal = data[index + 1]

        while currVal < nextVal:
            index += 1

            currVal = data[index]
            nextVal = data[index + 1]

            maxInd = index - 1

        return maxInd

    # xdata = DataStructure._ProcessedData[0,:]
    # ydata = DataStructure._ProcessedData[:,0]

    def _normalizeData(self, ydata, xdata):
        '''
        This intakes 2 numpy arrays and normalizes them.
        returns:
            numpy arrays
        '''

        maxInd = _findMax(ydata, 10)

        xdata = xdata[:maxInd]
        ydata = ydata[:maxInd]

        x_norm = (xdata - np.min(xdata)) / (np.max(xdata) - np.min(xdata))
        y_norm = (ydata - np.min(ydata)) / (np.max(ydata) - np.min(ydata))

        return y_norm, x_norm


