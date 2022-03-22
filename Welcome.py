import tkinter as tk

class WelcomeWindow(tk.Tk):
    def __int__(self):
        super().__init__()


        self.geometry('800x600')
        self.title('All in One Data Cleaner')



if __name__ == "__main__":
    welcomeWindow = WelcomeWindow()
    welcomeWindow.mainloop()