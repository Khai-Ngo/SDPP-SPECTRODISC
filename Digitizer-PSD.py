from tkinter import *
from tkinter import filedialog

class labelledFields:
    def __init__(self, frame, label, padx = 5, pady = 5, width = 50, borderwidth = 5):
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
    def __init__(self, frame, label, padx = 5, pady = 5, width = 50, borderwidth = 5):
        labelledFields.__init__(self, frame, label, padx = 5, pady = 5, width = width, borderwidth = borderwidth)
        self.Button = Button (self.Frame, text = "...", command = self.open_file)
    def open_file(self):
        filename = filedialog.askopenfilename(initialdir = "/", title = "Select a text file", filetypes=(("Text files","*.txt"), ("All files","*.*")))
        self.Field.delete(0, END)
        self.Field.insert(0, filename)
    def place(self, row, column, columnspan = 1, txtboxspan = 1):
        labelledFields.place(self, row = row, column = column, columnspan = columnspan, txtboxspan = txtboxspan)
        self.Button.grid(row = 0, column = 1+txtboxspan)
if __name__ == '__main__':
    # Create the window
    root = Tk()
    root.title("Digitizer PSD analysis")
    # Create widgets
    titleLabel = Label(root, text = "This program takes in output from scintillator-analysis.py and perform post analysis", padx = 10, pady=10)
    inFile = fileDialogButtons(root, label = 'Input file:', width = 125)
    range_controls = LabelFrame(root, text = 'Range controls', padx = 5, pady =5)
    Min_x = labelledFields(range_controls, label = 'Minimum PH', width = 10)
    Max_x = labelledFields(range_controls, label = 'Maximum PH', width = 10)
    Min_y = labelledFields(range_controls, label = 'Minimum PSD', width = 10)
    Max_y = labelledFields(range_controls, label = 'Minimum PSD', width = 10)
    spectrum_controls = LabelFrame(root, text = 'Further histogram building controls', padx = 5, pady = 5)
    quantity = labelledFields(spectrum_controls, label = 'Quantity', width = 10)
    autobinning = labelledFields(spectrum_controls, label = 'Auto-binning?', width = 10)
    noOfBins = labelledFields(spectrum_controls, label = 'Number of bins', width = 10)    
    # PLace widgets
    titleLabel.grid(row = 0, column = 0)
    inFile.place(row = 1, column = 0, columnspan = 2)
    range_controls.grid(row=2, column = 0, pady= 10)
    Min_x.place(row = 0, column = 1)
    Max_x.place(row = 0, column = 2)
    Min_y.place(row = 1, column = 1)
    Max_y.place(row = 1, column = 2)
    spectrum_controls.grid(row = 2, column = 1)
    quantity.place(row = 0, column = 0)
    autobinning.place(row = 0, column =1)
    noOfBins.place(row=0, column =2)
    root.mainloop()
