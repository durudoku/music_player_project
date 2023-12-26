import tkinter as tk
from tkinter import scrolledtext, ttk
from database import Database
from playlist import PlaylistGUI
from src.audio_player import AudioPlayer
from src.search_song import SearchSongApp
import gettext


class MainPageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("900x300+100+100")
        self.root.iconbitmap("music.ico")
        self.db = Database()
        self.setup_ui()
        self.populate_playlists()
        self.populate_songs()
        self.current_audio_player = None
        self.selected_playlist_id = None

    def setup_ui(self):
        # Playlists
        self.label_playlists = tk.Label(self.root, text="Playlists")
        self.label_playlists.place(x=10, y=30)

        self.playlist_tree = ttk.Treeview(self.root, columns=("ID", "Name"), show="headings", selectmode="browse")
        self.playlist_tree.heading("ID", text="ID")
        self.playlist_tree.heading("Name", text="Name")
        self.playlist_tree.column("ID", width=50)
        self.playlist_tree.column("Name", width=200)
        self.playlist_tree.place(x=10, y=50)

        self.button_playlist_add = ttk.Button(self.root, text="+", width=5, command=self.show_add_playlist_gui)
        self.button_playlist_add.place(x=270, y=65)

        self.button_playlist_remove = ttk.Button(self.root, text="-", width=5, command=self.remove_selected_playlist)
        self.button_playlist_remove.place(x=270, y=170)

        # Songs
        self.label_songs = tk.Label(self.root, text="Songs")
        self.label_songs.place(x=330, y=30)

        self.song_tree = ttk.Treeview(self.root, columns=("ID", "Track", "Artist", "Album", "Duration"), show="headings")
        self.song_tree.heading("ID", text="ID")
        self.song_tree.heading("Track", text="Track Name")
        self.song_tree.heading("Artist", text="Artist Name")
        self.song_tree.heading("Album", text="Album Name")
        self.song_tree.heading("Duration", text="Duration")

        self.song_tree.column("ID", width=30)
        self.song_tree.column("Track", width=150)
        self.song_tree.column("Artist", width=100)
        self.song_tree.column("Album", width=100)
        self.song_tree.column("Duration", width=80)

        self.song_tree.place(x=330, y=50)

        self.button_song_add = ttk.Button(self.root, text="+", width=5, command=self.show_add_song_gui)
        self.button_song_add.place(x=800, y=65)

        self.button_song_remove = ttk.Button(self.root, text="-", width=5, command=self.remove_selected_songs)
        self.button_song_remove.place(x=800, y=170)

        self.song_tree.bind("<Double-1>", self.open_song_gui)
        self.playlist_tree.bind("<ButtonRelease-1>", lambda event: self.load_songs_for_selected_playlist())

    def populate_playlists(self):
        # Clear existing content in the playlist treeview
        self.playlist_tree.delete(*self.playlist_tree.get_children())

        # Fetch playlists from the database
        playlists = self.db.fetch_playlists()

        # Display playlists in the treeview
        for playlist in playlists:
            self.playlist_tree.insert("", "end", values=playlist)

    def populate_songs(self):
        # Clear existing items
        for item in self.song_tree.get_children():
            self.song_tree.delete(item)

        # Fetch data from the database
        songs = self.db.fetch_songs()

    def load_songs(self):
        # Fetch song IDs for the selected playlist from the database
        if self.selected_playlist_id != None:
            playlist_songs = self.db.get_playlist_songs(self.selected_playlist_id)

            for item in self.song_tree.get_children():
                self.song_tree.delete(item)

            for song_id in playlist_songs:
                song_details = self.db.get_song_by_id(song_id)
                self.song_tree.insert("", "end", values=song_details)

    def show_add_playlist_gui(self):
        # Create a new window for adding a playlist
        add_playlist_window = tk.Toplevel(self.root)
        add_playlist_window.title("Add Playlist")

        # Create an instance of PlaylistGUI
        playlist_gui = PlaylistGUI(add_playlist_window, callback=self.populate_playlists)

    def show_add_song_gui(self):
        # Get the selected playlist's ID
        selected_item = self.playlist_tree.selection()
        if selected_item:
            playlist_id = int(self.playlist_tree.item(selected_item, "values")[0])  # Assuming the ID is in the first column

            # Open the search song GUI
            search_song_root = tk.Toplevel(self.root)
            search_song_app = SearchSongApp(search_song_root,
                                            playlist_id=self.selected_playlist_id)  # Pass the selected playlist ID

    def remove_selected_playlist(self):
        # Get the selected item in the treeview
        selected_item = self.playlist_tree.selection()

        if selected_item:
            # Get the playlist ID from the selected item
            playlist_id = self.playlist_tree.item(selected_item, "values")[0]

            # Remove the playlist from the database
            self.db.remove_playlist(playlist_id)

            # Update the playlist treeview
            self.populate_playlists()

    def load_songs_for_selected_playlist(self):
        selected_item = self.playlist_tree.selection()
        if selected_item:
            self.selected_playlist_id = int(
                self.playlist_tree.item(selected_item, "values")[0])  # Assuming the ID is in the first column

            # Load songs for the selected playlist
            self.load_songs()

    def remove_selected_songs(self):
        pass

    def open_song_gui(self, event):
        selected_item = self.song_tree.selection()
        if selected_item:
            # Get the file_path attribute directly
            file_path = self.song_tree.item(selected_item, "values")[5]  # Assuming "File Path" is the 6th column (index 5)

            # Close the current audio player window if it's open
            if self.current_audio_player:
                self.current_audio_player.on_close()

            # Open the new audio player window and pass the reference to the MainPageApp instance
            audio_player_root = tk.Toplevel(self.root)
            audio_player = AudioPlayer(audio_player_root, file_path=file_path, main_page_app=self)

            # Update the currently open audio player window
            self.current_audio_player = audio_player




if __name__ == "__main__":
    root = tk.Tk()
    main_page_gui = MainPageGUI(root)
    root.mainloop()
