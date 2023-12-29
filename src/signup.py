import hashlib
import re
import tkinter as tk
from tkinter import messagebox
from database import Database
import customtkinter as ctk

class SignUpGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Up")
        self.root.iconbitmap("icons/music.ico")
        self.setup_ui()
        self.db = Database()

    def setup_ui(self):
        self.label_signup = ctk.CTkLabel(self.root, text="Sign Up")
        self.label_signup.grid(column=0, row=0, columnspan=2, pady=15)

        self.label_name = ctk.CTkLabel(self.root, text="Name:")
        self.label_name.grid(column=0, row=1, padx=15, pady=(0, 15), sticky="w")
        self.entry_name = ctk.CTkEntry(self.root)
        self.entry_name.grid(column=1, row=1, padx=15, pady=(0, 15), sticky="w")

        self.label_email = ctk.CTkLabel(self.root, text="Email:")
        self.label_email.grid(column=0, row=3, padx=15, pady=(0, 15), sticky="w")
        self.entry_email = ctk.CTkEntry(self.root)
        self.entry_email.grid(column=1, row=3, padx=15, pady=(0, 15), sticky="w")

        self.label_password = ctk.CTkLabel(self.root, text="Password:")
        self.label_password.grid(column=0, row=4, padx=15, pady=(0, 15), sticky="w")
        self.entry_password = ctk.CTkEntry(self.root, show="*")
        self.entry_password.grid(column=1, row=4, padx=15, pady=(0, 15), sticky="w")

        self.button_signup = ctk.CTkButton(self.root, text="Sign Up", command=self.sign_up)
        self.button_signup.grid(column=0, row=5, columnspan=2, padx=15, pady=(0, 15))

        self.label_message = ctk.CTkLabel(self.root, text="")
        self.label_message.grid(column=0, row=6, columnspan=2, padx=15, pady=(0, 15))

        self.label_already_have_account = ctk.CTkLabel(self.root, text="You already have an account?")
        self.label_already_have_account.grid(column=0, row=7, columnspan=2, padx=15, pady=(0, 15))

        self.button_login = ctk.CTkButton(self.root, text="Login", command=self.go_to_login)
        self.button_login.grid(column=0, row=8, columnspan=2, padx=15, pady=(0, 15))

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
        self.root.withdraw()
        login_root = ctk.CTk()
        login_gui = LoginGUI(login_root)

        def on_login_window_close():
            login_root.withdraw()  # Hide the login window
            login_root.after(1, login_root.destroy)  # Schedule destruction after a short delay
            self.root.deiconify()  # Bring back the main window

        login_root.protocol("WM_DELETE_WINDOW", on_login_window_close)
        login_root.mainloop()


if __name__ == "__main__":
    root = ctk.CTk()
    signup_gui = SignUpGUI(root)
    root.mainloop()
