import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize 
from scipy.interpolate import interpn
import sys

def twoDdataSelector (x, y, xlow = 0, xhigh = np.inf, ylow = 0, yhigh = np.inf, numPoint = np.inf):
    xret = []
    yret = []
    count = 0
    assert len(x) == len(y), "The arrays are not of the same length"
    for i in range (len(x)):
        if x[i] <= xhigh and x[i] >= xlow and y[i] <= yhigh and y[i] >= ylow:
            xret.append(x[i])
            yret.append(y[i])
            count+=1
        if count > numPoint:
            break
    xret = np.array(xret)
    yret = np.array(yret)
    return xret, yret
def density_scatter( x , y, ax = None, xlow = 0, xhigh = 16000, ylow = 1, yhigh = 1.5, sort = True, bins = 20, xlabel = 'x', ylabel = 'y', limFlag = True, **kwargs )   :
    """
    Scatter plot colored by 2d histogram
    """
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
    ax.scatter( x, y, c=z, s=0.05,cmap = 'rainbow', **kwargs )
    norm = Normalize(vmin = np.min(z), vmax = np.max(z))
    cbar = fig.colorbar(cm.ScalarMappable(norm = norm), ax=ax)
    cbar.ax.set_ylabel('Density')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()
    return ax
def readExport (filepath):
    with open(filepath) as f:
        x = []
        y= []
        lines = f.readlines()[1:]
        for line in lines:
            tmp = line.split()[0]
            if tmp != 'nan':
                x.append(float(tmp))
                y.append(float(line.split()[1]))
        x = np.array(x)
        y = np.array(y)
        return x, y
def plotParamsRead():
    with open("plotParams.par") as f:
        lines = [line.strip("\n") for line in f.readlines() if not line.startswith('#')]
        inputPath = lines[0].split("=")[1].strip(" ")
        minPH = float(lines[2].split("=")[1].strip(" "))
        maxPH = float(lines[3].split("=")[1].strip(" "))
        minr = float(lines[4].split("=")[1].strip(" "))
        maxr = float(lines[5].split("=")[1].strip(" "))
        return inputPath, minPH, maxPH, minr, maxr
if __name__ == '__main__':
    inputPath, minPH, maxPH, minr, maxr = plotParamsRead()
    x, y = readExport(inputPath)
    xprime, yprime = twoDdataSelector (x, y, xlow = minPH, xhigh = maxPH, ylow = minr, yhigh = maxr)
    density_scatter(xprime, yprime, xlow = minPH, xhigh = maxPH, ylow = minr, yhigh = maxr, bins = [1000,1000], xlabel = 'Pulse area', ylabel = 'PSD')
    
