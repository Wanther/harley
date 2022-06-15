import os

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk
)
from matplotlib.figure import Figure

from creep.CreepA709 import CreepA709

class CreepPage(ttk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.selected_filename = StringVar(self)

        self.Temperature = IntVar(self, 816)
        self.N = IntVar(self, 8000)
        self.C = DoubleVar(self, 14.9249760029308)
        self.a0 = DoubleVar(self, 26139.4634995320)
        self.a1 = DoubleVar(self, -2341.98112181595)
        self.a2 = DoubleVar(self, -739.1914468118)

        self.analyzer = None
        self.result = None

        self.__create_file_chose_frame()
        self.__create_parameter_frame()
        self.__create_action_buttons()
        self.__create_result_frame()
    
    def destroy(self):
        self.result = None
        self.analyzer = None
        return super().destroy()
        
    
    def __create_file_chose_frame(self):
        file_choose_frame = ttk.LabelFrame(self, text='Choose Data File')
        file_choose_frame.pack(fill=X)
        file_choose_label = ttk.Label(file_choose_frame, textvariable=self.selected_filename, cursor='hand2')
        file_choose_label.bind('<Button-1>', self.__choose_file)
        file_choose_label.pack(fill=X, ipady=8, padx=8)
    
    def __create_parameter_frame(self):
        parameter_frame = ttk.LabelFrame(self, text='Parameters')
        parameter_frame.pack(fill=X, ipadx=8, ipady=8)
        for i in range(6):
            parameter_frame.columnconfigure(i, weight=1)

        ttk.Label(parameter_frame, text='Temperature:', anchor=E).grid(row=0, column=0, sticky=(E, W, S, N))
        self.TemperatureEntry = ttk.Entry(parameter_frame, textvariable=self.Temperature)
        self.TemperatureEntry.grid(row=0, column=1, sticky=(E, W, S, N))

        ttk.Label(parameter_frame, text='N:', anchor=E).grid(row=0, column=2, sticky=(E, W, S, N))
        self.NEntry = ttk.Entry(parameter_frame, textvariable=self.N)
        self.NEntry.grid(row=0, column=3, sticky=(E, W, S, N))

        ttk.Label(parameter_frame, text='C:', anchor=E).grid(row=0, column=4, sticky=(E, W, S, N))
        self.CEntry = ttk.Entry(parameter_frame, textvariable=self.C)
        self.CEntry.grid(row=0, column=5, sticky=(E, W, S, N))

        ttk.Label(parameter_frame, text='a0:', anchor=E).grid(row=1, column=0, sticky=(E, W, S, N))
        self.a0Entry = ttk.Entry(parameter_frame, textvariable=self.a0)
        self.a0Entry.grid(row=1, column=1, sticky=(E, W, S, N))

        ttk.Label(parameter_frame, text='a1:', anchor=E).grid(row=1, column=2, sticky=(E, W, S, N))
        self.a1Entry = ttk.Entry(parameter_frame, textvariable=self.a1)
        self.a1Entry.grid(row=1, column=3, sticky=(E, W, S, N))

        ttk.Label(parameter_frame, text='a2:', anchor=E).grid(row=1, column=4, sticky=(E, W, S, N))
        self.a2Entry = ttk.Entry(parameter_frame, textvariable=self.a2)
        self.a2Entry.grid(row=1, column=5, sticky=(E, W, S, N))
    
    def __create_result_frame(self):
        self.result_frame = ttk.LabelFrame(self, text='Result')
        self.result_frame.pack(fill=BOTH, expand=YES)

        fig = Figure()

        fig.add_subplot()

        self.canvas = FigureCanvasTkAgg(fig, master=self.result_frame)
        self.canvas.draw()

        toolbar = NavigationToolbar2Tk(self.canvas, self.result_frame)
        toolbar.update()

        toolbar.pack(side=TOP)

        ttk.Button(toolbar, text='CSV', command=self.__export_to_csv).pack(fill=Y, side=LEFT)

        self.canvas.get_tk_widget().pack(fill=BOTH, expand=YES)
    
    def __create_action_buttons(self):
        self.start_button = ttk.Button(self, text='START', command=self.__start_analyze)
        self.start_button.pack(fill='x', ipady=8)

    def __choose_file(self, *args):
        filename = filedialog.askopenfilename(filetypes=[('Data File', '*.csv')])
        if filename:
            self.selected_filename.set(filename)
    
    def __export_to_csv(self):
        if self.analyzer and self.result:
            sample_name = os.path.basename(self.selected_filename.get())
            sample_name = os.path.splitext(sample_name)[0]
            default_save_file_name = '{}_FittingCurve.csv'.format(sample_name)

            save_file_name = filedialog.asksaveasfilename(initialfile=default_save_file_name, confirmoverwrite=True, defaultextension='.csv', filetypes=[('Result File', '*.csv')])
            if save_file_name:
                self.analyzer.export_csv(self.result, save_file_name)
        else:
            messagebox.showerror(title='Error', message='Analyze Data First, Please Click "START" Button')
        
    
    def __start_analyze(self):
        try:
            self.analyzer = CreepA709(
                Temperature=self.Temperature.get(),
                N = self.N.get(),
                C = self.C.get(),
                a0 = self.a0.get(),
                a1 = self.a1.get(),
                a2 = self.a2.get()
            )
            data = self.analyzer.load_data(self.selected_filename.get())
            self.result = self.analyzer.calculate(data)

            sample_name = os.path.basename(self.selected_filename.get())
            sample_name = os.path.splitext(sample_name)[0]
            
            # Clear old points/lines on Canvas
            self.canvas.figure.axes[0].clear()
            # Draw fresh image
            self.analyzer.draw_in_axes(sample_name, data, self.result, self.canvas.figure.axes[0])
            # Need redraw to display Changes
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror(title='Error', message=e)