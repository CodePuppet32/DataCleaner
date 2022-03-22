import tkinter as tk


class WelcomeWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('800x600')
        self.title('All in One Data Cleaner')
        

welcomeWindow = WelcomeWindow()
welcomeWindow.mainloop()
