from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from parameterpanel import ParameterPanel

HOLD_TYPES = ('COMPEESSION', 'TENSION')

class DemoPage(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

        self.selectedFilename = None
        self.progress = DoubleVar(self, 0.0)

        self['padding'] = (8, 8, 8, 8)

        # Top File Choose Area
        self.__addFileChoosePanel()

        # Parameters Display
        self.parameterPanel = ParameterPanel(self, text='Parameters')
        self.parameterPanel.pack(fill='x')

        # Result(s)
        self.resultFrame = ttk.LabelFrame(self, text='Result(s)', height=480)
        self.resultFrame.pack(fill='both', expand=1)

        # Status Bar/Progress Bar
        self.progressbar = ttk.Progressbar(self, orient=HORIZONTAL, mode='determinate', variable=self.progress)
        self.progressbar.pack(fill='x')

        self.startButton = ttk.Button(self, text='Start', command=self.startAnalysis)
        self.startButton.pack(fill='x', side='bottom')

    def __addFileChoosePanel(self):
        fileChooseFrame = ttk.LabelFrame(self, text='Data File')
        fileChooseFrame.pack(fill='x')
        self.selectedFilename = StringVar(fileChooseFrame, 'Click Me To Choose A File')
        fileChooseLabel = ttk.Label(fileChooseFrame, textvariable=self.selectedFilename, cursor='hand2')
        fileChooseLabel.pack(fill='x')
        fileChooseLabel.bind('<Button-1>', self.chooseFile)

    def startAnalysis(self):
        self.parameterPanel.setDisabled(True)
        self.startButton.state(['disabled'])

        self.simulateProgress()
    
    def chooseFile(self, *args):
        filename = filedialog.askopenfilename()
        if filename:
            self.selectedFilename.set(filename)
    
    def simulateProgress(self):
        progress = self.progress.get()
        if progress < 100.0:
            self.progress.set(progress + 1)
            self.after(20, self.simulateProgress)
        else:
            self.progress.set(0.0)
            self.onComplete()
    
    def onComplete(self):
        self.parameterPanel.setDisabled(False)
        self.startButton.state(['!disabled'])
        messagebox.showinfo(title='Tips', message='Process Complete!')

        for child in self.resultFrame.winfo_children():
            child.forget()
        
        params = self.parameterPanel.getParameters()

        params = '\n'.join('%s=%s' % (k, v) for (k, v) in params.items())
        
        ttk.Label(self.resultFrame, text=params).pack(fill='both')
