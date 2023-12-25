import tkinter as tk
from tkinter import scrolledtext, ttk
from database import Database
from playlist import PlaylistGUI

class MainPageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Page")
        self.root.geometry("750x300+100+100")

        self.db = Database()

        # GUI Elements
        self.label_playlists = tk.Label(root, text="Playlists")
        self.label_playlists.place(x=10, y=30)

        self.playlist_listbox = scrolledtext.ScrolledText(root, width=30, height=10, state=tk.DISABLED)
        self.playlist_listbox.place(x=10, y=50)

        self.button_playlist_add = ttk.Button(root, text="+", width=5, command=self.show_add_playlist_gui)
        self.button_playlist_add.place(x=270, y=65)

        self.button_playlist_remove = ttk.Button(root, text="-", width=5)
        self.button_playlist_remove.place(x=270, y=170)

        self.label_songs = tk.Label(root, text="Songs")
        self.label_songs.place(x=330, y=30)

        self.song_listbox = scrolledtext.ScrolledText(root, width=40, height=10, state=tk.DISABLED)
        self.song_listbox.place(x=330, y=50)

        self.button_song_add = ttk.Button(root, text="+", width=5, command=self.show_add_song_gui)
        self.button_song_add.place(x=670, y=65)

        self.button_song_remove = ttk.Button(root, text="-", width=5)
        self.button_song_remove.place(x=670, y=170)

        self.populate_playlists()

        self.playlist_listbox.bind("<ButtonRelease-1>", self.show_selected_playlist_songs)

    def populate_playlists(self):
        # Clear existing content in the playlist listbox
        self.playlist_listbox.config(state=tk.NORMAL)
        self.playlist_listbox.delete(1.0, tk.END)

        # Fetch playlists from the database
        playlists = self.db.fetch_playlists()

        # Display playlists in the listbox
        for playlist in playlists:
            self.playlist_listbox.insert(tk.END, playlist[1] + "\n")

        # Disable the playlist listbox for read-only
        self.playlist_listbox.config(state=tk.DISABLED)

    def show_selected_playlist_songs(self, event):
        # Clear existing songs in the song listbox
        self.song_listbox.config(state=tk.NORMAL)
        self.song_listbox.delete(1.0, tk.END)
        self.song_listbox.config(state=tk.DISABLED)

        # Get the indices of the selected text
        sel_start_index = self.playlist_listbox.tag_ranges(tk.SEL + ' first')
        sel_end_index = self.playlist_listbox.tag_ranges(tk.SEL + ' last')

        # Ensure there is a selection
        if sel_start_index and sel_end_index:
            # Get the selected text using the indices
            sel_start = self.playlist_listbox.index(sel_start_index)
            sel_end = self.playlist_listbox.index(sel_end_index)

            selected_playlist = self.playlist_listbox.get(sel_start, sel_end).strip()

            # Fetch songs for the selected playlist from the database
            songs = self.db.fetch_songs_for_playlist(selected_playlist)

            # Display songs in the listbox
            self.song_listbox.config(state=tk.NORMAL)
            for song in songs:
                self.song_listbox.insert(tk.END, f"{song[1]} by {song[2]}\n")
            self.song_listbox.config(state=tk.DISABLED)

    def show_add_playlist_gui(self):
        # Create a new window for adding a playlist
        add_playlist_window = tk.Toplevel(self.root)
        add_playlist_window.title("Add Playlist")

        # Create an instance of PlaylistGUI
        playlist_gui = PlaylistGUI(add_playlist_window, callback=self.populate_playlists)

    def show_add_song_gui(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    main_page_gui = MainPageGUI(root)
    root.mainloop()
