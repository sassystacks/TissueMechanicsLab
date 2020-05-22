import numpy as np

class DataClusterAnalysis:

    def __init__(self):

        pass

    def _getNumberOfPointsInCluster(self, data,clusterWidth):
        '''
        take the first element in the data set and get the next n data points that
        are within the cluster. returns n
        '''
        count = 1;
        # print(data[count+1] - data[count] < clusterWidth)

        while count < len(data)  and data[count] - data[count -1] < clusterWidth[0]\
                and data[count] - data[0] < clusterWidth[1]:
            count += 1
        return count

    def _clusterByData(self, data1,data2,clusterWidth):

        # data1Cluster = []
        # data2Cluster = []

        dataClusters = [[],[]]
        while (len(data1) > 0):

            numberOfPoints = self._getNumberOfPointsInCluster(data1, clusterWidth)

            dataClusters[0].append(data1[:numberOfPoints])
            dataClusters[1].append(data2[:numberOfPoints])


            # data1Cluster.append(np.mean(data1[:numberOfPoints]))
            # data2Cluster.append(np.mean(data2[:numberOfPoints]))

            data1 = np.delete(data1, np.arange(numberOfPoints))
            data2 = np.delete(data2, np.arange(numberOfPoints))
        return dataClusters


    def _clusterDataStat(self, dataClusters, operator):
        '''
        This is a little convoluted, but it runs through the data and takes the mean
        '''
        dataSize = len(dataClusters[0])
        clusterStat = [np.zeros(dataSize), np.zeros(dataSize)]

        for i in range(dataSize):
            clusterStat[0][i] = operator(dataClusters[0][i])
            clusterStat[1][i] = operator(dataClusters[1][i])

        return clusterStat
