from tkinter import *
from tkinter import filedialog
import postprocess as pp

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
class fileDialogButtons (labelledFields):
    def __init__(self, frame, label, padx = 5, pady = 5, width = 10, borderwidth = 5):
        labelledFields.__init__(self, frame, label, padx = 5, pady = 5, width = width, borderwidth = borderwidth)
        self.Button = Button (self.Frame, text = "...", command = self.open_file)
    def open_file(self):
        filename = filedialog.askopenfilename(initialdir = "/", title = "Select a text file", filetypes=(("Text files","*.txt"), ("All files","*.*")))
        self.Field.delete(0, END)
        self.Field.insert(0, filename)
    def place(self, row, column, columnspan = 1, txtboxspan = 1):
        labelledFields.place(self, row = row, column = column, columnspan = columnspan, txtboxspan = txtboxspan)
        self.Button.grid(row = 0, column = 1+txtboxspan)
class dropdownMenus:
    def __init__(self, frame, label, options, padx = 5, pady = 5):
        self.Frame = LabelFrame(frame, padx=padx, pady=pady)
        self.Label = Label(self.Frame, text = label)
        clicked = StringVar()
        self.Menu= OptionMenu(self.Frame, clicked, *options)
        clicked.set(options[0])
    def place(self, row, column, columnspan = 1, boxspan = 1):
        self.Frame.grid(row = row, column = column, columnspan = columnspan)
        self.Label.grid(row = 0, column = 0)
        self.Menu.grid(row = 0, column = 1, columnspan = boxspan)
def plotScatterplot():
    x, y = pp.readExport(inFile.get())
    x, y = pp.dataTruncator(x, y, xlow = int(Min_x.get()), xhigh = int(Max_x.get()), ylow = float(Min_y.get()), yhigh = float(Max_y.get()), numPoint = 1e6)
    a = 1
    b = 0
    if a_const.get() and b_const.get():
        a = float(a_const.get())
        b = float(b_const.get())
        x = a*x + b
    pp.density_scatter(x, y, xlow = a*int(Min_x.get())+b, xhigh = a*int(Max_x.get())+b, ylow = float(Min_y.get()), yhigh = float(Max_y.get()), bins = [1000,1000], xlabel = x_name.get(), ylabel = y_name.get())
def plotHist():
    return
if __name__ == '__main__':
    # Create the window
    root = Tk()
    root.title("Digitizer PSD analysis")
    # Create widgets
    titleLabel = Label(root, text = "PSD scatterplot and histogram plotting", padx = 10, pady=10)
    inFile = fileDialogButtons(root, label = 'Input file:', width = 125)
    
    range_controls = LabelFrame(root, text = 'Range controls', padx = 5, pady =25)
    Min_x = labelledFields(range_controls, label = 'Minimum PH:')
    Max_x = labelledFields(range_controls, label = 'Maximum PH:')
    Min_y = labelledFields(range_controls, label = 'Minimum PSD:')
    Max_y = labelledFields(range_controls, label = 'Minimum PSD:')
    
    spectrum_controls = LabelFrame(root, text = 'Further histogram building controls', padx = 22, pady = 5)
    quantity = dropdownMenus(spectrum_controls, label = "Quantity:", options = ("Pulse Height", "PSD"))
    autobinning = dropdownMenus(spectrum_controls, label = 'Auto-binning:', options = ("No", "Yes"))
    noOfBins = labelledFields(spectrum_controls, label = 'Number of bins:')
    
    plot_options = LabelFrame(root, text = 'Plotting options', padx=5, pady=5)
    x_name = labelledFields( plot_options, label = 'x-axis label:')
    y_name = labelledFields( plot_options, label = 'y-axis label:')

    mevee_scaling = LabelFrame(root, text = 'MeVee scaling: E (MeVee) = A*PH + B', padx = 5, pady = 5)
    a_const = labelledFields( mevee_scaling, label = 'A:')
    b_const = labelledFields( mevee_scaling, label = 'B:') 
    
    scatterplot_button = Button(root, text = 'Plot scatterplot', command = plotScatterplot, padx = 20, pady=20, borderwidth = 5)
    hist_button = Button(root, text = 'Plot histogram', command = plotHist, padx = 20, pady = 20, borderwidth= 5)
    
    # Place widgets
    titleLabel.grid(row = 0, column = 0)
    inFile.place(row = 1, column = 0, columnspan = 2)
    
    range_controls.grid(row=2, column = 0, rowspan = 2, pady= 10)
    Min_x.place(row = 0, column = 0)
    Max_x.place(row = 0, column = 1)
    Min_y.place(row = 1, column = 0)
    Max_y.place(row = 1, column = 1)
    
    spectrum_controls.grid(row = 2, column = 1, columnspan = 2, padx = 20 ,pady = 5)
    quantity.place(row = 0, column = 0)
    autobinning.place(row = 0, column =1)
    noOfBins.place(row=0, column =2)
    
    plot_options.grid(row = 3, column = 1, pady = 5)
    x_name.place(row =0 , column = 0)
    y_name.place(row = 0, column = 1)

    mevee_scaling.grid(row = 3,column = 2, padx = 15)
    a_const.place(row = 0, column = 0)
    b_const.place(row = 0, column = 1)
    
    scatterplot_button.grid(row = 4, column = 0, pady = 10)
    hist_button.grid(row = 4, column = 1, pady = 10)
    
    root.mainloop()
