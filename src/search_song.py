# search_song.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import Database


class SearchSongApp:
    def __init__(self, root, playlist_id):
        self.root = root
        self.root.title("Search Songs")
        self.playlist_id = playlist_id
        self.setup_ui()

    def setup_ui(self):
        # Create Treeview with columns
        self.song_tree = ttk.Treeview(self.root, columns=("ID", "Track Name", "Artist Name", "Album Name", "Duration (ms)", "File Path"), show="headings")
        self.song_tree.pack()

        # Set column headings
        self.song_tree.heading("ID", text="ID")
        self.song_tree.heading("Track Name", text="Track Name")
        self.song_tree.heading("Artist Name", text="Artist Name")
        self.song_tree.heading("Album Name", text="Album Name")
        self.song_tree.heading("Duration (ms)", text="Duration (ms)")
        self.song_tree.heading("File Path", text="File Path")

        self.load_songs()

        self.add_button = ttk.Button(self.root, text="Add", width=5, command=self.add_song_to_playlist)
        self.add_button.pack(pady=10)

    def load_songs(self):
        # Fetch songs from the database
        db = Database()
        songs = db.get_all_songs()

        # Populate the Treeview with songs
        for song in songs:
            self.song_tree.insert("", "end", values=song)

    def add_song_to_playlist(self):
        selected_item = self.song_tree.selection()
        if selected_item:
            # Get the song details
            song_details = {
                "song_id": self.song_tree.item(selected_item, "values")[0],
                "track_name": self.song_tree.item(selected_item, "values")[1],
                "artist_name": self.song_tree.item(selected_item, "values")[2],
                "album_name": self.song_tree.item(selected_item, "values")[3],
                "duration_ms": self.song_tree.item(selected_item, "values")[4],
                "file_path": self.song_tree.item(selected_item, "values")[5],
            }

            # Save the song to the playlist
            db = Database()

            try:
                db.add_song_to_playlist(self.playlist_id, song_details)
            except DatabaseWarning as e:
                # Display warning to the user
                messagebox.showwarning("Song is already on the list!", str(e))

            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SearchSongApp(root, playlist_id=1)  # Replace 1 with the actual playlist ID
    root.mainloop()
