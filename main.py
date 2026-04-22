from tkinter import *
from tkinter import messagebox, simpledialog, font
from PIL import ImageTk, Image
import sqlite3 as sql
from accounts import *
from ledger import *
from gui.login import *
from users import *
from gui.user_home import *

root = Tk()
root.title("Ledger Application v.0.0.2")
root.geometry("1280x800")
root.configure(pady=50)

lp = Login_Page(root)

lp.build_login()

root.mainloop()