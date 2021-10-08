import numpy as np
import struct
import scipy.integrate
import matplotlib.pyplot as plt

# specify input and output directories here
inputDir = r'E:\Scintillator analysis code\test-input'
outputDirectory = r'E:\Scintillator analysis code\test-output'
filename = "scint1_wave1_20"

def trapezoidal (pulse):
    l = len(pulse)
    L = 2
    G = 7
    pulse_Ftrap = []
    for i in range(l - G - 2*L):
        Vav1 = 0
        Vav2 = 0
        for j in range(i, i+L):
            Vav1 += pulse[j]
        for k in range(i+L+G, i+2*L+G):
            Vav2 += pulse[k]
        Vav1/=L
        Vav2/=L
        Vout = Vav2-Vav1
        pulse_Ftrap.append(Vout)
    return pulse_Ftrap
def pile_up_flag (pulse):
    ret = False
    step = 5
    pulse_Ftrap = trapezoidal(pulse)
    length = len(pulse_Ftrap)
    maxPulse = max(pulse_Ftrap)
    trigger = maxPulse*0.20
    count = 0
    i = 0
    flag = 1
    while i < length:
        if flag == 1:
            if pulse_Ftrap[i] > trigger:
                count +=1
                flag = 0
        if flag == 0:
            if pulse_Ftrap[i] < 0:
                count+=1 
                flag = 1
        if count > 2:
            ret = True
            break
        i+=step
    return ret
def writeWave (pulseArray, pulsenum, filename):
    len(pulseArray)
    fileDestination = outputDirectory + "\pulse" + str(pulsenum) + filename + ".txt"
    f1 = open(fileDestination, 'w')
    for i in range(length):
        f1.write('%s\t%s\n'%(i, pulseArray[i]))
    f1.close()
    print("Write successfully to " + fileDestination)
def plotWave (pulse):
    length = len(pulse)
    xdata = np.arange(0, length, 1)
    plt.plot(xdata, pulse)
    plt.show()
def normalise(pulse):
    maxPulse = max(pulse)
    ret = np.array(pulse)
    for i in range(len(ret)):
        ret[i] /= maxPulse
    return ret
def pulseAreaCLYC (pulse, W1 = 80, W2 = 500, delay = 20, allGate = 1800):
    length = len(pulse)
    threshold = 5.0 #mV
    startIndex = 0
    # detect when threshold is first crossed in signal pulse
    for i in range(length):
         if pulse[i] > threshold:
             startIndex = i
             break
    startIndex -= 8
    # make sure that integration bounds are sensible
    if startIndex < 0:
        startIndex = 0
    assert startIndex+allGate+1 <= length, "integration out of bounds!"
    shortInte = scipy.integrate.trapz (pulse[startIndex:startIndex+W1+1], None, dx = 1.0) 
    longInte = scipy.integrate.trapz (pulse[startIndex+W1+delay:startIndex+W1+delay+W2+1], None, dx = 1.0)
    allInte = scipy.integrate.trapz (pulse[startIndex:startIndex+allGate+1], None, dx = 1.0)
    return shortInte, longInte, allInte
def pulseAreaEJ276 (pulseArray, shortGate = 60, longGate = 220):
    length = len(pulseArray)
    threshold = 5.0 #mV
    startIndex = 0
    for i in range(length):
         if pulseArray[i] > threshold:
             startIndex = i
             break
    startIndex -= 5 
    if startIndex < 0:
        startIndex = 0
    stopShort = startIndex + shortGate
    stopLong = startIndex + longGate
    if stopShort > (length - 1):
        stopShort = length - 1
    if stopLong > (length - 1):
        stopLong = length - 1
    shortInte = scipy.integrate.trapz (pulseArray[startIndex:stopShort+1], None, dx = 1.0) 
    longInte = scipy.integrate.trapz (pulseArray[startIndex:stopLong+1], None, dx = 1.0)
    return shortInte, longInte
def buildHist(arr, filename, minVal, maxVal, noOfBins, auto = False, plot = False, save = True):
    print("Building histogram...")
    if auto:
        PAS, bin_edges = np.histogram(arr, bins = 'auto') # auto-binning is used
    else:
        PAS, bin_edges = np.histogram(arr, bins = noOfBins, range = (minVal, maxVal))
    if save:
        fileDestination = outputDirectory + "\\"+filename+ ".txt"
        f = open (fileDestination, 'w')
        f.write('Value\tCounts\n')
        for i in range(len(PAS)):
            f.write('%s\t%s\n'%(bin_edges[i], PAS[i]))
        f.close()
        print("Wrote histogram succesffully to " + fileDestination+"\n")
    if plot:
        plt.plot(bin_edges[:len(PAS)], PAS)
        plt.show()
def buildTimeTrace(countArray, cycle, filename):
    print("Exporting time trace of " + filename + "...\n")
    fileDestination = outputDirectory +"\\"+ filename + ".txt"
    f = open (fileDestination, 'w')
    f.write('Time(sec)\tCounts\n')
    for i in range(len(countArray)):
        f.write('%d\t%d\n'%(i*cycle, countArray[i]))
    f.close()
def save(x, y, filename, xlabel = "x", ylabel = "y"):
    filepath = outputDirectory+"\\"+filename+".txt"
    f = open(filepath, "w")
    f.write("{}\t{}\n".format(xlabel, ylabel))
    assert len(x) == len(y), "To write to txt, need same length array!"
    for i in range(len(x)):
        f.write("{}\t{}\n".format(x[i], y[i]))
    f.close()
    print("Data saved to {} successfully".format(filepath))
# main
if __name__ == '__main__':
    # initialise variables
    length = 0 # pulse length
    currentTimeStamp = 0.0
    time_elasped_microsec = 0.0
    Reset = 0.0
    FirstTimeC = 0.0
    time_elasped_sec = 0.0
    fi = 0 # first pulse flag
    pulsenum = 0

    currentCycle = 1.0 # in seconds
    cycle = 1.0 # in seconds
    pileUpCount = 0
    count = 0
    threshold = 5.0# in mV

    countArray = []
    ratioArray = []
    areaArray= []
    #reading input file
    filepath = inputDir + "\\"+filename + ".dat"
    with open(filepath, 'rb') as file:
        while True:        
            # read header for pulse length and time stamp
            buffer = file.read(24)
            if not buffer: break # eof exit
            length, idk2, idk3, idk4, idk5, this_time_stamp = struct.unpack('=iiiiiI', buffer)
            length = int((length-24)/2)
            currentTimeStamp = float(this_time_stamp) * 0.008 # in microseconds
            # check for reset
            if fi == 0:
                FirstTimeC = currentTimeStamp
                fi = 1
            currentTimeStamp = currentTimeStamp + Reset - FirstTimeC
            if currentTimeStamp < time_elasped_microsec:
                Reset = Reset + 17179869.19
                time_elasped_microsec = currentTimeStamp + 17179869.19
            else: time_elasped_microsec = currentTimeStamp
            time_elasped_sec = time_elasped_microsec / 1000000.0 # in seconds
            # read and analyse pulse
            shortbuffer = file.read(2 * length)
            pulse = struct.unpack(f'={length}h', shortbuffer)
            pulsenum += 1
            baseline = float(sum(pulse[:10]))/10
            pulse = [baseline - float(elem) for elem in pulse] # subtract baseline from pulse
            # recording counts
            if max(pulse) > threshold:
                if not pile_up_flag(pulse):
                    count +=1
                    short, long = pulseAreaEJ276(pulse)
                    areaArray.append(long)
                    r = long/short
                    ratioArray.append(r)
                else:
                    pileUpCount +=1
            if time_elasped_sec > currentCycle: # check for count after as soon as 1 cycle is complete
                print("Analysed "+ str(pulsenum)+ " pulses after " + str(currentCycle)+" seconds")
                currentCycle += cycle
                countArray.append(count)
                count = 0 # reset count for next cycle    
    # dat file has closed
    print("Total number of pulses:" + str(pulsenum)+"\n")
    print("Total number of pile-up pulses: %d"%(pileUpCount))
    print("Total number of processed pulse: %d" % len(areaArray))
    save(areaArray, ratioArray, filename = "Area-PSD-og-code-output",xlabel = "PH", ylabel = "PSD")
    buildTimeTrace(countArray, cycle, filename = "Time-trace-og-code-output")
    print("Hecho. Hasta luego\n")






    


        
        


