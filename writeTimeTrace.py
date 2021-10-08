import sys
import matplotlib.pyplot as plt
def readTime(inputPath):
    with open(inputPath) as f:
        t = []
        lines = f.readlines()[1:]
        for line in lines:
            t.append(line.split()[2])
        return t
def writeTimeTrace (timeArr, filename):
    currentCycle = 1.0
    cycle = 1.0
    count = 0
    f = open(filename, "w")
    f.write("Time (s)\tCount\n")
    for t in timeArr:
        if t > currentCycle:
            f.write("{}\t{}\n".format(currentCycle, count))
            count = 0
            currentCycle += cycle
        else: 
            count +=1
    print("Output time trace to {}".format(filename))
if __name__ == '__main__':
    t = readTime(sys.argv[1])
    FirstTimeC = t[0]
    time_elasped_microsec = 0
    Reset = 0
    t_elasped_sec = []
    for timeStamp in t:
        currentTimeStamp = timeStamp + Reset - FirstTimeC
        if currentTimeStamp < time_elasped_microsec:
            Reset = Reset + 17179869.19
            time_elasped_microsec = currentTimeStamp + 17179869.19
        else: 
            time_elasped_microsec = currentTimeStamp
        t_elasped_sec.append(time_elasped_microsec / 1000000.0)
    writeTimeTrace(t_elasped_sec, sys.argv[2])
    