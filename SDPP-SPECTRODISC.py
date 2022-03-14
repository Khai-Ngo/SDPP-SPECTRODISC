from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from modules import postprocess as pp
from modules import analysis

class labelledFields:
    def __init__(self, frame, label, height = 10, txtwidth = 10, padding = "3 3 12 12"):
        self.Frame = ttk.Frame(frame, height = height, padding = padding)
        self.Label = ttk.Label(self.Frame, text = label)
        self.Field = ttk.Entry(self.Frame, width = txtwidth)
    def place(self, row, column, columnspan=1, txtboxspan = 1):
        self.Frame.grid(row = row, column = column, columnspan = columnspan, sticky = "W")
        self.Label.grid(row = 0, column = 0)
        self.Field.grid(row = 0, column = 1, columnspan = txtboxspan)
    def get(self):
        return self.Field.get()
    def set (self, text):
        self.Field.insert(0, text)
    def clear(self):
        self.Field.delete(0, END)
    def disable(self):
        self.Field.state(['disabled'])
    def enable(self):
        self.Field.state(['!disabled'])
class fileDialogButtons (labelledFields):
    """
    Object variables area: title, filetypes, Button, and txtboxspan
    """
    def __init__(self, frame, label,  title = "Select a file", filetypes=(("Text files","*.txt"), ("All files","*.*")), height = 5, txtwidth = 10, padding = "3 3 12 12"):
        labelledFields.__init__(self, frame, label, height = height, txtwidth = txtwidth, padding = padding)
        self.title = title
        self.filetypes = filetypes
        self.Button = ttk.Button (self.Frame, text = "...", command = self.open_file, width = 2)
    def open_file(self):
        filename = filedialog.askopenfilename(initialdir = "/", title = self.title, filetypes= self.filetypes)
        self.Field.delete(0, END)
        self.Field.insert(0, filename)
    def open_folder(self):
        foldername = filedialog.askdirectory(initialdir = "/", title = self.title, mustexist = True)
        self.Field.delete(0, END)
        self.Field.insert(0, foldername) 
    def place(self, row, column, columnspan = 1, txtboxspan = 1):
        labelledFields.place(self, row = row, column = column, columnspan = columnspan, txtboxspan = txtboxspan)
        self.Button.grid(row = 0, column = 1+txtboxspan)
        self.txtboxspan = txtboxspan
    def update_folder_input(self, title):
        """
        Change what the dialog button opens. Now it takes in folder instead
        Never call this function before object.place has been called at least once before (such that self.txtboxspan is defined)
        """
        self.title =title
        self.Button.grid_forget()
        self.Button = ttk.Button(self.Frame, text ="...", command = self.open_folder, width = 2)
        self.Button.grid(row = 0, column = 1+self.txtboxspan)
    def update_file_input(self, title, filetypes):
        """
        Change what the dialog button opens. Now it takes in single files, and may take in other filetypes too. 
        Never call this function before object.place has been called at least once before (such that self.txtboxspan is defined)
        """
        self.title = title
        self.filetypes = filetypes
        self.Button.grid_forget()
        self.Button = ttk.Button(self.Frame, text = "...", command = self.open_file, width = 2)
        self.Button.grid(row = 0, column = 1+self.txtboxspan)
class dropdownMenus:
    def __init__(self, frame, label, options, width = 15, height = 5, padding = "3 3 12 12"):
        self.Frame = ttk.Frame(frame, height = height, padding = padding)
        self.Label = ttk.Label(self.Frame, text = label)
        self.clicked = StringVar()
        self.Menu= ttk.Combobox(self.Frame, textvariable = self.clicked, width = width)
        self.Menu['values'] = options
        self.clicked.set(options[0])
    def place(self, row, column, columnspan = 1, boxspan = 1):
        self.Frame.grid(row = row, column = column, columnspan = columnspan, sticky = "W")
        self.Label.grid(row = 0, column = 0)
        self.Menu.grid(row = 0, column = 1, columnspan = boxspan)
    def get(self):
        return self.clicked.get()
def plotScatterplot():
    global truncate
    if row_no.get() == 'inf' or row_no.get() == 'INF':
        max_rows = None
    else: max_rows = int(row_no.get())
    x, y = pp.readExport(inFile2.get(), max_rows = max_rows)
    if a_const.get() and b_const.get():
        a = float(a_const.get())
        b = float(b_const.get())
        x = a*x + b
    if truncate.get():
        x, y = pp.dataTruncator(x, y, xlow = float(Min_x.get()), xhigh = float(Max_x.get()), ylow = float(Min_y.get()), yhigh = float(Max_y.get()))
    ax = pp.density_scatter(x, y, xlow = float(Min_x.get()), xhigh = float(Max_x.get()), ylow = float(Min_y.get()), yhigh = float(Max_y.get()), bins = [1000,1000], xlabel = x_name.get(), ylabel = y_name.get()) 
def plotHist():
    global truncate
    filename = filedialog.asksaveasfilename(initialdir = "/", title = "Save histogram to", defaultextension = ".txt",filetypes=(("Text files","*.txt"), ("All files","*.*")))
    x, y = pp.readExport(inFile2.get())
    if a_const.get() and b_const.get():
        a = float(a_const.get())
        b = float(b_const.get())
        x = a*x + b
    if truncate.get():
        x, y = pp.dataTruncator(x, y, xlow = float(Min_x.get()), xhigh = float(Max_x.get()), ylow = float(Min_y.get()), yhigh = float(Max_y.get()))    
    auto = True if autobinning.get() == 'Yes' else False
    if quantity.get() == 'Pulse Height':
        ax = pp.buildHist(x, filename, minVal = float(Min_x.get()), maxVal = float(Max_x.get()), noOfBins = int(noOfBins.get()), auto = auto, plot = True, save = True)
    else:
        ax = pp.buildHist(y, filename, minVal = float(Min_y.get()), maxVal = float(Max_y.get()), noOfBins = int(noOfBins.get()), auto = auto, plot = True, save = True)        
def write_time_trace():
    outputPath = filedialog.asksaveasfilename(initialdir = "/", title = "Save histogram to", defaultextension = ".txt",filetypes=(("Text files","*.txt"), ("All files","*.*")))
    t = pp.readTime(inFile2.get())
    pp.timeTrace (t, outputPath)
def multi_checkbox_command(flag):
    global inFile1
    if flag:
        inFile1.update_folder_input(title="Select a folder")
    else:
        inFile1.update_file_input(title = "Select a file", filetypes = (("DAT files","*.dat"), ("TRACES files", "*.traces"),("All files","*.*")))
def charge_checkbox_cmd(flag):
    global charge_gate_box
    if flag:
        charge_gate_box.disable()
    else:
        charge_gate_box.enable()
def callback_digitizer_box(dropDownMenu, *labelledFields):
    if dropDownMenu.get() == 'PicoScope5444_V3':
        for field in labelledFields:
            field.disable()
    else:
        for field in labelledFields:
            field.enable()
def analyse_button():
    global charge_chbx_bool
    outFile = filedialog.asksaveasfilename(initialdir = "/", title = "Save output to", defaultextension = ".txt",filetypes=(("Text files","*.txt"), ("All files","*.*")))
    fname = inFile1.get()
    polarity = True if polarity_box.get() == 'Positive' else False
    shift = int(shift_back.get())
    short = int(shortGate_box.get())
    long = int(longGate_box.get())
    qGate = long if charge_chbx_bool.get() else int(charge_gate_box.get())
    if digitizer_box.get() == "CAEN_10_bit":
        analysis.CAEN(fname = fname, output = outFile, baseline = int(baseline_box.get()), polarity = polarity, threshold = int(threshold_box.get()), pregate = shift, shortGate = short, longGate = long, qGate = qGate)
    elif digitizer_box.get() == "CAEN_14_bit":
        # divide by 2 because sampling frequency = 500 MHz (CAEN DT5730)
        analysis.CAEN(fname = fname, output = outFile, baseline = int(baseline_box.get()), polarity = polarity, threshold = int(threshold_box.get()), pregate = int(shift/2), shortGate = int(short/2), longGate = int(long/2), qGate = int(qGate/2))
    else: #last option is obviously "PicoScope5444_V3"
        # divide by 8 because sampling frequency = 128 MHz
        analysis.Pico(fname = fname, output = outFile, pregate = int(shift/8), shortGate = int(short/8), longGate = int(long/8), qGate = int(qGate/8))
if __name__ == '__main__':
    # Create the window
    root = Tk()
    root.title("SDPP-SPECTRODISC")
    root.geometry("510x420")
    root.resizable(False, False)
    # Create widgets
    n = ttk.Notebook(root)
    f1 = ttk.Frame(n)
    f2 = ttk.Frame(n)
    n.add(f1, text = 'Analyse')
    n.add(f2, text = 'Plot')
    # Tab 1 widgets
    titleLabel1 = ttk.Label(f1, text = "Pulse height and pulse shape discrimination analysis - charge comparison method")
    inFile1 = fileDialogButtons(f1, label = 'Input data:', filetypes = (("DAT files","*.dat"), ("TRACES files", "*.traces"),("All files","*.*")),txtwidth = 69)
    multi = IntVar(value = 0)
    multi_checkbox = ttk.Checkbutton(f1, text = 'Choose folder instead?', command = lambda: multi_checkbox_command(multi.get()), variable = multi)

    sub_frame = ttk.Frame(f1)
    digitizer_box = dropdownMenus(sub_frame, width = 28, label = "Digitizer:", options = ("CAEN_10_bit", "CAEN_14_bit","PicoScope5444_V3"))
    threshold_box = labelledFields(sub_frame, label = 'Threshold:', txtwidth = 29)
    digitizer_box.Menu.bind('<<ComboboxSelected>>', func = lambda event: callback_digitizer_box(digitizer_box, threshold_box, baseline_box))
    shift_back = labelledFields(sub_frame, label = 'Pre-gate (ns):', txtwidth = 26)
    baseline_box = labelledFields(sub_frame, label = 'Baseline (samples):', txtwidth = 22)
    polarity_box = dropdownMenus(sub_frame, width = 28, label = 'Polarity:', options =("Negative", "Positive"))
    longGate_box = labelledFields(sub_frame, label = 'Long Gate (ns):', txtwidth = 25)
    shortGate_box = labelledFields(sub_frame, label = 'Short Gate (ns):', txtwidth = 24)
    charge_gate_box = labelledFields(sub_frame, label = 'Total Charge (ns):', txtwidth = 23)
    charge_chbx_bool = IntVar(value = 0)
    charge_checkbox = ttk.Checkbutton(sub_frame, text = 'Same as long gate?', command = lambda: charge_checkbox_cmd(charge_chbx_bool.get()), variable = charge_chbx_bool)
    analyse = ttk.Button(sub_frame, text = 'Analyse', command = analyse_button, width = 39)

    # Tab 2 widgets
    titleLabel2 = ttk.Label(f2, text = "PSD scatterplot and histogram plotting")
    inFile2 = fileDialogButtons(f2, label = 'Input file:', txtwidth = 70)

    range_controls = ttk.LabelFrame(f2, text = 'Range controls')
    Min_x = labelledFields(range_controls, label = 'Minimum PH:', txtwidth = 24)
    Max_x = labelledFields(range_controls, label = 'Maximum PH:', txtwidth = 24)
    Min_y = labelledFields(range_controls, label = 'Minimum PSD:', txtwidth = 23)
    Max_y = labelledFields(range_controls, label = 'Maximum PSD:', txtwidth = 23)
    truncate = IntVar(value = 1)
    check_truncate = ttk.Checkbutton(range_controls, text = 'Truncate raw data to range?', variable = truncate)
    row_no = labelledFields(range_controls, label = 'Lines to read:', txtwidth = 25)
    
    spectrum_controls = ttk.LabelFrame(f2, text = 'Histogram building options')
    quantity = dropdownMenus(spectrum_controls, label = "Quantity:", options = ("Pulse Height", "PSD"))
    autobinning = dropdownMenus(spectrum_controls, width = 5, label = 'Auto-binning:', options = ("No", "Yes"))
    noOfBins = labelledFields(spectrum_controls, label = 'Number of bins:')
    
    plot_options = ttk.LabelFrame(f2, text = 'Plotting options')
    x_name = labelledFields( plot_options, label = 'x-axis label:')
    y_name = labelledFields( plot_options, label = 'y-axis label:')

    scaling = ttk.LabelFrame(f2, text = 'Scaling: PH -> A*PH + B')
    a_const = labelledFields( scaling, label = 'A:')
    b_const = labelledFields( scaling, label = 'B:') 
    
    scatterplot_button = ttk.Button(f2, text = 'Plot scatterplot', command = plotScatterplot)
    hist_button = ttk.Button(f2, text = 'Plot histogram', command = plotHist)
    time_button = ttk.Button (f2, text = 'Time trace', command = write_time_trace)
    # Place widgets
    n.grid(row = 0, column = 0)
    # Tab 1 widgets placement
    titleLabel1.grid(row = 0, column = 0, sticky = "W")
    inFile1.place(row = 1, column = 0, columnspan = 2)
    multi_checkbox.grid(row = 2, column = 0, sticky = "W")
    sub_frame.grid(row = 3, column = 0, sticky = "W")

    digitizer_box.place(row = 0, column = 0)
    threshold_box.place(row = 1, column = 0)
    shift_back.place(row = 1, column = 1)
    baseline_box.place(row = 2, column = 0)
    polarity_box.place(row = 2, column = 1)
    longGate_box.place(row = 3, column = 0)
    shortGate_box.place(row = 3, column = 1)
    charge_gate_box.place(row = 4, column = 0)
    charge_checkbox.grid(row = 4, column = 1, sticky = "W")
    analyse.grid(row = 0, column = 1, sticky = "W")
    
    # Tab 2 widgets placement
    titleLabel2.grid(row = 0, column = 0, columnspan = 3, sticky = "W")
    inFile2.place(row = 1, column = 0, columnspan = 3)
    
    range_controls.grid(row=2, column = 0, columnspan = 3, sticky = "W")
    Min_x.place(row = 0, column = 0)
    Max_x.place(row = 0, column = 1)
    Min_y.place(row = 1, column = 0)
    Max_y.place(row = 1, column = 1)
    check_truncate.grid(row =2, column =0, columnspan = 2, pady = 5, sticky = "W")
    row_no.place(row = 2, column = 1)
    row_no.set('1200000')
    
    spectrum_controls.grid(row = 3, column = 0, columnspan = 3, padx = 2 ,pady = 10, sticky = "W")
    quantity.place(row = 0, column = 0)
    autobinning.place(row = 0, column =1)
    noOfBins.place(row=0, column =2)
    
    scaling.grid(row = 4,column = 0, pady = 5, sticky = "W")
    a_const.place(row = 0, column = 0)
    b_const.place(row = 0, column = 1)

    plot_options.grid(row = 4, column = 1,columnspan = 2,padx = 10, pady = 5, sticky = "W")
    x_name.place(row =0 , column = 0)
    y_name.place(row = 0, column = 1)

    scatterplot_button.grid(row = 8, column = 0, pady = 10)
    hist_button.grid(row = 8, column = 1, pady = 10)
    time_button.grid(row = 8, column = 2, pady = 10)
    
    root.mainloop()
