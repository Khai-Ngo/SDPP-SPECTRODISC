import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize 
from scipy.interpolate import interpn
def readExport (filepath, max_rows = None):
    x, y = [], []
    with open(filepath, "r") as f:
        lines = f.readlines()[:max_rows]
    for line in lines:
        x.append(float(line.split()[0]))
        y.append(float(line.split()[1]))
    return np.array(x), np.array(y)
def dataTruncator (x, y, xlow = -np.inf, xhigh = np.inf, ylow = -np.inf, yhigh = np.inf, numPoint = np.inf):
    xret = []
    yret = []
    count = 0
    assert len(x) == len(y), "The arrays are not of the same length"
    for xelem, yelem in zip(x, y):
        if xlow<=xelem<xhigh and ylow<=yelem<yhigh:
            xret.append(xelem)
            yret.append(yelem)
            count+=1
        if count > numPoint:
            break
    xret = np.array(xret)
    yret = np.array(yret)
    return xret, yret
def buildHist(arr, filename, minVal, maxVal, noOfBins, auto = False, plot = False, save = True):
    hist, bin_edges = np.histogram(arr, bins = noOfBins, range = (minVal, maxVal)) if not auto else np.histogram(arr, bins = 'auto')
    if save:
        with open(filename,"w") as f:
            f.write('Value\tCounts\n')
            for e, val in zip(bin_edges[:-1], hist):
                f.write('%s\t%s\n'%(e, val))
    if plot:
        plt.plot(bin_edges[:-1], hist)
        plt.show()
def density_scatter( x , y, xlow, xhigh, ylow, yhigh, ax = None, sort = True, bins = 20, xlabel = 'x', ylabel = 'y', fontsize = 18)   :
    """
    Scatter plot colored by 2d histogram
    """
    if ax is None :
        fig , ax = plt.subplots(figsize=(8, 6))
    data , x_e, y_e = np.histogram2d( x, y, bins = bins, density = True )
    z = interpn( ( 0.5*(x_e[1:] + x_e[:-1]) , 0.5*(y_e[1:]+y_e[:-1]) ) , data , np.vstack([x,y]).T , method = "splinef2d", bounds_error = False)
    #To be sure to plot all data
    z[np.where(np.isnan(z))] = 0.0
    # Sort the points by density, so that the densest points are plotted last
    if sort :
        idx = z.argsort()
        x, y, z = x[idx], y[idx], z[idx]
    # configure plot aesthetics
    plt.xlim(xlow, xhigh)
    plt.ylim(ylow, yhigh)
    plt.rcParams['font.size'] = fontsize
    for label in (ax.get_xticklabels()+ax.get_yticklabels()):
        label.set_fontsize(fontsize)
    # actual plotting
    ax.scatter( x, y, c=z, s=0.05,cmap = 'jet')
    norm = Normalize(vmin = np.min(z), vmax = np.max(z))
    cbar = fig.colorbar(cm.ScalarMappable(norm = norm, cmap = 'jet'), ax=ax, spacing = 'proportional')
    ax.set_xlabel(xlabel, fontsize = fontsize)
    ax.set_ylabel(ylabel, fontsize = fontsize)
    # configure grid and minor ticks
    ax.grid(visible = True)
    ax.yaxis.get_ticklocs(minor=True)
    ax.minorticks_on()
    plt.show()
    return ax
