import hashlib
import tkinter as tk
from tkinter import messagebox
from database import Database
from main_page import MainPageGUI
import customtkinter as ctk
from src.admin_page import AdminPage


class LoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("250x300+100+100")
        self.root.iconbitmap("icons/music.ico")

        self.label_welcome = ctk.CTkLabel(root, text="Login")
        self.label_welcome.place(x=100, y=30)

        self.label_email = ctk.CTkLabel(root, text="Email:")
        self.label_email.place(x=10, y=60)
        self.entry_email = ctk.CTkEntry(root)
        self.entry_email.place(x=80, y=60)

        self.label_password = ctk.CTkLabel(root, text="Password:")
        self.label_password.place(x=10, y=100)
        self.entry_password = ctk.CTkEntry(root, show="*")
        self.entry_password.place(x=80, y=100)

        self.login_button = ctk.CTkButton(root, text="Login", command=self.login)
        self.login_button.place(x=60, y=140)

        self.label_signup = ctk.CTkLabel(root, text="Don't have an account?")
        self.label_signup.place(x=50, y=180)

        self.signup_button = ctk.CTkButton(root, text="Sign Up", command=self.go_to_signup)
        self.signup_button.place(x=60, y=210)

        self.db = Database()

    def login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if email == "admin" and password == "admin":
            messagebox.showinfo("Admin", "Directing to Admin Page.")
            self.root.withdraw()  # Hide the current login window
            admin_page = ctk.CTk()
            AdminPage(admin_page)
            admin_page.protocol("WM_DELETE_WINDOW", lambda: self.on_admin_page_close(admin_page))
            admin_page.mainloop()
        else:
            if self.db.check_credentials(email, hashed_password):
                messagebox.showinfo("Success", "Login successful.")
                self.root.withdraw()  # Hide the current login window
                self.go_to_main_page()
            else:
                messagebox.showerror("Error", "Invalid email or password.")

    def on_admin_page_close(self, admin_page):
        admin_page.withdraw()  # Hide the admin page window
        admin_page.after(1, admin_page.destroy)  # Schedule destruction after a short delay
        self.root.deiconify()  # Bring back the login window

    def go_to_main_page(self):
        from main_page import MainPageGUI

        # Hide the login window
        self.root.withdraw()

        # Create the main page window
        main_page_root = ctk.CTk()
        main_page_gui = MainPageGUI(main_page_root)

        def on_main_page_close():
            main_page_root.withdraw()  # Hide the main page window
            main_page_root.after(1, main_page_root.destroy)  # Schedule destruction after a short delay
            self.root.deiconify()  # Bring back the login window

        # Use the protocol on the Tk instance of the Toplevel window
        main_page_root.protocol("WM_DELETE_WINDOW", on_main_page_close)
        main_page_root.mainloop()

    def go_to_signup(self):
        from signup import SignUpGUI

        # Hide the main window
        self.root.withdraw()

        # Create the signup window
        signup_root = ctk.CTk()
        signup_gui = SignUpGUI(signup_root)

        def on_signup_window_close():
            signup_root.withdraw()  # Hide the signup window
            signup_root.after(1, signup_root.destroy)  # Schedule destruction after a short delay
            self.root.deiconify()  # Bring back the main window

        # Use the protocol on the Tk instance of the Toplevel window
        signup_root.protocol("WM_DELETE_WINDOW", on_signup_window_close)
        signup_root.mainloop()


if __name__ == "__main__":
    root = ctk.CTk()
    login_gui = LoginGUI(root)
    root.mainloop()
