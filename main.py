from tkinter import *
from tkinter import messagebox, simpledialog, font
from PIL import ImageTk, Image
import sqlite3 as sql
from accounts import *
from ledger import *
from gui.login import *
from users import *
from gui.user_home import *

def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()

root = Tk()
root.title("Ledger Application v.0.0.2")
root.geometry("1280x800")
root.configure(pady=50)

lp = Login_Page(root)
uh = User_Home(root)

#lp.build_login()
uh.build_userhome()

root.mainloop()