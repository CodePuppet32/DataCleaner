import tkinter as tk
from tkinter import *
from tkinter import ttk
from functools import partial
import pandas as pd
from tkinter import messagebox
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.impute import SimpleImputer

button_font = ('arial', 13)
small_btn_font = ('arial', 10)
default_text_font = ('Courier ', 10)
default_text_font_bold = ('Courier ', 10, 'bold')


default_button_options = {'activebackground': 'white', 'bg': 'RoyalBlue3', 'relief': 'groove',
                          'activeforeground': 'RoyalBlue3', 'width': '16',
                          'fg': 'white', 'font': button_font, 'bd': 2}

another_button_options = {'activebackground': 'black', 'bg': 'springgreen2', 'relief': 'groove',
                          'activeforeground': 'springgreen2', 'width': '9',
                          'fg': 'black', 'font': small_btn_font, 'bd': 1}


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.one_hot_encode_window = None
        self.impute_window = None
        self.change_datatype_window = None
        self.undo_stack = []
        self.redo_stack = []
        self.right_btn_list = None
        self.left_btn_list = None
        self.get_column_window = None
        self.check_btn_vars = None
        self.numeric_df = None
        self.selected_columns = []
        self.df = pd.read_csv("C:/Users/rahul/Downloads/dataset.csv")
        self.original_df = self.df.copy()
        self.columns = self.df.columns

        screen_width = 1360
        screen_height = self.winfo_screenheight()

        self.resizable(False, False)
        self.geometry("%dx%d" % (screen_width, screen_height))
        self.title('Happy Data Cleaning')

        # label for showing rows x columns
        self.row_col_display = Label(fg='gray7')
        self.row_col_display.place(x=1360 // 2, y=5)

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
        Button(manipulate_button_frame, default_button_options, text='Change Datatype', command=self.change_dtype) \
            .grid(row=0, column=2, padx=btn_padding_x, pady=btn_padding_y)
        Button(manipulate_button_frame, default_button_options, text='One-Hot Encode', command=self.one_hot_encode) \
            .grid(row=0, column=3, padx=btn_padding_x, pady=btn_padding_y)
        Button(manipulate_button_frame, default_button_options, text='Impute', command=self.impute) \
            .grid(row=0, column=4, padx=btn_padding_x, pady=btn_padding_y)
        Button(manipulate_button_frame, default_button_options, text='Co-relation HeatMap', command=self.correlation_map) \
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
        self.show_original_btn = Button(manipulate_button_frame, default_button_options, text='Original Dataset', command=self.show_original)
        self.show_original_btn.grid(row=1, column=7, padx=btn_padding_x, pady=btn_padding_y)

        manipulate_button_frame.place(y=screen_height * 2 / 5 + 20, height=screen_height * 3 / 5, width=screen_width)

    def correlation_map(self):
        corr = self.df.corr()
        for col in corr.columns:
            total_row = corr.shape[0]
            total_na = corr[col].isna().sum()
            if total_na == total_row:
                corr.drop(col, inplace=True, axis=1)
                corr.drop(col, inplace=True, axis=0)
        sns.heatmap(corr, center=0)
        plt.show()

    def one_hot_encode(self):
        category_cols = self.df.select_dtypes(include='O').keys()

        if len(category_cols) == 0:
            messagebox.showinfo('Info!', 'No Categorical Column Found')
            return

        self.one_hot_encode_window = Toplevel(self)
        self.one_hot_encode_window.title('One Hot Encoder')
        width = 360
        height = min(len(category_cols) * 30 + 60, 460)
        self.one_hot_encode_window.geometry('{}x{}'.format(width, height))
        self.one_hot_encode_window.resizable(False, False)

        top_list_frame = LabelFrame(self.one_hot_encode_window, width=width)
        scroll_bar = Scrollbar(top_list_frame)
        scroll_bar.pack(side=RIGHT, fill=Y)

        check_list = Text(top_list_frame, height=height-50)
        check_list.pack(fill=X)

        self.left_btn_list = [Button for _ in range(len(category_cols))]
        self.right_btn_list = [Button for _ in range(len(category_cols))]

        for i in range(len(category_cols)):
            container = LabelFrame(check_list)
            self.left_btn_list[i] = Button(container, another_button_options, text='Select', cursor='hand2',
                                           command=partial(self.change_state, i, 0, category_cols))
            self.left_btn_list[i].pack(side=LEFT)
            Label(container, text=category_cols[i].upper(), width=24).pack(side=LEFT)
            self.right_btn_list[i] = Button(container, another_button_options, text='Remove', cursor='hand2',
                                            state=DISABLED, command=partial(self.change_state, i, 1, category_cols))
            self.right_btn_list[i].pack(side=LEFT)
            container.pack(fill=X)

            check_list.window_create('end', window=container)
            check_list.insert('end', '\n')

        check_list.config(yscrollcommand=scroll_bar.set)
        scroll_bar.config(command=check_list.yview)
        check_list.configure(state='disabled')

        top_list_frame.pack()

        bottom_button_frame = LabelFrame(self.one_hot_encode_window)
        Button(bottom_button_frame, default_button_options, text='Encode', bg='red3',
               command=self.one_hot_encode_helper).pack(side=LEFT)
        bottom_button_frame.place(relx=.5, y=height-25, anchor=CENTER)

    def one_hot_encode_helper(self):
        self.one_hot_encode_window.destroy()
        self.save_state()
        encoder = preprocessing.OneHotEncoder()
        for i, col in enumerate(self.selected_columns):
            encoded_series = encoder.fit_transform(self.df[col].values.reshape(-1, 1)).toarray().reshape(-1)
            self.df[col] = pd.Series(encoded_series)
        self.show_dataset()
        self.selected_columns = []

    def impute(self):
        numerical_data_types = ['int64', 'float64']
        numerical_cols = []
        for col in self.columns:
            if self.df[col].dtype in numerical_data_types:
                numerical_cols.append(col)
        nan_cols = [col for col in self.df.columns if self.df[col].isnull().any()]

        if len(nan_cols) == 0:
            messagebox.showinfo('Info!', 'No Numerical Column has NaN value')
            return

        options = ['none', 'mean', 'median', 'most_frequent']
        clicked_arr = [StringVar() for _ in range(len(nan_cols))]
        for var in clicked_arr:
            var.set(options[0])

        self.impute_window = Toplevel(self)
        self.impute_window.title('Imputer')
        width = 380
        height = min(len(nan_cols) * 30 + 80, 460)
        self.impute_window.geometry('{}x{}'.format(width, height))

        top_list_frame = LabelFrame(self.impute_window, border=0)
        scroll_bar = Scrollbar(top_list_frame)
        scroll_bar.pack(side=RIGHT, fill=Y)
        check_list = Text(top_list_frame, height=height/21)
        check_list.pack(fill=X)

        container = LabelFrame(check_list, border=0)
        Label(container, text='COLUMN', width=34).pack(side=LEFT)
        Label(container, text='STRATEGY', width=16).pack(side=LEFT)
        container.pack(fill=X)
        check_list.window_create('end', window=container)
        check_list.insert('end', '\n')

        for i in range(len(nan_cols)):
            container = LabelFrame(check_list, border=0)
            cur_col = nan_cols[i]
            Label(container, text=cur_col.upper(), width=29, font=default_text_font_bold).pack(side=LEFT)
            option_menu = OptionMenu(container, clicked_arr[i], *options)
            option_menu.configure(width=10, font=default_text_font)
            option_menu.pack(side=LEFT, fill=X)
            container.pack(fill=X)

            check_list.window_create('end', window=container)
            check_list.insert('end', '\n')

        check_list.config(yscrollcommand=scroll_bar.set)
        scroll_bar.config(command=check_list.yview)
        check_list.configure(state='disabled')
        top_list_frame.pack()
        Button(self.impute_window, another_button_options, text='Impute',
               command=partial(self.impute_helper, clicked_arr, nan_cols)).place(relx=.5, y=height - 25, anchor=CENTER)

    def impute_helper(self, arr_list, col_list):
        self.impute_window.destroy()

        for i, col in enumerate(col_list):
            strategy = arr_list[i].get()
            if strategy != 'none':
                imputer = SimpleImputer(strategy=strategy)
                self.df[col] = imputer.fit_transform(self.df[col].values.reshape(-1, 1))

        self.save_state()
        self.show_dataset()

    def change_dtype(self):
        data_types = ['object', 'int64', 'float64', 'bool', 'datetime64', 'timedelta[ns]', 'category']

        clicked_arr = [StringVar() for i in range(len(self.columns))]
        for i in range(len(self.columns)):
            clicked_arr[i].set(self.df[self.columns[i]].dtype)

        self.change_datatype_window = Toplevel(self)
        self.change_datatype_window.title('Change Datatype')
        self.change_datatype_window.geometry('480x460')

        top_list_frame = LabelFrame(self.change_datatype_window)

        scroll_bar = Scrollbar(top_list_frame)
        scroll_bar.pack(side=RIGHT, fill=Y)

        check_list = Text(top_list_frame)
        check_list.pack(fill=X)

        container = LabelFrame(check_list, border=0)
        Label(container, text='Column', width=44).pack(side=LEFT)
        Label(container, text='Change to Dtype', width=22).pack(side=LEFT)
        container.pack(fill=X)
        check_list.window_create('end', window=container)
        check_list.insert('end', '\n')

        for i in range(len(self.columns)):
            container = LabelFrame(check_list, border=0)
            cur_col = self.columns[i]
            Label(container, text=cur_col.upper(), width=42, font=default_text_font_bold).pack(side=LEFT)
            option_menu = OptionMenu(container, clicked_arr[i], *data_types)
            option_menu.configure(width=10, font=default_text_font)
            option_menu.pack(side=LEFT, fill=X)
            container.pack(fill=X)

            check_list.window_create('end', window=container)
            check_list.insert('end', '\n')
        check_list.config(yscrollcommand=scroll_bar.set)
        scroll_bar.config(command=check_list.yview)
        check_list.configure(state='disabled')
        top_list_frame.pack()
        Button(self.change_datatype_window, another_button_options, text='Change',
               command=partial(self.change_dtype_helper, clicked_arr)).pack(pady=20)

    def change_dtype_helper(self, arr_list):
        self.save_state()
        for i, column in enumerate(self.columns):
            cur_col_dtype = self.df[self.columns[i]].dtype
            if arr_list[i].get() != cur_col_dtype:
                try:
                    self.df[self.columns[i]] = self.df[self.columns[i]].astype(arr_list[i].get())
                except Exception as e:
                    messagebox.showinfo('Error', 'While Changing type of {}\n{}\nException Occurred\n'
                                                 'Other Columns Type has been changed'
                                        .format(self.columns[i].upper(), e))

    def save_state(self):
        # first condition makes sure that the current dataframe has some changes made to it
        if len(self.undo_stack) and self.undo_stack[-1].equals(self.df):
            return

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
        if not self.df.equals(self.original_df):
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

        self.left_btn_list = [None for i in range(total_columns)]
        self.right_btn_list = [None for i in range(total_columns)]

        for i in range(total_columns):
            container = LabelFrame(check_list)
            self.left_btn_list[i] = Button(container, another_button_options, text='Select', width=10, cursor='hand2',
                                           command=partial(self.change_state, i, 0, self.columns))
            self.left_btn_list[i].pack(side=LEFT)
            Label(container, text=self.columns[i].upper(), width=24).pack(side=LEFT)
            self.right_btn_list[i] = Button(container, another_button_options, text='Remove', width=10, cursor='hand2',
                                            state=DISABLED, command=partial(self.change_state, i, 1, self.columns))
            self.right_btn_list[i].pack(side=LEFT)
            container.pack(fill=X)

            check_list.window_create('end', window=container)
            check_list.insert('end', '\n')

        check_list.config(yscrollcommand=scroll_bar.set)
        scroll_bar.config(command=check_list.yview)
        check_list.configure(state='disabled')

        top_list_frame.pack()

        bottom_button_frame = LabelFrame(self.get_column_window)
        Button(bottom_button_frame, default_button_options, text='Delete', bg='red3',
               command=partial(self.delete_cols_helper)).pack(side=LEFT)
        bottom_button_frame.pack(pady=14)

    def change_state(self, idx, right, cols):
        if right == 1:
            self.selected_columns.remove(cols[idx])
            self.left_btn_list[idx]['state'] = NORMAL
            self.right_btn_list[idx]['state'] = DISABLED
        else:
            self.selected_columns.append(cols[idx])
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


mwin = MainWindow()
mwin.mainloop()
