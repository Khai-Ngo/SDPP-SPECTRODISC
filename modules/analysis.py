import struct
import scipy.integrate
import os
import re

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)
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
    shortInte = scipy.integrate.trapz (pulse[startIndex:stopShort+1], None, dx = 1.0) 
    longInte = scipy.integrate.trapz (pulse[startIndex:stopLong+1], None, dx = 1.0)
    PSD = (longInte-shortInte)/longInte
    return longInte, PSD
def save(x, y, z, outPath):
    """
    Write data to text file. Current suppports writing 3 lists
    But could extend to writing any number of lists
    Clears all lists from memory after writing to file
    """
    assert len(x) == len(y) and len(x) == len(z), "To write to txt, need same length array!"
    with open(outPath, "a") as f:
        for x_, y_, z_, in zip(x, y, z):
            f.write("{}\t{}\t{}\n".format(x_, y_, z_))
    # clear lists after writing to file
    x.clear()
    y.clear()
    z.clear()
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
def CAEN(fname, output, mode, threshold, pregate, **kwargs):
    # initialise variables
    areaArray, ratioArray, tArr = [], [], []
    pulsenum = 0 
    # select correct analysis method
    if mode == 1:
        analyse = pulseAreaEJ276
    elif mode == 2:
        analyse = pulseAreaCLYC
    else:
        raise ValueError('Invalid mode. Valid modes are 1 or 2')
    # fname could either be a file or a folder
    fileList = [fname + "\\" + name for name in sorted_alphanumeric(os.listdir(fname))] if os.path.isdir(fname) else [fname]   
    for a_file in fileList:
        if a_file.endswith(".dat"):
            with open(a_file, 'rb') as f:
                print("Reading from {}".format(a_file))
                while True:
                    # read header for pulse length and time stamp
                    buffer = f.read(24)
                    if not buffer: break # eof exit
                    length, idk2, idk3, idk4, idk5, this_time_stamp = struct.unpack('=iiiiiI', buffer)
                    length = int((length-24)/2)
                    currentTimeStamp = float(this_time_stamp) * 0.008 # in microseconds
                    # read and analyse pulse
                    pulse = struct.unpack(f'={length}h', f.read(2*length))
                    pulsenum += 1
                    baseline = float(sum(pulse[:10]))/10
                    pulse = [baseline - float(elem) for elem in pulse] # subtract baseline from pulse
                    # recording counts
                    if max(pulse) > threshold:
                        PH, r = analyse(pulse, threshold, pregate, **kwargs)
                        areaArray.append(PH)
                        ratioArray.append(r)
                        tArr.append(currentTimeStamp)
                    if pulsenum % 10000 == 0: # save to file every batch of 10k pulses
                        print ("Analysed {} pulses".format(pulsenum))
                        print("Total number of accepted pulse: {}".format(len(areaArray)))
                        save(areaArray, ratioArray, tArr, output)
            # dat file has closed
            print("Analysed {} pulses".format(pulsenum))
            print("Total number of accepted pulse: {}\n".format(len(areaArray)))
            save(areaArray, ratioArray, tArr, output) # save leftovers
    print("Analysis complete!\n")
def Pico(fname, output, mode, pregate, **kwargs): # no need for threshold variable because the traces file saves the trigger level used during DAQ
    # initialise variables
    areaArray, ratioArray, tArr = [], [], []
    # select correct analysis method
    if mode == 1:
        analyse = pulseAreaEJ276
    elif mode == 2:
        analyse = pulseAreaCLYC
    else:
        raise ValueError('Invalid mode. Valid modes are 1 or 2')
    # fname coukd either be a file or a folder
    fileList = [fname + "\\" + name for name in sorted_alphanumeric(os.listdir(fname))] if os.path.isdir(fname) else [fname]   
    for a_file in fileList:
        if a_file.endswith(".traces"):
            with open(a_file, 'rb') as file:
                print("Reading from {}".format(a_file))
                # Read overall header
                # Read Picoscope version (Note that the rest of the code assumes that digitizer is Picoscope-5444-V3)
                progVersionStrlen = struct.unpack('=I',file.read(4))[0] #length of version string (Int32)
                buffer = struct.unpack(f'={progVersionStrlen}c', file.read(progVersionStrlen))
                progVersionStr = ''.join([byte.decode('utf-8') for byte in buffer])
                # Read the comment that the user has entered as description of the run
                runDescriptionStrlen = struct.unpack('=I', file.read(4))[0]
                buffer = struct.unpack(f'{runDescriptionStrlen}c', file.read(runDescriptionStrlen))
                runDescriptionStr =  ''.join([byte.decode('utf-8') for byte in buffer])
                # Read the resolution for V3 syntax or higher
                resolution = struct.unpack('=I', file.read(4))[0]
                # Read channel information i.e. scale factor, offset, sampling interval and record length
                NbrChannels = struct.unpack('=I', file.read(4))[0]
                ChanEnabled = [buffer for buffer in struct.unpack(f'={NbrChannels}?', file.read(NbrChannels))]
                VoltsScaleFact = [buffer for buffer in struct.unpack(f'={NbrChannels}d', file.read(NbrChannels*8))]
                ChanOffsetVolts = [buffer for buffer in struct.unpack(f'={NbrChannels}d', file.read(NbrChannels*8))]
                SampInterval, NbrSamples = struct.unpack('=dI', file.read(12))
                # Read trigger information
                # Trigger slope: 0 = Above, 1 = Below, 2 = Rising, 3 = Falling, 4 = RisingOrFalling. Other trigger modes are not (yet) supported.
                # External trig info is stored on separate set of variables
                TriggerEnabled = [buffer for buffer in struct.unpack(f'={NbrChannels}?', file.read(NbrChannels))]
                ExtTrigEnabled = struct.unpack('=?', file.read(1))[0]
                TriggerLevel = [buffer for buffer in struct.unpack(f'={NbrChannels}d', file.read(NbrChannels*8))]
                ExtTrigLevel = struct.unpack('=d', file.read(8))[0]
                TriggerSlope = [buffer for buffer in struct.unpack(f'={NbrChannels}I', file.read(NbrChannels*4))]
                ExtTrigSlope = struct.unpack('=I', file.read(4))[0]
                # Continuously read and process events. Assumption: only 1 channel is saved
                while True:        
                    # read event header
                    buffer = file.read(16)
                    if not buffer: break #eof exit
                    # Read index of currrent event, time elasped since start of the run (in seconds), and number of saved traces in this event
                    CurEvent, eveRunTime, nbrSavedTraces = struct.unpack('=IdI', buffer)
                    # read which channels the traces were saved to
                    savedChannels = [buffer for buffer in struct.unpack(f'={NbrChannels}?', file.read(NbrChannels))]
                    # read trigger offset time in seconds, from start of trace
                    trigTime = struct.unpack('=d', file.read(8))[0]
                    # read trace of every saved channel one by one, but it's assumed there's only 1 channel enabled
                    for i in range(NbrChannels):
                        if savedChannels[i]:
                            pulse = struct.unpack(f'={NbrSamples}h', file.read(2*NbrSamples))
                            pulse = [VoltsScaleFact[i]*elem - ChanOffsetVolts[i] for elem in pulse] 
                            # analyse the trace here. Again, it's assumed only 1 channel is active
                            pulse = [-elem for elem in pulse] #baseline is 0 for Picoscope-5444-V3
                            threshold = -TriggerLevel[i]
                            if max(pulse) > threshold:
                                PH, r = analyse(pulse, threshold, pregate, **kwargs)
                                areaArray.append(PH)
                                ratioArray.append(r)
                                tArr.append(eveRunTime)
                    if CurEvent % 10000 == 0: # save to file every batch of 10k pulses
                        print('Processed {} pulses'.format(CurEvent))
                        print('Accepted {} pulses'.format(len(areaArray)))
                        save(areaArray, ratioArray, tArr, output)
            # traces file has closed
            print('Processed {} pulses'.format(CurEvent))
            print('Accepted {} pulses'.format(len(areaArray)))
            save(areaArray, ratioArray, tArr, output) # save leftover pulses
    print("Analysis complete!\n")
def main():
    # for module testing
    import sys
    #CAEN(sys.argv[1], sys.argv[2], mode = 2, threshold = 10, pregate = 8, allGate = 1800, W1 = 80, W2 = 500, delay = 20)
    Pico(sys.argv[1], sys.argv[2], mode = 1, pregate = int(16/8), shortGate = int(72/8), longGate = int(272/8))
if __name__ == '__main__':
    main()
