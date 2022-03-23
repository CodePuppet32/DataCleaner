import tkinter as tk
from tkinter import *


class Test(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('1000x600')

        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)

        checklist = Text(self, width=20, background='red')
        checklist.pack(fill=X)

        for i in range(20):
            container = LabelFrame(checklist)
            Label(container, text='Left').pack(side=LEFT, fill=X)
            Button(container, text='Button').pack(side=LEFT, fill=X)
            Label(container, text='Right').pack(side=LEFT, fill=X)
            container.pack(fill=X)

            checklist.window_create('end', window=container)
            checklist.insert('end', '\n')

        checklist.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=checklist.yview)
        checklist.configure(state=DISABLED)


test = Test()
test.mainloop()
