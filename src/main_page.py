import tkinter as tk
from tkinter import ttk
from database import Database
from playlist import PlaylistGUI
from src.audio_player import AudioPlayer
from src.search_song import SearchSongApp
import customtkinter as ctk


class MainPageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("700x300+100+100")
        self.root.iconbitmap("icons/music.ico")
        self.db = Database()
        self.setup_ui()
        self.populate_playlists()
        self.populate_songs()
        self.current_audio_player = None
        self.selected_playlist_id = None
        self.root.protocol("WM_DELETE_WINDOW", self.on_main_page_close)

    def setup_ui(self):
        # Playlists
        self.label_playlists = ctk.CTkLabel(self.root, text="Playlists")
        self.label_playlists.place(x=10, y=18)

        self.playlist_tree = ttk.Treeview(self.root, columns=("ID", "Name"), show="headings", selectmode="browse")
        self.playlist_tree.heading("ID", text="ID")
        self.playlist_tree.heading("Name", text="Name")
        self.playlist_tree.column("ID", width=50)
        self.playlist_tree.column("Name", width=200)
        self.playlist_tree.place(x=10, y=50)

        self.button_playlist_add = ctk.CTkButton(self.root, text="Create Playlist", width=5, command=self.show_add_playlist_gui)
        self.button_playlist_add.place(x=10, y=230)

        self.button_playlist_remove = ctk.CTkButton(self.root, text="Delete Playlist", width=5, command=self.remove_selected_playlist)
        self.button_playlist_remove.place(x=110, y=230)

        # Songs
        self.label_songs = ctk.CTkLabel(self.root, text="Songs")
        self.label_songs.place(x=270, y=18)

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

        self.button_song_add = ctk.CTkButton(self.root, text="Add Song", width=5, command=self.show_add_song_gui)
        self.button_song_add.place(x=265, y=230)

        self.button_song_remove = ctk.CTkButton(self.root, text="Delete Playlist", width=5, command=self.remove_selected_songs)
        #self.button_song_remove.place(x=800, y=170)

        self.song_tree.bind("<Double-1>", self.open_song_gui)
        self.playlist_tree.bind("<ButtonRelease-1>", lambda event: self.load_songs_for_selected_playlist())

    def on_main_page_close(self):
        if self.root.winfo_exists():
            self.root.destroy()

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
        if self.selected_playlist_id is not None:
            playlist_songs = self.db.get_playlist_songs(self.selected_playlist_id)

            for item in self.song_tree.get_children():
                self.song_tree.delete(item)

            for song_id in playlist_songs:
                song_details = self.db.get_song_by_id(song_id)
                self.song_tree.insert("", "end", values=song_details)

    def show_add_playlist_gui(self):
        add_playlist_window = tk.Toplevel(self.root)
        add_playlist_window.title("Add Playlist")
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

            self.db.remove_playlist(playlist_id)
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
            file_path = self.song_tree.item(selected_item, "values")[5]
            track_name = self.song_tree.item(selected_item, "values")[1]

            # Close the current audio player window if it's open
            if self.current_audio_player:
                self.current_audio_player.on_close()

            audio_player_root = tk.Toplevel(self.root)
            audio_player = AudioPlayer(audio_player_root, file_path=file_path,
                                       main_page_app=self, track_name=track_name)

            self.current_audio_player = audio_player


if __name__ == "__main__":
    root = ctk.CTk()
    main_page_gui = MainPageGUI(root)
    root.mainloop()
