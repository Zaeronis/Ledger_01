from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3 as sql

root = Tk()
root.title("Ledger Application v.0.0.2")
root.geometry("1280x800")

ledger_logo = Image.open("../image.png")
ledger_logo_resize = ledger_logo.resize((300, 300))
logo_image = ImageTk.PhotoImage(ledger_logo_resize)
logo = Label(root, image=logo_image)
logo.pack()

login_frame = LabelFrame(root, text="User Login", padx=10, pady=10)
username_label = Label(login_frame, text="Username:")
username_entry = Entry(login_frame)
password_label = Label(login_frame, text="Password:")
password_entry = Entry(login_frame)
login_button = Button(login_frame, text="Login")

class Ledger_Login:
    def __init__(self):
        pass

    def login(self):


login_frame.pack()
username_label.grid(row=0, column=0, sticky=W)
username_entry.grid(row=1, column=0)
password_label.grid(row=2, column=0, sticky=W)
password_entry.grid(row=3, column=0)
login_button.grid(row=4, column=0)

root.mainloop()