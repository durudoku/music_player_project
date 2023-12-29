from src.signup import SignUpGUI
from src.login import LoginGUI
import customtkinter as ctk

class WelcomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.iconbitmap("icons/music.ico")

        self.label_welcome = ctk.CTkLabel(root, text="Welcome to the Music Application!")
        self.label_welcome.grid(row=0, column=0, columnspan=2, sticky="we", pady=15, padx=30)

        self.label_already_user = ctk.CTkLabel(root, text="Already a user?")
        self.label_already_user.grid(row=1, column=0, columnspan=2, sticky="we", pady=(0, 7))

        self.button_login = ctk.CTkButton(root, text="Login", command=self.go_to_login)
        self.button_login.grid(row=2, column=0, sticky="nswe", pady=(0, 15), padx=40)

        self.label_already_user = ctk.CTkLabel(root, text="New to Music Player?")
        self.label_already_user.grid(row=3, column=0, columnspan=2, sticky="we", pady=(15, 7))

        self.button_login = ctk.CTkButton(root, text="Sign Up", command=self.go_to_login)
        self.button_login.grid(row=4, column=0, columnspan=1, sticky="nswe", pady=(0, 15), padx=40)

    def go_to_login(self):
        login_page = ctk.CTk()
        LoginGUI(login_page)
        self.root.destroy()
        login_page.mainloop()

    def go_to_signup(self):
        signup_page = ctk.CTk()
        SignUpGUI(signup_page)
        self.root.destroy()
        signup_page.mainloop()


if __name__ == "__main__":
    root = ctk.CTk()
    app = WelcomePage(root)
    root.mainloop()
