from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import postprocess as pp
import analysis

class labelledFields:
    def __init__(self, frame, label, padx = 5, pady = 5, width = 10, borderwidth = 5):
        self.Frame = LabelFrame(frame, padx=padx, pady=pady)
        self.Label = Label(self.Frame, text = label)
        self.Field = Entry(self.Frame, width = width, borderwidth = borderwidth)
    def place(self, row, column, columnspan=1, txtboxspan = 1):
        self.Frame.grid(row = row, column = column, columnspan = columnspan)
        self.Label.grid(row = 0, column = 0)
        self.Field.grid(row = 0, column = 1, columnspan = txtboxspan)
    def get(self):
        return self.Field.get()
    def clear(self):
        self.Field.delete(0, END)
class fileDialogButtons (labelledFields):
    """
    Object variables area: title, filetypes, Button, and txtboxspan
    """
    def __init__(self, frame, label,  title = "Select a file", filetypes=(("Text files","*.txt"), ("All files","*.*")), padx = 5, pady = 5, width = 10, borderwidth = 5):
        labelledFields.__init__(self, frame, label, padx = 5, pady = 5, width = width, borderwidth = borderwidth)
        self.title = title
        self.filetypes = filetypes
        self.Button = Button (self.Frame, text = "...", command = self.open_file)
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
        self.Button = Button(self.Frame, text ="...", command = self.open_folder)
        self.Button.grid(row = 0, column = 1+self.txtboxspan)
    def update_file_input(self, title, filetypes):
        """
        Change what the dialog button opens. Now it takes in single files, and may take in other filetypes too. 
        Never call this function before object.place has been called at least once before (such that self.txtboxspan is defined)
        """
        self.title = title
        self.filetypes = filetypes
        self.Button.grid_forget()
        self.Button = Button(self.Frame, text = "...", command = self.open_file)
        self.Button.grid(row = 0, column = 1+self.txtboxspan)
class dropdownMenus:
    def __init__(self, frame, label, options, padx = 5, pady = 5):
        self.Frame = LabelFrame(frame, padx=padx, pady=pady)
        self.Label = Label(self.Frame, text = label)
        self.clicked = StringVar()
        self.Menu= OptionMenu(self.Frame, self.clicked, *options)
        self.clicked.set(options[0])
    def place(self, row, column, columnspan = 1, boxspan = 1):
        self.Frame.grid(row = row, column = column, columnspan = columnspan)
        self.Label.grid(row = 0, column = 0)
        self.Menu.grid(row = 0, column = 1, columnspan = boxspan)
    def get(self):
        return self.clicked.get()
def plotScatterplot():
    global truncate
    x, y = pp.readExport(inFile2.get(), max_rows = 1.0e6)
    if a_const.get() and b_const.get():
        a = float(a_const.get())
        b = float(b_const.get())
        x = a*x + b
    if truncate.get():
        x, y = pp.dataTruncator(x, y, xlow = float(Min_x.get()), xhigh = float(Max_x.get()), ylow = float(Min_y.get()), yhigh = float(Max_y.get()))
    pp.density_scatter(x, y, xlow = float(Min_x.get()), xhigh = float(Max_x.get()), ylow = float(Min_y.get()), yhigh = float(Max_y.get()), bins = [1000,1000], xlabel = x_name.get(), ylabel = y_name.get())
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
        pp.buildHist(x, filename, minVal = float(Min_x.get()), maxVal = float(Max_x.get()), noOfBins = int(noOfBins.get()), auto = auto, plot = True, save = True)
    else:
        pp.buildHist(y, filename, minVal = float(Min_y.get()), maxVal = float(Max_y.get()), noOfBins = int(noOfBins.get()), auto = auto, plot = True, save = True)        
def clear_all():
    inFile.clear()
    Min_x.clear()
    Max_x.clear()
    Min_y.clear()
    Max_y.clear()
    x_name.clear()
    y_name.clear()
    a_const.clear()
    b_const.clear()
    noOfBins.clear()
def multi_checkbox_command(flag):
    global inFile1
    if flag:
        inFile1.update_folder_input(title="Select a folder")
    else:
        inFile1.update_file_input(title = "Select a file", filetypes = (("DAT files","*.dat"), ("TRACES files", "*.traces"),("All files","*.*")))
def analyse_button1():
    outFile = filedialog.asksaveasfilename(initialdir = "/", title = "Save output to", defaultextension = ".txt",filetypes=(("Text files","*.txt"), ("All files","*.*")))
    fname = inFile1.get()
    short = int(shortGate_box.get())
    long = int(longGate_box.get())
    thres = int(threshold_box1.get())
    shift = int(shift_back1.get())
    if digitizer_box1.get() == "CAEN_10_bit":
        analysis.CAEN(fname = fname, output = outFile, mode = 1, threshold = thres, pregate = shift, shortGate = short, longGate = long)
    elif digitizer_box1.get() == "CAEN_14_bit":
        analysis.CAEN(fname = fname, output = outFile, mode = 1, threshold = thres, pregate = int(shift/2), shortGate = int(short/2), longGate = int(long/2))
    else: #last option is obviously "PicoScope5444_V3"
        #analyse.Pico(fname = fname, output = outFile, mode = 1, threshold = thres, pregate = shift, shortGate = short, longGate = long)
        pass
def analyse_button2():
    outFile = filedialog.asksaveasfilename(initialdir = "/", title = "Save output to", defaultextension = ".txt",filetypes=(("Text files","*.txt"), ("All files","*.*")))
    fname = inFile1.get()
    W1 = int(W1_box.get())
    W2 = int(W2_box.get())
    delay = int(delay_box.get())
    thres = int(threshold_box2.get())
    shift = int(shift_back2.get())
    allGate = int(allGate_box.get())
    if digitizer_box2.get() == "CAEN_10_bit":
        analysis.CAEN(fname = fname, output = outFile, mode = 2, threshold = thres, pregate = shift, allGate = allGate, W1 = W1, W2 = W2, delay = delay)
    elif digitizer_box2.get() == "CAEN_14_bit":
        analysis.CAEN(fname =fname, output = outFile, mode = 2, threshold = thres, pregate = int(shift/2), allGate = int(allGate/2), W1 = int(W1/2), W2 = int(W2/2), delay = int(delay/2))
    else: #last option is obviously "PicoScope5444_V3"
        #analyse.Pico(fname = fname, output = outFile, mode = 2, threshold = thres, pregate = shift, allGate = allGate, W1 = W1, W2 = W2, delay = delay)
        pass
if __name__ == '__main__':
    # Create the window
    root = Tk()
    root.title("Digitizer PSD analysis")
    # Create widgets
    n = ttk.Notebook(root)
    f1 = ttk.Frame(n)
    f2 = ttk.Frame(n)
    n.add(f1, text = 'Analyse')
    n.add(f2, text = 'Plot')
    # Tab 1 widgets
    titleLabel1 = Label(f1, text = "Pulse height and pulse shape discrimination analysis - charge comparison method", padx = 10, pady=10)
    inFile1 = fileDialogButtons(f1, label = 'Input data:', filetypes = (("DAT files","*.dat"), ("TRACES files", "*.traces"),("All files","*.*")),width = 125)
    multi = IntVar(value = 0)
    multi_checkbox = Checkbutton(f1, text = 'Choose folder instead?', command = lambda: multi_checkbox_command(multi.get()), variable = multi)
    sub_notebook = ttk.Notebook(f1)
    meth1_frame = ttk.Frame(sub_notebook)
    meth2_frame = ttk.Frame(sub_notebook)
    sub_notebook.add(meth1_frame, text = 'Qlong/Qshort')
    sub_notebook.add(meth2_frame, text = 'W2/(W1+W2)')
    
    digitizer_box1 = dropdownMenus(meth1_frame, label = "Digitizer:", options = ("CAEN_10_bit", "CAEN_14_bit","PicoScope5444_V3"), padx = 145)
    threshold_box1= labelledFields(meth1_frame, label = 'Threshold:')
    shift_back1 = labelledFields(meth1_frame, label = 'Pre-gate (ns):', padx = 17)
    longGate_box = labelledFields(meth1_frame, label = 'Long Gate (ns):',padx = 52)
    shortGate_box = labelledFields(meth1_frame, label = 'Short Gate (ns):',padx = 30)
    analyse1 = Button(meth1_frame, text = 'Analyse', command = analyse_button1, padx = 220, pady= 10)

    digitizer_box2 = dropdownMenus(meth2_frame, label = "Digitizer:", options = ("CAEN_10_bit", "CAEN_14_bit","PicoScope5444_V3"), padx = 145)
    threshold_box2= labelledFields(meth2_frame, label = 'Threshold:')
    shift_back2 = labelledFields(meth2_frame, label = 'Pre-gate (ns):', padx = 17)
    W1_box = labelledFields(meth2_frame, label = 'W1 (ns):',padx = 70)
    delay_box = labelledFields(meth2_frame, label = 'Delay (ns):',padx = 65)
    W2_box = labelledFields(meth2_frame, label = 'W2 (ns)', padx = 50)
    allGate_box = labelledFields(meth2_frame, label = 'Gate (ns)', padx = 50)
    analyse2 = Button(meth2_frame, text = 'Analyse', command = analyse_button2, padx = 85, pady= 8)
    # Tab 2 widgets
    titleLabel2 = Label(f2, text = "PSD scatterplot and histogram plotting", padx = 10, pady=10)
    inFile2 = fileDialogButtons(f2, label = 'Input file:', width = 125)

    range_controls = LabelFrame(f2, text = 'Range controls', padx = 5, pady =10)
    Min_x = labelledFields(range_controls, label = 'Minimum PH:')
    Max_x = labelledFields(range_controls, label = 'Maximum PH:')
    Min_y = labelledFields(range_controls, label = 'Minimum PSD:')
    Max_y = labelledFields(range_controls, label = 'Maximum PSD:')
    truncate = IntVar(value = 1)
    check_truncate = Checkbutton(range_controls, text = 'Truncate raw data to range?', variable = truncate)
    
    spectrum_controls = LabelFrame(f2, text = 'Further histogram building controls', padx = 20, pady =10)
    quantity = dropdownMenus(spectrum_controls, label = "Quantity:", options = ("Pulse Height", "PSD"))
    autobinning = dropdownMenus(spectrum_controls, label = 'Auto-binning:', options = ("No", "Yes"))
    noOfBins = labelledFields(spectrum_controls, label = 'Number of bins:')
    
    plot_options = LabelFrame(f2, text = 'Plotting options', padx=5, pady=5)
    x_name = labelledFields( plot_options, label = 'x-axis label:')
    y_name = labelledFields( plot_options, label = 'y-axis label:')

    scaling = LabelFrame(f2, text = 'Scaling: PH -> A*PH + B', padx = 5, pady = 5)
    a_const = labelledFields( scaling, label = 'A:')
    b_const = labelledFields( scaling, label = 'B:') 
    
    scatterplot_button = Button(f2, text = 'Plot scatterplot', command = plotScatterplot, padx = 20, pady=20, borderwidth = 5)
    hist_button = Button(f2, text = 'Plot histogram', command = plotHist, padx = 20, pady = 20, borderwidth= 5)
    clear_button = Button (f2, text = 'Clear all', command = clear_all, padx = 20, pady=20, borderwidth = 5)
    # Place widgets
    n.grid(row = 0, column = 0)
    # Tab 1 widgets placement
    titleLabel1.grid(row = 0, column = 0)
    inFile1.place(row = 1, column = 0, columnspan = 2)
    multi_checkbox.grid(row = 1, column = 2)
    sub_notebook.grid(row = 2, column = 0, pady = 20)

    digitizer_box1.place(row = 0, column = 0, columnspan = 2, boxspan = 2)
    threshold_box1.place(row = 1, column = 0)
    shift_back1.place(row = 1, column = 1)
    longGate_box.place(row = 2, column = 0)
    shortGate_box.place(row = 2, column = 1)
    analyse1.grid(row = 3, column = 0, columnspan = 2)

    digitizer_box2.place(row = 0, column = 0, columnspan = 2)
    threshold_box2.place(row = 1, column = 0)
    shift_back2.place(row = 1, column = 1)
    W1_box.place(row = 2, column = 0)
    W2_box.place(row = 2, column = 1)
    allGate_box.place(row = 3, column = 0)
    delay_box.place(row = 3, column = 1)
    analyse2.grid(row = 4, column = 0, columnspan = 2)
    # Tab 2 widgets placement
    titleLabel2.grid(row = 0, column = 0)
    inFile2.place(row = 1, column = 0, columnspan = 2)
    
    range_controls.grid(row=2, column = 0, rowspan = 2, pady= 10)
    Min_x.place(row = 0, column = 0)
    Max_x.place(row = 0, column = 1)
    Min_y.place(row = 1, column = 0)
    Max_y.place(row = 1, column = 1)
    check_truncate.grid(row =2, column =0, columnspan = 2, pady = 5)
    
    spectrum_controls.grid(row = 2, column = 1, columnspan = 2, padx = 2 ,pady = 10)
    quantity.place(row = 0, column = 0)
    autobinning.place(row = 0, column =1)
    noOfBins.place(row=0, column =2)
    
    scaling.grid(row = 3,column = 1, pady = 5 )
    a_const.place(row = 0, column = 0)
    b_const.place(row = 0, column = 1)

    plot_options.grid(row = 3, column = 2,padx = 10, pady = 5)
    x_name.place(row =0 , column = 0)
    y_name.place(row = 0, column = 1)

    scatterplot_button.grid(row = 4, column = 0, pady = 10)
    hist_button.grid(row = 4, column = 1, pady = 10)
    clear_button.grid(row = 4, column = 2, pady = 10)
    
    root.mainloop()
