from tkinter import *
from tkinter import messagebox, simpledialog, font
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
            messagebox.showinfo("Success", "Login successful.")
            return True

    def logout(self, var):
        u.user_logout(var.get())
        var.delete(0, END)
        messagebox.showinfo("Success", "Logout successful.")
        return True

    def user_creation(self):

        ucw = Toplevel(root, padx=20, pady=20)
        ucw.title("User Creation")
        ucw.geometry("450x615")
        ucw.attributes('-topmost', True)
        ucw.focus_set()
        ucw.grab_set()

        ucw_frame = LabelFrame(ucw, padx=10, pady=10)
        usrname_label = Label(ucw_frame, text="Username:", font=("Arial", 20))
        usrname_entry = Entry(ucw_frame)
        usrname = StringVar()
        usrname.set('''Must contain at least 1 letter & between 3-16 characters;\nCan contain: letters, numbers, _ , ! , ~ , @ , #''')
        usrname_validate = Label(ucw_frame, textvariable=usrname, font=('Arial', 12), fg='white')
        fname_label = Label(ucw_frame, text="First Name:", font=("Arial", 20))
        fname_entry = Entry(ucw_frame)
        fname = StringVar()
        fname.set('Can only contain letters')
        fname_validate = Label(ucw_frame, textvariable=fname, font=('Arial', 12), fg='white')
        lname_label = Label(ucw_frame, text="Last Name:", font=("Arial", 20))
        lname_entry = Entry(ucw_frame)
        lname = StringVar()
        lname.set('Can only contain letters')
        lname_validate = Label(ucw_frame, textvariable=lname, font=('Arial', 12), fg='white')
        password_label = Label(ucw_frame, text="Password:", font=("Arial", 20))
        password_entry = Entry(ucw_frame, show='\u2022')
        psswrd = StringVar()
        psswrd.set('Must be at least 8-32 characters long;\nMust have at least 1 capital, lowercase,\nnumber, & special character each;\nAllowed Special Characters: @ , $ , ! , % , * , ? , &')
        password_validate = Label(ucw_frame, textvariable=psswrd, font=('Arial', 12), fg='white')
        password_confirm_label = Label(ucw_frame, text="Confirm Password:", font=("Arial", 20))
        password_confirm_entry = Entry(ucw_frame, show='\u2022')
        pass_confirm = StringVar()
        pass_confirm.set('')
        pass_confirm_validate = Label(ucw_frame, textvariable=pass_confirm, font=('Arial', 12))
        conifrm_btn = Button(ucw, text='Confirm')

        ucw_frame.pack(fill=X)
        ucw_frame.grid_columnconfigure(0, weight=1)
        usrname_label.grid(row=0, column=0, sticky=W)
        usrname_entry.grid(row=1, column=0, sticky=EW)
        usrname_validate.grid(row=2, column=0, sticky=EW)
        fname_label.grid(row=3, column=0, sticky=W, pady=(15, 0))
        fname_entry.grid(row=4, column=0, sticky=EW)
        fname_validate.grid(row=5, column=0, sticky=EW)
        lname_label.grid(row=6, column=0, sticky=W, pady=(15, 0))
        lname_entry.grid(row=7, column=0, sticky=EW)
        lname_validate.grid(row=8, column=0, sticky=EW)
        password_label.grid(row=9, column=0, sticky=W, pady=(15, 0))
        password_entry.grid(row=10, column=0, sticky=EW)
        password_validate.grid(row=11, column=0, sticky=EW)
        password_confirm_label.grid(row=12, column=0, sticky=W, pady=(15, 0))
        password_confirm_entry.grid(row=13, column=0, sticky=EW)
        pass_confirm_validate.grid(row=14, column=0, sticky=EW)
        conifrm_btn.pack(pady=10)

        def usrname_validation(event):
            current_val = usrname_entry.get()
            if current_val == '':
                usrname_validate.config(fg='white')
            elif u.validate_username(current_val):
                usrname_validate.config(fg='green')
            else:
                usrname_validate.config(fg='red')

        def fname_validation(event):
            current_val = fname_entry.get()
            if current_val == '':
                fname_validate.config(fg='white')
            elif u.validate_name(current_val):
                fname_validate.config(fg='green')
            else:
                fname_validate.config(fg='red')

        def lname_validation(event):
            current_val = lname_entry.get()
            if current_val == '':
                lname_validate.config(fg='white')
            elif u.validate_name(current_val):
                lname_validate.config(fg='green')
            else:
                lname_validate.config(fg='red')

        def pass_validation(event):
            current_val = password_entry.get()
            if current_val == '':
                password_validate.config(fg='white')
            elif u.validate_password(current_val):
                password_validate.config(fg='green')
            else:
                password_validate.config(fg='red')

        def passcon_validation(event):
            current_pass = password_entry.get()
            current_val = password_confirm_entry.get()
            if current_val == '':
                pass_confirm.set('')
                pass_confirm_validate.config(fg='white')
            elif current_val == current_pass:
                pass_confirm.set('Confirmed!')
                pass_confirm_validate.config(fg='green')
            else:
                pass_confirm.set('Passwords don\'t match!')
                pass_confirm_validate.config(fg='red')

        usrname_entry.bind('<KeyRelease>', usrname_validation)
        fname_entry.bind('<KeyRelease>', fname_validation)
        lname_entry.bind('<KeyRelease>', lname_validation)
        password_entry.bind('<KeyRelease>', pass_validation)
        password_confirm_entry.bind('<KeyRelease>', passcon_validation)

        return

lp = Login_Page()

root = Tk()
root.title("Ledger Application v.0.0.2")
root.geometry("1280x800")
root.configure(pady=50)

logo = ImageTk.PhotoImage(Image.open("ledger.png").resize((300, 300)))
Label(root, image=logo).pack()
Label(root, text="Ledger Application v.0.0.2", pady=20, font=('Times', 48, 'bold italic')).pack()

login_frame = LabelFrame(root, text="User Login", padx=10, pady=10)
username_label = Label(login_frame, text="Username:")
username_entry = Entry(login_frame)
password_label = Label(login_frame, text="Password:")
password_entry = Entry(login_frame, show='\u2022')
login_button = Button(login_frame, text="Login", command=lambda: lp.login(username_entry, password_entry))
logout_button = Button(root, text="Logout", command=lambda: lp.logout(username_entry))

login_frame.pack()
username_label.grid(row=0, column=0, sticky=W)
username_entry.grid(row=1, column=0)
password_label.grid(row=2, column=0, sticky=W)
password_entry.grid(row=3, column=0)
login_button.grid(row=4, column=0)
logout_button.pack()

Button(root, text="Create User", command=lp.user_creation).pack()

root.mainloop()