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
# write PAS to file
def buildHist(arr, filename, minVal, maxVal, noOfBins, auto = False, plot = False, save = True):
    print("Building histogram...")
    if auto:
        PAS, bin_edges = np.histogram(arr, bins = 'auto') # auto-binning is used
    else:
        PAS, bin_edges = np.histogram(arr, bins = noOfBins, range = (minVal, maxVal))
    if save:
        f = open ("{}.txt".format(filename), 'w')
        f.write('Value\tCounts\n')
        for i in range(len(PAS)):
            f.write('%s\t%s\n'%(bin_edges[i], PAS[i]))
        f.close()
        print("Wrote histogram succesffully\n")
    if plot:
        plt.plot(bin_edges[:len(PAS)], PAS)
        plt.show()
def readExport (filepath):
    with open(filepath) as f:
        x = []
        y= []
        lines = f.readlines()
        for line in lines:
            tmp = line.split()[0]
            if tmp != 'nan':
                x.append(float(tmp))
                y.append(float(line.split()[1]))
        x = np.array(x)
        y = np.array(y)
        return x, y
def convertBool (string):
    if string == 'TRUE' or string == 'T' or string == 'true' or string == 'True' or string == '1':
        return True
    else: return False
def plotParamsRead():
    with open("plotParams.par") as f:
        lines = [line.strip("\n") for line in f.readlines() if not line.startswith('#')]
    inputPath = lines[0].split("=")[1].strip(" ")
    outputPath = lines[1].split("=")[1].strip(" ")
    minPH = float(lines[2].split("=")[1].strip(" "))
    maxPH = float(lines[3].split("=")[1].strip(" "))
    minr = float(lines[4].split("=")[1].strip(" "))
    autoflag = lines[6].split("=")[1].strip(" ")
    binWidth = float(lines[7].split("=")[1].strip(" "))
    return inputPath, outputPath, minPH, maxPH, minr, autoflag, binWidth  
if __name__ == '__main__':
    inputPath, outputPath, minPH, maxPH, minr, autoflag, binWidth  = plotParamsRead()
    x, y = readExport(inputPath)
    autoflag = convertBool(autoflag)
    #LO = (0.627*x - 41)/1000
    xprime, yprime = twoDdataSelector (x, y, xlow = minPH, xhigh = maxPH, ylow = minr)
    if not autoflag:
        noOfBins = int(maxPH/binWidth)
        buildHist(xprime, outputPath, minVal = minPH, maxVal = maxPH, noOfBins = noOfBins, auto = False, plot = True, save = True)
    else:
        buildHist(xprime, outputPath, minVal = 0, maxVal = 0, noOfBins = 0, auto = True, plot = True, save = True)


