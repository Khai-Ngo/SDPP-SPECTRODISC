## Scintillator Digital Pulse Processing for SPECTROscopy and pulse shape DISCrimination (SDPP-SPECTRODISC)

A tkinter program that performs pulse shape discrimination (PSD) analysis of digitized scintillator pulses via the charge integration method.
### Installation
[Add something here later]
### PSD analysis method
The program takes in raw pulse binary data. Currently the binary data formats from CAEN wavedump.exe and Picoscope 5444 are supported since we use these digitizers at work. 
For each pulse, the program calculates the baseline by averaging the first n samples specified by the user. The pulse is flipped upside-down if the raw pulse is specified to have negative polarity, as it is often for the case scintillator detectors.
The start of the pulse is the point at which the pulse crosses a threshold, shifted backwards by an amount called the pre-gate.
Then the pulse is numerically integrated twice from the identified start over two time intervals: short gate and long gate. 
The PSD criteria is defined as 1-Qshort/Qlong. The total charge can be taken as Qlong, or the user can choose to integrate the pulse for a third time by specifying the lenght of the total charge gate since sometimes the optimal long gate for PSD might not cover the whole pulse. 
Be sure to check the box "Same as long gate" if a third integration is not required.
Finally, please note that the following parameters do not matter when analysing Picoscope data: baseline, threshold, and pulse polarity. 

Upon clicking analyse, the user is prompted to choose save destination of the analysis results, which is in the format of a three-column .txt file. The columns in order are: pulse height, psd value, and time stamp. 
This result file can be read by SDPP-SPECTRODISC again to perform post analysis and graph plotting. 
### Post analysis and graph plotting

### Possible improvements

1. Implement data validation for the input fields.
2. Implement count rate analysis into the program (currently used as a separate module)
3. Implement optional feature pile-up rejection 
4. Some sort of optimization idk
