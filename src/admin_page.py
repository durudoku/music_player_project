import tkinter as tk
from tkinter import ttk

from src.add_song import AddSongApp
from src.songs.edit_user import EditUserApp

class AdminPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Page")
        self.root.geometry("230x300+100+100")

        self.add_song_button = ttk.Button(root, text="Add Song", command=self.add_song_page)
        self.add_song_button.pack()

        self.edit_user_button = ttk.Button(root, text="Edit Users", command=self.edit_user_page)
        self.edit_user_button.pack()

    def add_song_page(self):
        add_song = tk.Tk()
        AddSongApp(add_song)
        add_song.mainloop()

    def edit_user_page(self):
        edit_user = tk.Tk()
        EditUserApp(edit_user)
        edit_user.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminPage(root)
    root.mainloop()
