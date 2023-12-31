import tkinter as tk
from tkinter import ttk

from src.add_song import AddSongApp
from src.edit_user import EditUserApp
import customtkinter as ctk


class AdminPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Page")
        self.root.geometry("200x100+100+100")
        self.root.iconbitmap("icons/music.ico")

        self.add_song_button = ctk.CTkButton(root, text="Add Song", command=self.add_song_page)
        self.add_song_button.pack(pady=15)

        self.edit_user_button = ctk.CTkButton(root, text="Edit Users", command=self.edit_user_page)
        self.edit_user_button.pack(pady=(0,15))

    def add_song_page(self):
        add_song = ctk.CTk()
        AddSongApp(add_song)
        add_song.mainloop()

    def edit_user_page(self):
        edit_user = ctk.CTk()
        EditUserApp(edit_user)
        edit_user.mainloop()


if __name__ == "__main__":
    root = ctk.CTk()
    app = AdminPage(root)
    root.mainloop()
