#################### Imports ####################
from turtledemo.sorting_animate import show_text

import argon2 as a
import sqlite3 as sql
import sys as s
import os as o
import time as t
import datetime as dt
import random as r
import re
import string as st
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

#################### Objects ####################

ph = a.PasswordHasher()

#################### Global Variables ####################

users = '''
uid TEXT PRIMARY KEY,
username TEXT,
first_name TEXT,
last_name TEXT,
logged_in TEXT,
datetime TEXT
'''

passwords = '''
uid TEXT PRIMARY KEY,
password TEXT,
datetime TEXT
'''

accounts = '''
uid TEXT PRIMARY KEY,
aid TEXT,
account_name TEXT,
account_type TEXT,
balance REAL,
datetime TEXT
'''

transactions = '''
uid TEXT PRIMARY KEY,
aid TEXT,
tid TEXT,
date TEXT,
description TEXT,
transaction_type TEXT,
amount REAL,
datetime TEXT
'''

itemized = '''
uid TEXT PRIMARY KEY,
aid TEXT,
tid TEXT,
iid TEXT,
item_name TEXT,
transaction_type TEXT,
price REAL,
quantity REAL,
subtotal REAL,
tax REAL,
shipping REAL,
discount REAL,
total REAL,
datetime TEXT
'''

logs = '''
lid INTEGER PRIMARY KEY AUTOINCREMENT,
uid TEXT,
action TEXT,
details TEXT
datetime TEXT,
'''

#################### GUI Variables ####################

##### Root Variables ###################
#################### Classes ####################

########################################
class Ledger:
    def __init__(self):
        pass

    def open_ledger(self):
        conn = sql.connect('/Users/dalton/PycharmProjects/Ledger_01/ledger.db')
        c = conn.cursor()
        return conn, c

    def close_ledger(self, conn, c):
        c.close()
        conn.close()
        return None

    def first_time_setup(self):
        conn, c = self.open_ledger()
        c.execute(f'CREATE TABLE IF NOT EXISTS ledger_users ({users})')
        c.execute(f'CREATE TABLE IF NOT EXISTS user_passwords ({passwords})')
        c.execute(f'CREATE TABLE IF NOT EXISTS user_accounts ({accounts})')
        c.execute(f'CREATE TABLE IF NOT EXISTS account_transactions ({transactions})')
        c.execute(f'CREATE TABLE IF NOT EXISTS itemized_transactions ({itemized})')
        conn.commit()
        self.close_ledger(conn, c)
        return None

l = Ledger()
#l.first_time_setup()