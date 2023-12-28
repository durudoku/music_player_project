import hashlib
import re
import tkinter as tk
from tkinter import messagebox
from database import Database
from login import LoginGUI
import customtkinter as ctk

class SignUpGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Up")
        self.root.geometry("250x320+100+100")
        self.root.iconbitmap("icons/music.ico")

        self.label_welcome = ctk.CTkLabel(root, text="Sign Up")
        self.label_welcome.place(x=100, y=30)

        self.label_name = ctk.CTkLabel(root, text="Name:")
        self.label_name.place(x=10, y=60)
        self.entry_name = ctk.CTkEntry(root)
        self.entry_name.place(x=80, y=60)

        self.label_email = ctk.CTkLabel(root, text="Email:")
        self.label_email.place(x=10, y=100)
        self.entry_email = ctk.CTkEntry(root)
        self.entry_email.place(x=80, y=100)

        self.label_password = ctk.CTkLabel(root, text="Password:")
        self.label_password.place(x=10, y=140)
        self.entry_password = ctk.CTkEntry(root, show="*")
        self.entry_password.place(x=80, y=140)

        self.sign_up_button = ctk.CTkButton(root, text="Sign Up", command=self.sign_up)
        self.sign_up_button.place(x=60, y=180)

        self.label_message = ctk.CTkLabel(root, text="")
        self.label_message.place(x=50, y=210)

        self.label_login = ctk.CTkLabel(root, text="You already have an account?")
        self.label_login.place(x=40, y=250)

        self.login_button = ctk.CTkButton(root, text="Login", command=self.go_to_login)
        self.login_button.place(x=60, y=280)

        self.db = Database()

    def sign_up(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        password = self.entry_password.get()

        # Regex
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        username_regex = r"^[a-zA-Z]{1,20}$"
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%?&])[A-Za-z\d@$!%*?&]{8,}$"

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if not re.match(email_regex, email):
            self.label_message.configure(text="Invalid email address.\nPlease enter a valid email.")

        elif not re.match(username_regex, name):
            self.label_message.configure(text="Invalid username.\nPlease enter 1 to 20 alphabetical characters only.")

        elif not re.match(password_regex, password):
            self.label_message.configure(text="Invalid password.\nPlease follow the password requirements.")
        else:
            # Check if email already exists
            if self.db.check_email_exists(email):
                self.label_message.configure(text="Email already exists.\nTry a different one.")
            else:
                self.db.add_user(name, email, hashed_password)
                messagebox.showinfo("Success", "Account created successfully.")

    def go_to_login(self):
        from login import LoginGUI

        # Hide the main window
        self.root.withdraw()

        # Create the login window
        login_root = ctk.CTk()
        login_gui = LoginGUI(login_root)

        def on_login_window_close():
            login_root.withdraw()  # Hide the login window
            login_root.after(1, login_root.destroy)  # Schedule destruction after a short delay
            self.root.deiconify()  # Bring back the main window

        # Use the protocol on the Tk instance of the Toplevel window
        login_root.protocol("WM_DELETE_WINDOW", on_login_window_close)
        login_root.mainloop()


if __name__ == "__main__":
    root = ctk.CTk()
    signup_gui = SignUpGUI(root)
    root.mainloop()
