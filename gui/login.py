from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3 as sql
from users import *

class Login_Page:
    def __init__(self):
        pass

    def login(self, var1, var2):
        if u.user_login(var1.get(), var2.get()) is False:
            var2.delete(0, END)
            messagebox.showerror("Error", "Invalid username or password.")
            return False
        else:
            var1.delete(0, END)
            var2.delete(0, END)
            return True

lp = Login_Page()

root = Tk()
root.title("Ledger Application v.0.0.2")
root.geometry("1280x800")

logo = ImageTk.PhotoImage(Image.open("ledger.png").resize((300, 300)))
Label(root, image=logo).pack()

login_frame = LabelFrame(root, text="User Login", padx=10, pady=10)
username_label = Label(login_frame, text="Username:")
username_entry = Entry(login_frame)
password_label = Label(login_frame, text="Password:")
password_entry = Entry(login_frame, show='\u2022')
login_button = Button(login_frame, text="Login", command=lambda: lp.login(username_entry, password_entry))

login_frame.pack()
username_label.grid(row=0, column=0, sticky=W)
username_entry.grid(row=1, column=0)
password_label.grid(row=2, column=0, sticky=W)
password_entry.grid(row=3, column=0)
login_button.grid(row=4, column=0)

root.mainloop()