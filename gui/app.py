from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from .creep import CreepPage


class Application(Tk):

    def __init__(self, title=None, screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        if title:
            self.title(title)

        self.option_add('*tearOff', FALSE)

        self.__create_menubar()
        self.create_page()


    def start(self):
        self.mainloop()
    
    def exit(self):
        self.destroy()
    
    def __create_menubar(self):
        menubar = Menu(self)

        menu = Menu(menubar)
        menu.add_command(label='Exit', command=self.exit)
        menubar.add_cascade(menu=menu, label='File')

        menu = Menu(menubar)
        menu.add_command(label='About', command=self.show_about)
        menubar.add_cascade(menu=menu, label='About')

        self['menu'] = menubar

    def create_page(self):
        CreepPage(self).pack(fill=BOTH, expand=YES)

    def show_about(self):
        messagebox.showinfo(title='About', message='Application Name, version 1.0.0')


if __name__ == '__main__':
    Application('Application Name').start()