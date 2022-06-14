from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from demopage import DemoPage


class Application(Tk):

    def __init__(self, title=None, screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        if title:
            self.title(title)

        self.option_add('*tearOff', FALSE)

        self.createPage()


    def start(self):
        self.mainloop()
    
    def exit(self):
        self.destroy()
    
    def __createMenuBar(self):
        menubar = Menu(self)

        menu = Menu(menubar)
        menu.add_command(label='Exit', command=self.exit)
        menubar.add_cascade(menu=menu, label='File')

        menu = Menu(menubar)
        menu.add_command(label='About', command=self.showAbout)
        menubar.add_cascade(menu=menu, label='About')

        self['menu'] = menubar

    def createPage(self):
        self.__createMenuBar()
        DemoPage(self).pack(fill='x')

    def showAbout(self):
        messagebox.showinfo(title='About', message='Application Name, version 1.0.0')


if __name__ == '__main__':
    Application('Application Name').start()