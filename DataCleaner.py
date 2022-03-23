import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd

button_font = ('arial', 13)
small_btn_font = ('arial', 10)
default_button_options = {'activebackground': 'white', 'bg': 'RoyalBlue3', 'relief': 'groove',
                          'activeforeground': 'RoyalBlue3', 'width': '16',
                          'fg': 'white', 'font': button_font, 'bd': 2}
another_button_options = {'activebackground': 'black', 'bg': 'springgreen2', 'relief': 'groove',
                          'activeforeground': 'springgreen2', 'width': '9',
                          'fg': 'black', 'font': small_btn_font, 'bd': 1}


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.get_column_window = None
        self.check_btn_vars = None
        self.numeric_df = None
        self.selected_columns = []
        self.df = pd.read_csv("C:/Users/rahul/Downloads/dataset.csv")

        screen_width = 1360
        screen_height = self.winfo_screenheight()

        self.resizable(False, False)
        self.geometry("%dx%d" % (screen_width, screen_height))
        self.title('Happy Data Cleaning')

        # to show dataframe
        dataset_frame = LabelFrame(self, text='DataFrame', border=0)
        dataset_frame.place(height=screen_height * 2 / 5, width=screen_width)
        self.tree_view = ttk.Treeview(dataset_frame)
        self.tree_view.place(relheight=1, relwidth=1)
        treescrolly = Scrollbar(dataset_frame, orient="vertical",
                                command=self.tree_view.yview)  # command means update the y-axis view of the widget
        treescrollx = Scrollbar(dataset_frame, orient="horizontal",
                                command=self.tree_view.xview)  # command means update the x-axis view of the widget
        self.tree_view.configure(xscrollcommand=treescrollx.set,
                                 yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
        treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x-axis with the Treeview widget
        treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y-axis with the Treeview widget
        self.show_dataset()

        # bottom Frame
        manipulate_button_frame = LabelFrame(self, border=0, text='Manipulate DataFrame', pady=10)
        btn_padding_x = 8
        btn_padding_y = 12
        Button(manipulate_button_frame, default_button_options, text='Delete NaN Rows', command=self.delete_columns) \
            .grid(row=0, column=0, padx=btn_padding_x, pady=btn_padding_y)
        Button(manipulate_button_frame, default_button_options, text='Delete Column', command=self.delete_column) \
            .grid(row=0, column=1, padx=btn_padding_x, pady=btn_padding_y)
        Button(manipulate_button_frame, default_button_options, text='Change Datatype') \
            .grid(row=0, column=2, padx=btn_padding_x, pady=btn_padding_y)
        Button(manipulate_button_frame, default_button_options, text='One-Hot Encode') \
            .grid(row=0, column=3, padx=btn_padding_x, pady=btn_padding_y)
        Button(manipulate_button_frame, default_button_options, text='Dummy') \
            .grid(row=0, column=4, padx=btn_padding_x, pady=btn_padding_y)
        Button(manipulate_button_frame, default_button_options, text='Dummy') \
            .grid(row=0, column=5, padx=btn_padding_x, pady=btn_padding_y)
        Button(manipulate_button_frame, default_button_options, text='Dummy') \
            .grid(row=0, column=6, padx=btn_padding_x, pady=btn_padding_y)
        Button(manipulate_button_frame, default_button_options, text='Dummy') \
            .grid(row=0, column=7, padx=btn_padding_x, pady=btn_padding_y)
        Button(manipulate_button_frame, default_button_options, text='Dummy') \
            .grid(row=1, column=0, padx=btn_padding_x, pady=btn_padding_y)
        Button(manipulate_button_frame, default_button_options, text='Dummy') \
            .grid(row=1, column=1, padx=btn_padding_x, pady=btn_padding_y)
        Button(manipulate_button_frame, default_button_options, text='Dummy') \
            .grid(row=1, column=2, padx=btn_padding_x, pady=btn_padding_y)
        Button(manipulate_button_frame, default_button_options, text='Dummy') \
            .grid(row=1, column=3, padx=btn_padding_x, pady=btn_padding_y)
        Button(manipulate_button_frame, default_button_options, text='Dummy') \
            .grid(row=1, column=4, padx=btn_padding_x, pady=btn_padding_y)
        Button(manipulate_button_frame, default_button_options, text='Dummy') \
            .grid(row=1, column=5, padx=btn_padding_x, pady=btn_padding_y)
        Button(manipulate_button_frame, default_button_options, text='Dummy') \
            .grid(row=1, column=6, padx=btn_padding_x, pady=btn_padding_y)
        Button(manipulate_button_frame, default_button_options, text='Dummy') \
            .grid(row=1, column=7, padx=btn_padding_x, pady=btn_padding_y)

        manipulate_button_frame.place(y=screen_height * 2 / 5, height=screen_height * 3 / 5, width=screen_width)

    def show_dataset(self):
        self.tree_view["column"] = list(self.df.columns)
        self.tree_view["show"] = "headings"
        for column in self.tree_view["columns"]:
            self.tree_view.heading(column, text=column)  # let the column heading = column name

        df_rows = self.df.to_numpy().tolist()  # turns the dataframe into a list of lists
        for row in df_rows:
            self.tree_view.insert("", "end", values=row)

    def get_numeric_columns(self):
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        self.numeric_df = self.df.select_dtypes(include=numerics)

        get_column_window = Toplevel(self)
        get_column_window.title('Select Columns')
        get_column_window.geometry('320x220')

    def delete_columns(self):
        self.select_columns()
        self.df.drop(self.selected_columns, inplace=True, axis=1)
        self.show_dataset()

    def select_columns(self):
        columns = self.df.columns
        total_columns = len(columns)
        print(total_columns)
        self.check_btn_vars = []
        for i in range(total_columns):
            self.check_btn_vars.append(IntVar())

        self.get_column_window = Toplevel(self)
        self.get_column_window.title('Select Columns')
        self.get_column_window.geometry('380x500')

        top_frame = LabelFrame(self.get_column_window, height=400, width=380)
        top_frame.pack()

        scrollbar = Scrollbar(top_frame, cursor='dot')
        scrollbar.pack(side=RIGHT, fill=Y)

        check_list = Text(top_frame, width=380)
        check_list.pack()

        select_button_list = []
        deselect_button_list = []

        for i in range(total_columns):
            container = LabelFrame(check_list)
            select_button_list.append(Button(container, another_button_options, text='SELECT', cursor="crosshair")
                                      .grid(row=0, column=0))
            Label(container, text=columns[i].upper(), width=25, fg='gray13').grid(row=0, column=1)
            deselect_button_list.append(Button(container, another_button_options, text='DE-SELECT', state=DISABLED,
                                               cursor="crosshair")
                                        .grid(row=0, column=2))
            container.pack(fill=X)

            check_list.window_create('end', window=container)
            check_list.insert('end', '\n')

        check_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=check_list.yview)
        check_list.configure(state='disabled')

        bottom_frame = LabelFrame(self.get_column_window)
        Button(bottom_frame, default_button_options, text='Done', command=self.get_selected_cols).pack(side=LEFT)
        Button(bottom_frame, default_button_options, text='Close', command=self.get_column_window.destroy).pack(
            side=LEFT)
        bottom_frame.pack(pady=30)

    # enable deselect btn  and disable select btn
    def change_state_enable(self, idx, select_btn_list, deselect_btn_list):
        pass

    def change_state_disable(self, idx, select_btn_list, deselect_btn_list):
        pass

    def get_selected_cols(self):
        self.selected_columns = []
        columns = self.df.columns

        for i, var in enumerate(self.check_btn_vars):
            if var.get() == 1:
                self.selected_columns.append(columns[i])

        print(self.selected_columns)

    def delete_column(self):
        pass


main_window = MainWindow()
main_window.mainloop()
