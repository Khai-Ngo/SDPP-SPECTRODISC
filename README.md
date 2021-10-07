# Scintillator-analysis
Scintillator-analysis.py contains functions that build detector's PHS, count per second time trace, and export data to plot PSD scatterplot

plotColorMap.py plots PSD scatterplot. Takes in arguments from plotParams.par (Input-path, minPH, maxPH, minr, maxr)

plotPHS.py plot PHS (MeVee scale). Requires 5 arguments. Argv 1: export file of Scintillator.py; Argv 2: name of output PHS file (saved in same folder as script); Argv3: PSD ratio cut; Argv4: PHS bin width; Argv5: max bin val

py <script-name-here.py> in cmd to run the Python script
