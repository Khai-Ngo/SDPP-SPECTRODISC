# Scintillator-analysis
Scintillator-analysis.py contains functions that build detector's PHS, count per second time trace, and export data to plot PSD scatterplot

plotColorMap.py plots PSD scatterplot, given full path of the export file of Scintillator-analysis.py, and 4 arguments specifying plot limits

plotPHS.py plot PHS. Requires 6 arguments. Argv 1: export file of Scintillator.py; Argv 2: name of output PHS file (saved in same folder as script); Argv3: PSD ratio cut; Argv4-5: specifies range of PHS; Argv6: number of bins

py <script's-name-here.py> in cmd to run the Python script
