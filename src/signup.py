import tkinter as tk
from tkinter import messagebox
from database import Database
from login import LoginGUI


class SignUpGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Up")
        self.root.geometry("230x300+100+100")

        self.label_welcome = tk.Label(root, text="Sign Up")
        self.label_welcome.place(x=100, y=30)

        self.label_name = tk.Label(root, text="Name:")
        self.label_name.place(x=10, y=60)
        self.entry_name = tk.Entry(root)
        self.entry_name.place(x=80, y=60)

        self.label_email = tk.Label(root, text="Email:")
        self.label_email.place(x=10, y=100)
        self.entry_email = tk.Entry(root)
        self.entry_email.place(x=80, y=100)

        self.label_password = tk.Label(root, text="Password:")
        self.label_password.place(x=10, y=140)
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.place(x=80, y=140)

        self.sign_up_button = tk.Button(root, text="Sign Up", command=self.sign_up)
        self.sign_up_button.place(x=110, y=170)

        self.label_message = tk.Label(root, text="")
        self.label_message.place(x=10, y=210)

        self.label_login = tk.Label(root, text="You already have an account?")
        self.label_login.place(x=30, y=240)

        self.login_button = tk.Button(root, text="Login", command=self.go_to_login)
        self.login_button.place(x=90, y=260)

    def sign_up(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        password = self.entry_password.get()

        # Check if email already exists
        if Database.check_email_exists(email):
            self.label_message.config(text="Email already exists. Try a different one.")
        else:
            Database.add_user(name, email, password)
            messagebox.showinfo("Success", "Account created successfully.")

    def go_to_login(self):
        self.root.destroy()
        login_root = tk.Tk()
        login_gui = LoginGUI(login_root)
        login_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    signup_gui = SignUpGUI(root)
    root.mainloop()
