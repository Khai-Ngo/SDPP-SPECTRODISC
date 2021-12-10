## Scintillator Digital Pulse Processing for SPECTROscopy and pulse shape DISCrimination (SDPP-SPECTRODISC)

This is a software with GUI that analyses digitized pulses of radiation detectors (e.g. scintillators, diamond detectors, ...) by charge integration. It's mainly a personal project, as it's only a small part in a bigger project during my Year in Industry, which is rather more physics-focused. 

### Installation
[Add something here later]
### Background: nuclear spectroscopy and pulse shape discrimination
In neutron/gamma spectroscopy, the histogram of the distribution of pulses' height, a.k.a the pulse height spectrum (PHS), provides information on the nature of the radiation field being measured. Pulse height can mean the actually peak of the pulse, or the integrated charge of the pulse over a period of time. Here charge integration is the metric for pulse height.

For certain types of detectors, neutron/gamma pulse shape discrimination (PSD) is possible. This means that neutro-induced events and gamma-induced events produce differnt kinds of pulses, and in practicce this is quantified by the ratio of the charge integrated over different time gates. Detectors with PSD capabilities are often scintillators, which is what this software is mainly intended for. 

### Using SDPP-SPECTRODISC
The software takes in input binary files from CAEN and PICOSCOPE digitizers. Currently, it only supports inputs from CAEN DT5751, CAEN DT5730, waveforms acquired by WAVEDUMP.EXE, and PICOSCOPE 5444 V3, since these are directly relevant to my day to day applicaions at work. 

There are two charge comparison PSD methods supported: Qlong/Qshort and W2/(W1+W2). The first method simply integrates the pulse for a second time over the short gate (Qshort), and ratio Qlong/Qshort is the PSD criterion. Qlong is taken as the pulse height. Other groups also used (Qlong-Qshort)/Qlong, but this does not make a big difference in the Figure Of Merit (FOM). The second method integrates over the pulse 3 times: firstly over W1 gate, secondly over W2 gate, which starts after the end of W1 gate with a delay, and finally over the Gate, which is a measure for the pulse height like Qlong in the first method. The second method is not as common, but is relevant to CLYC-like scintillators. 

The user also needs to specify a threshold. Pulses whose maximum is lower than the threshold are not considered, while for the ones that do this determines the start of the integration gate. Often, this point is on the rising edge of the pulse, so a Pre-gate must be specified to shift the start of the gate back to the actual start of the pulse. Please be aware that the value of the threshold depends on the digitizer, so the user should have some knowledge of their DAQ system to pick a suitable number. Usually, picking a number close to the trigger threshold whike acquiring the data is good. There is no need to specify a threshold for PICOSCOPE digitizer since it saves the trigger threshold used during DAQ in its wavedump file. 

Once the user click "Analyse", the software outputs its results in a 3-colummn .txt file. The format is PH-PSD value-Time Stamp. This file can be given as an input to the Plot tab of this software. Here user can truncate their data, plot 2D PSD vs PH scatterplot, plot and output PHS and PSD spectrum. The user can also apply calibration scaling to the raw data, once they're known.  

### Possible improvements

1. Improve GUI: better arrangement of widgets, and add scroll bars
2. Implement data validation for the input fields to prevent the user from putting in trash data/missing data
3. Output time trace (counts per second vs seconds)
