import struct
import scipy.integrate
import sys

def pulseAreaCLYC (pulse, threshold, pregate, allGate, W1 = 80, W2 = 500, delay = 20):
    """
    PSD method usually applied to CLYC
    PSD = W2/(W1+W2)
    recommend W1-W2-delay = 80-500-20 ns
    allGate: as long as possible
    """
    # detect start of the gate
    startIndex = 0
    for i, elem in enumerate(pulse):
         if elem > threshold:
             startIndex = i
             break
    startIndex -= pregate if startIndex > pregate - 1 else 0
    # determine end of the gate
    end = startIndex+allGate if startIndex + allGate < len(pulse) else len(pulse)-1
    # perform integration
    shortInte = scipy.integrate.trapz (pulse[startIndex:startIndex+W1+1], None, dx = 1.0) 
    longInte = scipy.integrate.trapz (pulse[startIndex+W1+delay:startIndex+W1+delay+W2+1], None, dx = 1.0)
    allInte = scipy.integrate.trapz (pulse[startIndex:end+1], None, dx = 1.0)
    PSD = longInte/(shortInte+longInte)
    return allInte, PSD
def pulseAreaEJ276 (pulse, threshold, pregate, shortGate =60, longGate = 220):
    """
    PSD method usually applied to plastic scintillators
    PSD = longGate/shortGate
    recommend short-long = 60-220ns
    """
    # detect start of the gate
    startIndex = 0
    for i, elem in enumerate(pulse):
         if elem > threshold:
             startIndex = i
             break
    startIndex -= pregate if startIndex > pregate - 1 else 0
    # determine end of the gate
    stopShort = startIndex + shortGate
    stopLong = startIndex + longGate if startIndex + longGate < len(pulse) else len(pulse) -1
    # perform integration
    shortInte = scipy.integrate.trapz (pulseArray[startIndex:stopShort+1], None, dx = 1.0) 
    longInte = scipy.integrate.trapz (pulseArray[startIndex:stopLong+1], None, dx = 1.0)
    PSD = longInte/shortInte
    return longInte, PSD
def save(x, y, z, outPath):
    assert len(x) == len(y) and len(x) == len(z), "To write to txt, need same length array!"
    with open(outPath, "a") as f:
        for x_, y_, z_, in zip(x, y, z):
            f.write("{}\t{}\t{}\n".format(x_, y_, z_))
def trapezoidal (pulse, L = 2, G = 7):
    pulse_Ftrap = []
    for i in range (len(pulse)-G-2*L):
        Vav1 = sum([elem for elem in pulse[i:i+L]])/L
        Vav2 = sum([elem for elem in pulse[i+L+G:i+2*L+G]])/L
        pulse_Ftrap.append(Vav2-Vav1)
    return pulse_Ftrap
def pile_up (pulse, step = 5, cfd = 0.15):
    pulse_Ftrap = trapezoidal(pulse)
    trigger = max(pulse_Ftrap)*cfd
    count = 0
    flag = 1
    for elem in pulse_Ftrap[::step]:
        if flag == 1 and elem > trigger:
            count += 1
            flag = 0
        if flag == 0 and elem < 0:
            count +=1
            flag =1
        if count > 2:
            return True
    return False
