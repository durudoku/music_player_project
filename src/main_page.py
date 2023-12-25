import tkinter as tk
from tkinter import scrolledtext
from database import Database

class MainPageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Page")

        # Initialize database operations
        self.db = Database()

        # Create GUI elements
        self.playlist_listbox = scrolledtext.ScrolledText(root, width=30, height=10, state=tk.DISABLED)
        self.playlist_listbox.pack(side=tk.LEFT, padx=10, pady=10)

        self.song_listbox = scrolledtext.ScrolledText(root, width=40, height=10, state=tk.DISABLED)
        self.song_listbox.pack(side=tk.LEFT, padx=10, pady=10)

        # Populate playlists
        self.populate_playlists()

        # Set event handler for playlist selection
        self.playlist_listbox.bind("<ButtonRelease-1>", self.show_selected_playlist_songs)

    def populate_playlists(self):
        # Fetch playlists from the database
        playlists = self.db.fetch_playlists()

        # Display playlists in the listbox
        for playlist in playlists:
            self.playlist_listbox.insert(tk.END, playlist[1] + "\n")

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


if __name__ == "__main__":
    root = tk.Tk()
    main_page_gui = MainPageGUI(root)
    root.mainloop()
