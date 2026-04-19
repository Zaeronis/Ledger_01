from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("Ledger Application v.0.0.2")
root.geometry("1280x800")

img = Image.open("image.png")
res_img = img.resize((300, 300))
img = ImageTk.PhotoImage(res_img)
ledger_icon = Label(root, image=img)
ledger_icon.pack()

login_frame = LabelFrame(root, text="Login", padx=10, pady=10)
login_frame.pack()

Label(login_frame, text="Username:").grid(row=1, column=0, columnspan=3, sticky=W)
username = Entry(login_frame).grid(row=2, column=0, columnspan=3)
Label(login_frame, text="Password:").grid(row=3, column=0, columnspan=3, sticky=W)
password = Entry(login_frame, show="*").grid(row=4, column=0, columnspan=3)
login = Button(login_frame, text="Login").grid(row=5, column=1)

create_account = Button(root, text="Create Account").pack()




root.mainloop()