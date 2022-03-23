import tkinter as tk
from tkinter import *
from tkinter import ttk
from functools import partial
from HomeScreen import df

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
        self.undo_stack = []
        self.redo_stack = []
        self.right_btn_list = None
        self.left_btn_list = None
        self.get_column_window = None
        self.check_btn_vars = None
        self.numeric_df = None
        self.selected_columns = []
        self.df = df
        self.original_df = self.df.copy()
        self.columns = self.df.columns

        screen_width = 1360
        screen_height = self.winfo_screenheight()

        self.resizable(False, False)
        self.geometry("%dx%d" % (screen_width, screen_height))
        self.title('Happy Data Cleaning')

        # label for showing rows x columns
        self.row_col_display = Label(fg='gray7')
        self.row_col_display.place(x=1360//2, y=5)

        # to show dataframe
        dataset_frame = LabelFrame(self, text='DataFrame', border=0)
        dataset_frame.place(y=20, height=screen_height * 2 / 5, width=screen_width)
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
        Button(manipulate_button_frame, default_button_options, text='Delete NaN Rows', command=self.remove_nans) \
            .grid(row=0, column=0, padx=btn_padding_x, pady=btn_padding_y)
        Button(manipulate_button_frame, default_button_options, text='Delete Column', command=self.delete_cols) \
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
        Button(manipulate_button_frame, default_button_options, text='Redo', command=self.redo) \
            .grid(row=1, column=5, padx=btn_padding_x, pady=btn_padding_y)
        Button(manipulate_button_frame, default_button_options, text='Undo', command=self.undo) \
            .grid(row=1, column=6, padx=btn_padding_x, pady=btn_padding_y)
        Button(manipulate_button_frame, default_button_options, text='Original Dataset', command=self.show_original) \
            .grid(row=1, column=7, padx=btn_padding_x, pady=btn_padding_y)

        manipulate_button_frame.place(y=screen_height * 2 / 5 + 20, height=screen_height * 3 / 5, width=screen_width)

    def save_state(self):
        self.undo_stack.append(self.df.copy())

    def redo(self):
        if len(self.redo_stack):
            self.undo_stack.append(self.df)
            self.df = self.redo_stack[-1]
            self.redo_stack.pop()
            self.show_dataset()

    def undo(self):
        if len(self.undo_stack):
            self.redo_stack.append(self.df)
            self.df = self.undo_stack[-1]
            self.undo_stack.pop()
            self.show_dataset()

    def show_original(self):
        self.undo_stack.append(self.df)
        self.df = self.original_df
        self.show_dataset()

    def clear_all(self):
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)

    def show_dataset(self):
        self.clear_all()
        num_rows, num_cols = self.df.shape
        self.row_col_display['text'] = '{}x{}'.format(num_rows, num_cols)
        self.tree_view["column"] = list(self.df.columns)
        self.tree_view["show"] = "headings"
        for column in self.tree_view["columns"]:
            self.tree_view.heading(column, text=column)  # let the column heading = column name
        df_rows = self.df.to_numpy().tolist()  # turns the dataframe into a list of lists
        for row in df_rows:
            self.tree_view.insert("", "end", values=row)

    def delete_cols(self):
        self.selected_columns = []

        self.get_column_window = Toplevel(self)
        self.get_column_window.title('Select Columns')
        self.get_column_window.geometry('380x460')

        total_columns = len(self.columns)

        top_list_frame = LabelFrame(self.get_column_window, height=400, width=380)

        scroll_bar = Scrollbar(top_list_frame)
        scroll_bar.pack(side=RIGHT, fill=Y)

        check_list = Text(top_list_frame)
        check_list.pack(fill=X)

        self.left_btn_list = [Button() for i in range(total_columns)]
        self.right_btn_list = [Button() for i in range(total_columns)]

        for i in range(total_columns):
            container = LabelFrame(check_list)
            self.left_btn_list[i] = Button(container, another_button_options, text='Select', width=10, cursor='hand2',
                                           command=partial(self.change_state, i, 0))
            self.left_btn_list[i].pack(side=LEFT)
            Label(container, text=self.columns[i].upper(), width=24).pack(side=LEFT)
            self.right_btn_list[i] = Button(container, another_button_options, text='Remove', width=10, cursor='hand2',
                                            state=DISABLED, command=partial(self.change_state, i, 1))
            self.right_btn_list[i].pack(side=LEFT)
            container.pack(fill=X)

            check_list.window_create('end', window=container)
            check_list.insert('end', '\n')

        check_list.config(yscrollcommand=scroll_bar.set)
        scroll_bar.config(command=check_list.yview)
        check_list.configure(state='disabled')

        top_list_frame.pack()

        bottom_button_frame = LabelFrame(self.get_column_window)
        Button(bottom_button_frame, default_button_options, text='Delete', bg='red3', command=partial(self.delete_cols_helper)).pack(side=LEFT)
        bottom_button_frame.pack(pady=14)

    def change_state(self, idx, right):
        if right == 1:
            self.selected_columns.remove(self.columns[idx])
            self.left_btn_list[idx]['state'] = NORMAL
            self.right_btn_list[idx]['state'] = DISABLED
        else:
            self.selected_columns.append(self.columns[idx])
            self.left_btn_list[idx]['state'] = DISABLED
            self.right_btn_list[idx]['state'] = NORMAL

    def delete_cols_helper(self):
        self.save_state()
        self.df.drop(self.selected_columns, inplace=True, axis=1)
        self.columns = self.df.columns
        self.selected_columns = []
        self.get_column_window.destroy()
        self.show_dataset()

    def remove_nans(self):
        self.save_state()
        self.df.dropna(inplace=True)
        self.show_dataset()

