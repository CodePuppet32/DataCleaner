from HomeScreen import *
from MainScreen import *

welcomeWindow = WelcomeWindow()
welcomeWindow.mainloop()

mainWindow = MainWindow()
if mainWindow.df.shape != (0, 0):
    mainWindow.mainloop()

