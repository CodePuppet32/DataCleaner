import os
import tkinter as tk
from tkinter import ttk, filedialog



class WelcomeWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        # the title
        self.title('AIO data cleaner')
        # geometry width x height
        self.geometry('400x280')
        # background color
        self.configure(bg='#99ccff')

        # welcome label
        self.welcome_label = tk.Label(self, text='\nThank you for using our software\n We hope you like it.\n\n',
                                      bg='#99ccff', font=('Arial', 16))
        self.welcome_label.pack()

        # data label
        self.dataset_location_label = tk.Label(self, text='Please pick your dataset', font=('Arial', 12), bg='#99ccff')
        self.dataset_location_label.pack()

        # dataset pick button
        self.pick_button = tk.Button(self, text='Pick Dataset', command=self.pick_dataset, bg='#ffd966')
        self.pick_button.pack()

        '''# dataset name label
        self.dataset_name_label = tk.Label(self, text='', font=('Arial', 10), bg='#99ccff', padx=2, pady=2)
        self.dataset_name_label.pack()'''

    # dataset picker function
    def pick_dataset(self):
        global dataset_path
        self.dataset = filedialog.askopenfile(mode='r', filetypes=[('CSV files', '*.csv')])
        if self.dataset:
            dataset_path = os.path.abspath(self.dataset.name)
            self.destroy()
            '''self.dataset_name_label['text'] = str(self.dataset_path)
            self.dataset_name_label['bg'] = '#80ffff'''


welcome = WelcomeWindow()
welcome.mainloop()