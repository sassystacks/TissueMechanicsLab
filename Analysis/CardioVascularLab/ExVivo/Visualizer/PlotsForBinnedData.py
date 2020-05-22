import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
import numpy as np
class BinnedDataPlotter:

    def __init__(self, dataDict):
        self.dataDict = dataDict
        self.elipses = []
        self.fig, self.ax = plt.subplots(figsize=(10,20))

    def _buildPlottingParameters(self, label):

        outputParameters = {}
        if label == 'Raw Data':
            outputParameters = {'label':label, 'alpha':0.5, 'zorder':1,
                                    'marker':'o', 'color':'y','linewidth': 2}
        elif label == 'Raw RDP':
            outputParameters = {'label':label, 'alpha':0.2, 'zorder':3,
                                    'marker':'o', 'color':'m','linewidth': 3}

        elif label == 'Binned Data':
            outputParameters = {'label':label, 'alpha':0.8, 'zorder':2,
                                    'marker':'o', 'color':'r','linewidth': 2}

        elif label == 'Binned RDP':
            outputParameters = {'label':label, 'alpha':0.7, 'zorder':4,
                                    'marker':'h', 'color':'k','linewidth': 3}

        elif label == 'Clusters':
            outputParameters = {'label':label, 'alpha':0.7, 'zorder':4,
                                    'marker':'h', 'color':'g','linewidth': 3}

        else:
            print("The label was not recognized")

        return outputParameters


    def _buildConfidenceElipse(self, x, y, n_std=3.0, facecolor='None', **kwargs):
        """
        Create a plot of the covariance confidence ellipse of `x` and `y`

        """
        if x.size != y.size:
            raise ValueError("x and y must be the same size")

        # Pearson confidence
        cov = np.cov(x, y)
        pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])

        # eigen values
        ell_radius_x = np.sqrt(1 + pearson)
        ell_radius_y = np.sqrt(1 - pearson)
        ellipse = Ellipse((0, 0),
            width=ell_radius_x * 2,
            height=ell_radius_y * 2,
            facecolor=facecolor,
            ec='k',
            **kwargs)

        # Calculating the stdandard deviation of x from
        # the squareroot of the variance and multiplying
        # with the given number of standard deviations.
        scale_x = np.sqrt(cov[0, 0]) * n_std
        mean_x = np.mean(x)

        # calculating the stdandard deviation of y ...
        scale_y = np.sqrt(cov[1, 1]) * n_std
        mean_y = np.mean(y)

        transf = transforms.Affine2D() \
            .scale(scale_x, scale_y) \
            .translate(mean_x, mean_y)

        ellipse.set_transform(transf + self.ax.transData)

        self.elipses.append(ellipse)


    def _addConfidenceElipses(self, key):
        xClusters = self.dataDict[key]['Clusters'][0]
        yClusters = self.dataDict[key]['Clusters'][1]

        numElements = len(xClusters);
        for i in range(numElements):
            self._buildConfidenceElipse(xClusters[i],yClusters[i])

    def _plot(self):

        import random
        # {'Raw Data':rawDataPoints,'Raw RDP':rawRDP,
        # 'Binned Data':binnedData,'Binned RDP':binnedRDP}

        colors = ['r','b','y','g']
        colorCount = 0

        for data in self.dataDict:
            for key in self.dataDict[data]:

                params = self._buildPlottingParameters(key)

                if 'RDP' in key:
                    self.ax.plot(self.dataDict[data][key][...,0],self.dataDict[data][key][...,1],
                                label=params['label'],
                                alpha=params['alpha'], marker=params['marker'],
                                color=params['color'],zorder=params['zorder'],
                                linewidth=params['linewidth'])

                elif 'Clusters' in key:
                    self._addConfidenceElipses(data)
                    # print('clusters')
                    for e in self.elipses:
                        self.ax.add_patch(e)
                else:
                    # Change colors from params['color']
                    self.ax.scatter(self.dataDict[data][key][...,0],self.dataDict[data][key][...,1],
                                label=params['label'],
                                alpha=params['alpha'], marker=params['marker'],
                                color=colors[colorCount],zorder=params['zorder'],
                                linewidth=params['linewidth'])
                    colorCount += 1

        self.ax.legend()
        plt.show()
