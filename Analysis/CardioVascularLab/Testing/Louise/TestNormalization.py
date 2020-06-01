from TestingTemplate import Test

def _normalizeData(self, xdata, ydata):
    '''
    This normalize 2 numpy arrays and normalize them
    Some ideas: numpy.linalg.normalize(x) ... look up
                x - min / (max-min)

    returns:
        numpy arrays
    '''
    # not sure how to reference the correct arrays here
    xdata = DataStructure._ProcessedData[0, :]
    ydata = DataStructure._ProcessedData[:, 0]

    x_norm = xdata / np.linalg.norm(xdata)
    y_norm = ydata / np.linalg.norm(ydata)

    # Normalize them
    normArray1 = []
    normArray2 = []

    return x_norm, y_norm
