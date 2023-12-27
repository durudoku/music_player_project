import hashlib
import tkinter as tk
from tkinter import messagebox
from database import Database
from main_page import MainPageGUI

from src.admin_page import AdminPage


class LoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("230x300+100+100")

        self.label_welcome = tk.Label(root, text="Login")
        self.label_welcome.place(x=100, y=30)

        self.label_email = tk.Label(root, text="Email:")
        self.label_email.place(x=10, y=60)
        self.entry_email = tk.Entry(root)
        self.entry_email.place(x=80, y=60)

        self.label_password = tk.Label(root, text="Password:")
        self.label_password.place(x=10, y=100)
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.place(x=80, y=100)

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.place(x=110, y=130)

        self.label_signup = tk.Label(root, text="Don't have an account?")
        self.label_signup.place(x=50, y=180)

        self.signup_button = tk.Button(root, text="Sign Up", command=self.go_to_signup)
        self.signup_button.place(x=80, y=200)

        self.db = Database()

    def login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if(email == "admin" and password == "admin"):
            messagebox.showinfo("Admin", "Directing to Admin Page.")
            self.root.destroy()
            admin_page = tk.Tk()
            AdminPage(admin_page)
            admin_page.mainloop()
        else:
            if self.db.check_credentials(email, hashed_password):
                messagebox.showinfo("Success", "Login successful.")
                self.root.destroy()
                main_page_root = tk.Tk()
                MainPageGUI(main_page_root)
                main_page_root.mainloop()
            else:
                messagebox.showerror("Error", "Invalid email or password.")

    def go_to_signup(self):
        from signup import SignUpGUI  # Import the class only when needed
        self.root.destroy()
        signup_root = tk.Tk()
        signup_gui = SignUpGUI(signup_root)
        signup_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    login_gui = LoginGUI(root)
    root.mainloop()
