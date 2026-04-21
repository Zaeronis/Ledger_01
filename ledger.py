####################Imports####################
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

####################Objects####################

ph = a.PasswordHasher()

####################Global Variables####################

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

####################Classes####################

########################################
class Ledger:
    def __init__(self):
        pass

    def open_ledger(self):
        conn = sql.connect('ledger.db')
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
########################################
class User:
    def __init__(self):
        pass

    def create_uid(self):
        conn, c = l.open_ledger()
        while True:
            uid = ''.join(r.choices(st.ascii_letters + st.digits, k=16))
            condition = re.search(r'(?=.*[A-Z])(?=.*[a-z])(?=.*\d)', uid)
            if condition is None:
                print('UID invalid')
                print('Trying again...')
                pass
            elif uid in c.execute(f'SELECT uid FROM ledger_users').fetchall():
                print('UID already exists')
                print('Trying again...')
                pass
            else:
                break
        l.close_ledger(conn, c)
        return uid

    def get_uid(self, uname):
        conn, c = l.open_ledger()
        c.execute(f'SELECT uid FROM ledger_users WHERE username = "{uname}"')
        uid = c.fetchone()[0]
        l.close_ledger(conn, c)
        return uid

    def create_username(self):
        conn, c = l.open_ledger()
        while True:
            uname = input('Please enter a username:\n')
            conditions = not re.fullmatch(r'((?=.*[a-z])|(?=.*[A-Z]))[A-Za-z0-9_!~@#]{3,16}', uname)
            if conditions:
                print('''
                \nUsername must be between 3 and 16 character, 
                contain at least one or more letters or numbers,
                and the following characters:   _   @   #   !   ~''')
                pass
            else:
                break
        return uname

    def create_name(self, pos):
        while True:
            name = input(f'Please enter your {pos} name: ')
            condition = not re.fullmatch(r'[A-Za-z]+', name)
            if condition:
                print('Name can only contain only letters.\n')
                pass
            else:
                break
        return name

    def create_password(self):
        while True:
            password = input('Please enter a password:\n')
            conditions = not re.fullmatch(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,32}', password)
            if conditions:
                print('''Password must be at least
                 8 - 32 characters long, have at least
                 one capital and lowercase letter
                 each, one number, and one
                 special character.\n''')
                pass
            else:
                password = ph.hash(password)
                confirmation = input('Please confirm your password:\n')
                try:
                    if ph.verify(password, confirmation):
                        print("Success! Password saved.")
                except:
                    print("Passwords do not match. Please try again.")
                    continue
                break
        return password

    def validate_password(self, uname, psswd):
        conn, c = l.open_ledger()
        uid = self.get_uid(uname)
        password = c.execute(f'SELECT password FROM user_passwords WHERE uid = "{uid}"').fetchone()[0]
        if ph.verify(password, psswd):
            l.close_ledger(conn, c)
            return True
        else:
            l.close_ledger(conn, c)
            return False

    def update_password(self, uname):
        conn, c = l.open_ledger()
        uid = self.get_uid(uname)
        psswd = input('Please enter your current password: ')
        if not self.validate_password(uname, psswd):
            print('Invalid password.')
            l.close_ledger(conn, c)
            return None
        else:
            print('Password is valid.')
            print('Updating password...')
            password = self.create_password()
            c.execute(f'UPDATE user_passwords SET password = "{password}" WHERE uid = "{uid}"')
            conn.commit()
            l.close_ledger(conn, c)
            return password

    def create_user(self):
        conn, c = l.open_ledger()
        condition = 'True' in c.execute(f'SELECT logged_in FROM ledger_users').fetchall()
        if condition:
            print('Please log out before creating a new user.')
            return None
        else:
            uid = self.create_uid()
            username = self.create_username()
            first_name = self.create_name('first')
            last_name = self.create_name('last')
            password = self.create_password()
            logged_in = 'True'
            datetime = str(dt.datetime.now())
            c.execute(f'INSERT INTO ledger_users VALUES (?,?,?,?,?,?)', (uid, username, first_name, last_name, logged_in, datetime))
            c.execute(f'INSERT INTO user_passwords VALUES (?,?,?)', (uid, password, datetime))
            conn.commit()
            l.close_ledger(conn, c)
        return uid, username, first_name, last_name, password

    def user_login(self, username, password):
        conn, c = l.open_ledger()
        condition = 'True' in c.execute(f'SELECT logged_in FROM ledger_users').fetchall()
        if condition:
            print('You are already logged in. Please log out to log into an account.')
            return None
        else:
            if self.validate_password(username, password):
                c.execute(f'UPDATE ledger_users SET logged_in = "True" WHERE uid = "{self.get_uid(username)}"')
                conn.commit()
                l.close_ledger(conn, c)
                print('Login successful.')
                return True
            else:
                print('Invalid username or password.')
                l.close_ledger(conn, c)
                return None

    def user_logout(self, username):
        conn, c = l.open_ledger()
        condition = 'True' not in c.execute(f'SELECT logged_in FROM ledger_users WHERE username = "{username}"').fetchone()
        if condition:
            print('You are not logged in.')
            l.close_ledger(conn, c)
            return None
        else:
            print('Logging out...')
            c.execute(f'UPDATE ledger_users SET logged_in = "False" WHERE username = "{username}"')
            conn.commit()
            l.close_ledger(conn, c)
            return True


u = User()
########################################
class Account:
    def __init__(self):
        pass

ac = Account()
########################################
class Login_Page:
    def __init__(self):
        pass

    def login(self):
        pass

####################GUI####################


#####Root Variables####################

root = Tk()
root.title("Ledger Application v.0.0.2")
root.iconbitmap("image.ico")
root.geometry("1280x800")

#####Login Page####################

ledger_logo = Image.open("image.png")
ledger_logo_resize = ledger_logo.resize((300, 300))
logo_image = ImageTk.PhotoImage(ledger_logo_resize)
logo = Label(root, image=logo_image)
logo.pack()

login_frame = LabelFrame(root, text="User Login", padx=10, pady=10)
username_label = Label(login_frame, text="Username:")
username_entry = Entry(login_frame)
password_label = Label(login_frame, text="Password:")
password_entry = Entry(login_frame, show="*")
login_button = Button(login_frame, text="Login", command=lambda: u.user_login(username_entry.get(), password_entry.get()))

login_frame.pack()
username_label.grid(row=0, column=0, sticky=W)
username_entry.grid(row=1, column=0)
password_label.grid(row=2, column=0, sticky=W)
password_entry.grid(row=3, column=0)
login_button.grid(row=4, column=0)

#####Runtime####################

root.mainloop()

####################Functions####################



####################Testing/Debugging####################

#l.first_time_setup()
#print(u.create_user())
#print(u.user_login())
#print(u.user_logout('Zaeronis'))
#print(u.update_password('Zaeronis'))