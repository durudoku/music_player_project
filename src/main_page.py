import tkinter as tk
from tkinter import scrolledtext, ttk
from database import Database
from playlist import PlaylistGUI

class MainPageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Page")
        self.root.geometry("750x300+100+100")

        # Initialize database operations
        self.db = Database()

        # GUI Elements
        self.label_playlists = tk.Label(root, text="Playlists")
        self.label_playlists.place(x=10, y=30)

        # Create Treeview for playlists
        self.playlist_tree = ttk.Treeview(root, columns=("ID", "Name"), show="headings", selectmode="browse")
        self.playlist_tree.heading("ID", text="ID")
        self.playlist_tree.heading("Name", text="Name")
        self.playlist_tree.column("ID", width=50)
        self.playlist_tree.column("Name", width=200)
        self.playlist_tree.place(x=10, y=50)

        # Bind treeview selection event
        self.playlist_tree.bind("<ButtonRelease-1>", self.show_selected_playlist_songs)

        self.button_playlist_add = ttk.Button(root, text="+", width=5, command=self.show_add_playlist_gui)
        self.button_playlist_add.place(x=270, y=65)

        self.button_playlist_remove = ttk.Button(root, text="-", width=5, command=self.remove_selected_playlist)
        self.button_playlist_remove.place(x=270, y=170)

        self.label_songs = tk.Label(root, text="Songs")
        self.label_songs.place(x=330, y=30)

        self.song_listbox = scrolledtext.ScrolledText(root, width=40, height=10, state=tk.DISABLED)
        self.song_listbox.place(x=330, y=50)

        self.button_song_add = ttk.Button(root, text="+", width=5, command=self.show_add_song_gui)
        self.button_song_add.place(x=670, y=65)

        self.button_song_remove = ttk.Button(root, text="-", width=5)
        self.button_song_remove.place(x=670, y=170)

        # Populate playlists
        self.populate_playlists()

    def populate_playlists(self):
        # Clear existing content in the playlist treeview
        self.playlist_tree.delete(*self.playlist_tree.get_children())

        # Fetch playlists from the database
        playlists = self.db.fetch_playlists()

        # Display playlists in the treeview
        for playlist in playlists:
            self.playlist_tree.insert("", "end", values=(playlist[0], playlist[1]))

    def show_selected_playlist_songs(self, event):
        # Get the selected item in the treeview
        selected_item = self.playlist_tree.selection()

        if selected_item:
            # Get the playlist ID from the selected item
            playlist_id = self.playlist_tree.item(selected_item, "values")[0]

            # Fetch songs for the selected playlist from the database
            songs = self.db.fetch_songs_for_playlist_id(playlist_id)

            # Display songs in the listbox
            self.song_listbox.config(state=tk.NORMAL)
            self.song_listbox.delete(1.0, tk.END)
            # Display songs in the listbox
            if songs:
                for song in songs.split(','):
                    self.song_listbox.insert(tk.END, f"{song}\n")
            self.song_listbox.config(state=tk.DISABLED)

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
