import hashlib
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import Database
from main_page import MainPageGUI
import customtkinter as ctk

from src import langpack
from src.admin_page import AdminPage
import CTkMessagebox as msg


class LoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("250x300+100+100")
        self.root.iconbitmap("icons/music.ico")

        self.selected_language = tk.StringVar(value="en")
        self.i18n = langpack.I18N(self.selected_language.get())

        self.label_login = ctk.CTkLabel(root, text=self.i18n.label_login)
        self.label_login.place(x=100, y=30)

        self.label_email = ctk.CTkLabel(root, text=self.i18n.label_email)
        self.label_email.place(x=10, y=60)
        self.entry_email = ctk.CTkEntry(root)
        self.entry_email.place(x=80, y=60)

        self.label_password = ctk.CTkLabel(root, text=self.i18n.label_password)
        self.label_password.place(x=10, y=100)
        self.entry_password = ctk.CTkEntry(root, show="*")
        self.entry_password.place(x=80, y=100)

        self.button_login = ctk.CTkButton(root, text=self.i18n.button_login, command=self.login)
        self.button_login.place(x=60, y=140)

        self.label_signup = ctk.CTkLabel(root, text=self.i18n.label_signup)
        self.label_signup.place(x=50, y=180)

        self.button_signup = ctk.CTkButton(root, text=self.i18n.button_signup, command=self.go_to_signup)
        self.button_signup.place(x=60, y=210)

        self.context_menu = tk.Menu(self.root, tearoff=False)
        self.context_menu.add_radiobutton(label="English", variable=self.selected_language, value="en",
                                          command=lambda: self.reload_gui_text("en"))
        self.context_menu.add_radiobutton(label="Türkçe", variable=self.selected_language, value="tr",
                                          command=lambda: self.reload_gui_text("tr"))
        self.db = Database()
        self.bind_widgets()

    def bind_widgets(self):
        self.root.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        self.context_menu.tk_popup(x=event.x_root, y=event.y_root)

    def reload_gui_text(self, language):
        self.i18n = langpack.I18N(language)
        self.label_login.configure(text=self.i18n.label_login)
        self.label_email.configure(text=self.i18n.label_email)
        self.label_password.configure(text=self.i18n.label_password)
        self.button_login.configure(text=self.i18n.button_login)
        self.label_signup.configure(text=self.i18n.label_signup)
        self.button_signup.configure(text=self.i18n.button_signup)

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
                msg.CTkMessagebox(self.root, title="Success",
                                  message="Login successful.",
                                  option_1="OK")
                self.root.withdraw()  # Hide the current login window
                self.go_to_main_page()
            else:
                msg.CTkMessagebox(self.root, title="Error",
                                  message="Invalid email or password.",
                                  option_1="OK")

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
        self.root.withdraw()  # hide
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
