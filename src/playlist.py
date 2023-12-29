import tkinter as tk
from database import Database
import customtkinter as ctk


class PlaylistGUI:
    def __init__(self, root, callback):
        self.root = root
        self.root.title("Create Playlist")
        self.root.iconbitmap("icons/music.ico")

        # Initialize database operations
        self.db = Database()

        # Callback function to update the main page after adding a new playlist
        self.callback = callback

        # Create GUI elements
        self.playlist_name_label = ctk.CTkLabel(root, text="Playlist Name:")
        self.playlist_name_label.grid(column=0, row=0, padx=15, pady=15, sticky="w")

        self.playlist_name_entry = ctk.CTkEntry(root)
        self.playlist_name_entry.grid(column=1, row=0, padx=15, pady=15, sticky="w")

        self.create_button = ctk.CTkButton(root, text="Create Playlist", command=self.create_playlist)
        self.create_button.grid(column=0, row=1, columnspan=2, padx=15, pady=(0, 15), sticky="we")

    def create_playlist(self):
        playlist_name = self.playlist_name_entry.get()

        if playlist_name:
            # Add the playlist to the database
            self.db.add_playlist(playlist_name)

            # Call the callback function to update the main page
            if self.callback:
                self.callback()

            # Close the playlist creation window
            self.root.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    playlist_gui = PlaylistGUI(root, callback=None)  # Pass the callback function if needed
    root.mainloop()
