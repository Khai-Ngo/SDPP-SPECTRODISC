import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize 
from scipy.interpolate import interpn
import sys
def readExport (filepath, max_rows = None):
    x, y = np.genfromtxt(filepath, dtype = (float, float), delimiter = '\t', missing_values = 'nan', usecols = (0,1), max_rows = max_rows, unpack = True)
    return x, y
def dataTruncator (x, y, xlow = 0, xhigh = np.inf, ylow = 0, yhigh = np.inf, numPoint = np.inf):
    xret = []
    yret = []
    count = 0
    assert len(x) == len(y), "The arrays are not of the same length"
    for i in range (len(x)):
        if x[i] < xhigh and x[i] >= xlow and y[i] < yhigh and y[i] >= ylow:
            xret.append(x[i])
            yret.append(y[i])
            count+=1
        if count > numPoint:
            break
    xret = np.array(xret)
    yret = np.array(yret)
    return xret, yret
def buildHist(arr, filename, minVal, maxVal, noOfBins, auto = False, plot = False, save = True):
    if auto:
        PAS, bin_edges = np.histogram(arr, bins = 'auto') # auto-binning is used
    else:
        PAS, bin_edges = np.histogram(arr, bins = noOfBins, range = (minVal, maxVal))
    if save:
        f = open(filename,"w")
        f.write('Value\tCounts\n')
        for i in range(len(PAS)):
            f.write('%s\t%s\n'%(bin_edges[i], PAS[i]))
        f.close()
    if plot:
        plt.plot(bin_edges[:len(PAS)], PAS)
        plt.show()
def density_scatter( x , y, ax = None, xlow = 0, xhigh = 16000, ylow = 1, yhigh = 1.5, sort = True, bins = 20, xlabel = 'x', ylabel = 'y', limFlag = True)   :
    """
    Scatter plot colored by 2d histogram
    """
    fontsize = 18
    if ax is None :
        fig , ax = plt.subplots()
    data , x_e, y_e = np.histogram2d( x, y, bins = bins, density = True )
    z = interpn( ( 0.5*(x_e[1:] + x_e[:-1]) , 0.5*(y_e[1:]+y_e[:-1]) ) , data , np.vstack([x,y]).T , method = "splinef2d", bounds_error = False)

    #To be sure to plot all data
    z[np.where(np.isnan(z))] = 0.0

    # Sort the points by density, so that the densest points are plotted last
    if sort :
        idx = z.argsort()
        x, y, z = x[idx], y[idx], z[idx]
    if limFlag:
        plt.ylim(ylow, yhigh)
        plt.xlim(xlow, xhigh)
    plt.rcParams['font.size'] = fontsize
    for label in (ax.get_xticklabels()+ax.get_yticklabels()):
        label.set_fontsize(fontsize)
    ax.scatter( x, y, c=z, s=0.05,cmap = 'rainbow')
    norm = Normalize(vmin = np.min(z), vmax = np.max(z))
    cbar = fig.colorbar(cm.ScalarMappable(norm = norm), ax=ax)
    cbar.ax.set_ylabel('Density')
    ax.set_xlabel(xlabel, fontsize = fontsize)
    ax.set_ylabel(ylabel, fontsize = fontsize)
    # configure grid and minor ticks
    ax.grid(visible = True)
    ax.yaxis.get_ticklocs(minor=True)
    ax.minorticks_on()
    plt.show()
    return ax
