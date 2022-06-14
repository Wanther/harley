from tkinter import *
from tkinter import ttk

HODE_TYPES = ('COMPEESSION', 'TENSION')

class ParameterPanel(ttk.LabelFrame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

        self.id = DoubleVar(self, 0.0)
        self.od = DoubleVar(self, 0.250)
        self.e = DoubleVar(self, 161000.00)
        self.initiation = IntVar(self, 2511)
        self.final = IntVar(self, 2718)
        self.loadingtime = DoubleVar(self, 1.20)
        self.holdingtime = DoubleVar(self, 600.00)
        self.stressRelaxCount = IntVar(self, 20)
        self.noiseCount = IntVar(self, 200)
        self.holdtype = StringVar(self, HODE_TYPES[0])
        self.fittingNum = IntVar(self, 600)
        self.fittingWindowsize = IntVar(self, 131)
        self.fittingPolyorder = IntVar(self, 2)

        for i in range(8):
            self.columnconfigure(i, weight=1)

        ttk.Label(self, text='ID:', anchor='e').grid(row=0, column=0, sticky=(E, W, S, N))
        idEntry = ttk.Entry(self, textvariable=self.id, state=['disabled'])
        idEntry.grid(row=0, column=1, sticky=(E, W, S, N))

        ttk.Label(self, text='OD:', anchor='e').grid(row=1, column=0, sticky=(E, W, S, N))
        odEntry = ttk.Entry(self, textvariable=self.od, state=['disabled'])
        odEntry.grid(row=1, column=1, sticky=(E, W, S, N))

        ttk.Label(self, text='Hold Type', anchor='e').grid(row=2, column=0, sticky=(E, W, S, N))
        self.holdtypeEntry = ttk.Combobox(self, textvariable=self.holdtype, values=HODE_TYPES, state=['readonly'])
        self.holdtypeEntry.grid(row=2, column=1, sticky=(E, W, S, N))

        ttk.Label(self, text='Noise Count', anchor='e').grid(row=3, column=0, sticky=(E, W, S, N))
        noiseCountEntry = ttk.Entry(self, textvariable=self.noiseCount, state=['disabled'])
        noiseCountEntry.grid(row=3, column=1, sticky=(E, W, S, N))

        ttk.Label(self, text='E:', anchor='e').grid(row=0, column=2, sticky=(E, W, S, N))
        eEntry = ttk.Entry(self, textvariable=self.e, state=['disabled'])
        eEntry.grid(row=0, column=3, sticky=(E, W, S, N))

        ttk.Label(self, text='Stress Relax Count:', anchor='e').grid(row=1, column=2, sticky=(E, W, S, N))
        stressRelaxCountEntry = ttk.Entry(self, textvariable=self.stressRelaxCount, state=['disabled'])
        stressRelaxCountEntry.grid(row=1, column=3, sticky=(E, W, S, N))

        ttk.Label(self, text='Initiation:', anchor='e').grid(row=0, column=4, sticky=(E, W, S, N))
        self.initiationEntry = ttk.Entry(self, textvariable=self.initiation)
        self.initiationEntry.grid(row=0, column=5, sticky=(E, W, S, N))

        ttk.Label(self, text='Final:', anchor='e').grid(row=1, column=4, sticky=(E, W, S, N))
        self.finalEntry = ttk.Entry(self, textvariable=self.final)
        self.finalEntry.grid(row=1, column=5, sticky=(E, W, S, N))

        ttk.Label(self, text='Loading Time:', anchor='e').grid(row=0, column=6, sticky=(E, W, S, N))
        loadingtimeEntry = ttk.Entry(self, textvariable=self.loadingtime, state=['disabled'])
        loadingtimeEntry.grid(row=0, column=7, sticky=(E, W, S, N))

        ttk.Label(self, text='Holding Time:', anchor='e').grid(row=1, column=6, sticky=(E, W, S, N))
        holdingtimeEntry = ttk.Entry(self, textvariable=self.holdingtime, state=['disabled'])
        holdingtimeEntry.grid(row=1, column=7, sticky=(E, W, S, N))

        ttk.Label(self, text='Fitting Num:', anchor='e').grid(row=2, column=2, sticky=(E, W, S, N))
        fittingNumEntry = ttk.Entry(self, textvariable=self.fittingNum, state=['disabled'])
        fittingNumEntry.grid(row=2, column=3, sticky=(E, W, S, N))

        ttk.Label(self, text='Fitting Window Size:', anchor='e').grid(row=2, column=4, sticky=(E, W, S, N))
        fittingNumEntry = ttk.Entry(self, textvariable=self.fittingWindowsize, state=['disabled'])
        fittingNumEntry.grid(row=2, column=5, sticky=(E, W, S, N))

        ttk.Label(self, text='Fitting Polyorder:', anchor='e').grid(row=2, column=6, sticky=(E, W, S, N))
        fittingNumEntry = ttk.Entry(self, textvariable=self.fittingPolyorder, state=['disabled'])
        fittingNumEntry.grid(row=2, column=7, sticky=(E, W, S, N))
    
    def setDisabled(self, disabled):
        stateStr = 'disabled' if disabled else '!disabled'
        self.initiationEntry.state([stateStr])
        self.finalEntry.state([stateStr])
        self.holdtypeEntry.state([stateStr])
    
    def getParameters(self):
        return dict(
            id=self.id.get(),
            od=self.od.get(),
            e=self.e.get(),
            initiation=self.initiation.get(),
            final=self.final.get(),
            loadingtime=self.loadingtime.get(),
            holdingtime=self.holdingtime.get(),
            stressRelaxCount=self.stressRelaxCount.get(),
            noiseCount=self.noiseCount.get(),
            holdtype=HODE_TYPES.index(self.holdtype.get()),
            fittingNum=self.fittingNum.get(),
            fittingWindowsize=self.fittingWindowsize.get(),
            fittingPolyorder=self.fittingPolyorder.get()
        )
