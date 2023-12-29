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
        #self.root.geometry("250x300+100+100")
        self.root.iconbitmap("icons/music.ico")
        self.setup_ui()
        self.db = Database()
        self.bind_widgets()

    def setup_ui(self):
        self.selected_language = tk.StringVar(value="en")
        self.i18n = langpack.I18N(self.selected_language.get())

        self.label_login = ctk.CTkLabel(self.root, text=self.i18n.label_login)
        self.label_login.grid(column=0, row=0, columnspan=2, pady=15)

        self.label_email = ctk.CTkLabel(self.root, text=self.i18n.label_email)
        self.label_email.grid(column=0, row=1, padx=15, pady=(0, 15), sticky="w")

        self.entry_email = ctk.CTkEntry(self.root)
        self.entry_email.grid(column=1, row=1, padx=15, pady=(0, 15), sticky="w")

        self.label_password = ctk.CTkLabel(self.root, text=self.i18n.label_password)
        self.label_password.grid(column=0, row=3, padx=15, pady=(0, 15), sticky="w")

        self.entry_password = ctk.CTkEntry(self.root, show="*")
        self.entry_password.grid(column=1, row=3, padx=15, pady=(0, 15), sticky="w")

        self.button_login = ctk.CTkButton(self.root, text=self.i18n.button_login, command=self.login)
        self.button_login.grid(column=0, row=4, columnspan=2, padx=15, pady=(0, 15), sticky="we")

        self.label_dont_have_account = ctk.CTkLabel(self.root, text=self.i18n.label_dont_have_account)
        self.label_dont_have_account.grid(column=0, row=5, columnspan=2, pady=(15, 5))

        self.button_signup = ctk.CTkButton(self.root, text=self.i18n.button_signup, command=self.go_to_signup)
        self.button_signup.grid(column=0, row=6, columnspan=2, padx=15, pady=(0, 15))

        self.context_menu = tk.Menu(self.root, tearoff=False)
        self.context_menu.add_radiobutton(label="English", variable=self.selected_language, value="en",
                                          command=lambda: self.reload_gui_text("en"))
        self.context_menu.add_radiobutton(label="Türkçe", variable=self.selected_language, value="tr",
                                          command=lambda: self.reload_gui_text("tr"))

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
        self.label_dont_have_account.configure(text=self.i18n.label_dont_have_account)
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
        self.root.withdraw()
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
