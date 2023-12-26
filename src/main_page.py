import tkinter as tk
from tkinter import scrolledtext, ttk
from database import Database
from playlist import PlaylistGUI
from src.audio_player import AudioPlayer


class MainPageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Page")
        self.root.geometry("900x300+100+100")

        self.db = Database()

        # Playlists
        self.label_playlists = tk.Label(root, text="Playlists")
        self.label_playlists.place(x=10, y=30)

        self.playlist_tree = ttk.Treeview(root, columns=("ID", "Name"), show="headings", selectmode="browse")
        self.playlist_tree.heading("ID", text="ID")
        self.playlist_tree.heading("Name", text="Name")
        self.playlist_tree.column("ID", width=50)
        self.playlist_tree.column("Name", width=200)
        self.playlist_tree.place(x=10, y=50)

        self.button_playlist_add = ttk.Button(root, text="+", width=5, command=self.show_add_playlist_gui)
        self.button_playlist_add.place(x=270, y=65)

        self.button_playlist_remove = ttk.Button(root, text="-", width=5, command=self.remove_selected_playlist)
        self.button_playlist_remove.place(x=270, y=170)

        # Songs
        self.label_songs = tk.Label(root, text="Songs")
        self.label_songs.place(x=330, y=30)

        self.song_tree = ttk.Treeview(root, columns=("ID", "Track", "Artist", "Album", "Duration"), show="headings")
        self.song_tree.heading("ID", text="ID")
        self.song_tree.heading("Track", text="Track Name")
        self.song_tree.heading("Artist", text="Artist Name")
        self.song_tree.heading("Album", text="Album Name")
        self.song_tree.heading("Duration", text="Duration (ms)")

        self.song_tree.column("ID", width=30)
        self.song_tree.column("Track", width=150)
        self.song_tree.column("Artist", width=100)
        self.song_tree.column("Album", width=100)
        self.song_tree.column("Duration", width=80)

        self.song_tree.place(x=330, y=50)

        self.button_song_add = ttk.Button(root, text="+", width=5, command=self.show_add_song_gui)
        self.button_song_add.place(x=800, y=65)

        self.button_song_remove = ttk.Button(root, text="-", width=5)
        self.button_song_remove.place(x=800, y=170)

        self.song_tree.bind("<Double-1>", self.play_selected_song)
        self.playlist_tree.bind("<ButtonRelease-1>", self.show_selected_playlist_songs)

        # Populate playlists and songs
        self.populate_playlists()
        self.populate_songs()


    def play_selected_song(self, event):
        item = self.song_tree.selection()[0]  # Get selected item
        song_id = self.song_tree.item(item, "values")[0]  # Get the ID of the selected song

        # Fetch the file path of the selected song
        self.cursor.execute("SELECT file_path FROM songs WHERE id=?", (song_id,))
        file_path = self.cursor.fetchone()[0]

        # Close the database connection
        self.conn.close()

        # Open the AudioPlayer window and pass the file path
        audio_player_window = tk.Toplevel(self.root)
        audio_player = AudioPlayer(audio_player_window, file_path)

    def populate_songs(self):
        # Clear existing items
        for item in self.song_tree.get_children():
            self.song_tree.delete(item)

        # Fetch data from the database
        songs = self.db.fetch_songs()

        # Insert data into Treeview
        for song in songs:
            self.song_tree.insert("", "end", values=song)

    def populate_playlists(self):
        # Clear existing content in the playlist treeview
        self.playlist_tree.delete(*self.playlist_tree.get_children())

        # Fetch playlists from the database
        playlists = self.db.fetch_playlists()

        # Display playlists in the treeview
        for playlist in playlists:
            self.playlist_tree.insert("", "end", values=(playlist[0], playlist[1]))

    def show_selected_playlist_songs(self, event):
        for item in self.song_tree.get_children():
            self.song_tree.delete(item)

            # Get the selected playlist from the Treeview
        selected_item = self.playlist_tree.selection()

        if selected_item:
            # Get the playlist ID from the selected item
            playlist_id = self.playlist_tree.item(selected_item, "values")[0]

            # Fetch songs for the selected playlist from the database
            songs = self.db.fetch_songs_for_playlist_id(playlist_id)

            # Insert songs into the Treeview
            for song in songs:
                self.song_tree.insert("", "end", values=song)

    def show_add_playlist_gui(self):
        # Create a new window for adding a playlist
        add_playlist_window = tk.Toplevel(self.root)
        add_playlist_window.title("Add Playlist")

        # Create an instance of PlaylistGUI
        playlist_gui = PlaylistGUI(add_playlist_window, callback=self.populate_playlists)

    def show_add_song_gui(self):
        pass

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


if __name__ == "__main__":
    root = tk.Tk()
    main_page_gui = MainPageGUI(root)
    root.mainloop()
