from tkinter import *
from tkinter import messagebox, simpledialog, font, ttk
from PIL import ImageTk, Image
import sqlite3 as sql
from users import *

class User_Home:
    def __init__(self, root):
        self.root = root

    def build_userhome(self):
        usracc_frame = LabelFrame(self.root)
        usrstat_frame = LabelFrame(self.root)
        usrstat_label = Label(usrstat_frame, text='This is the stat frame')
        usrlog_frame = LabelFrame(self.root)
        usrlog_label = Label(usrlog_frame, text='This is the log frame')
        account_columns = ('id', 'account_name', 'account_type')
        account_table = ttk.Treeview(usracc_frame, columns=account_columns, show='headings')
        account_table.heading('id', text='#')
        account_table.heading('account_name', text='Account Name')
        account_table.heading('account_type', text='Account Type')
        account_table.column('id', width=50, anchor=CENTER)
        account_table.column('account_name', width=200)
        account_table.column('account_type', width=100)

        usracc_frame.grid(row=0, column=0, sticky=NSEW)
        self.root.grid_columnconfigure(0, weight=1)
        usracc_frame.grid_columnconfigure(0, weight=1)
        usracc_frame.grid_rowconfigure(0, weight=1)
        account_table.grid(row=0, column=0, sticky=NSEW)
        usrstat_frame.grid(row=0, column=1, sticky=NSEW)
        self.root.grid_columnconfigure(1, weight=1)
        usrstat_label.grid(row=0, column=0)
        usrlog_frame.grid(row=1, column=0, columnspan=2, sticky=NSEW)
        self.root.grid_rowconfigure(0, weight=2)
        self.root.grid_rowconfigure(1, weight=1)
        usrlog_label.grid(row=0, column=0)