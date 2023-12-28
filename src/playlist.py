import tkinter as tk
from database import Database
import customtkinter as ctk


class PlaylistGUI:
    def __init__(self, root, callback):
        self.root = root
        self.root.title("Create Playlist")
        self.root.iconbitmap("icons/music.ico")
        self.root.geometry("250x100+100+100")

        # Initialize database operations
        self.db = Database()

        # Callback function to update the main page after adding a new playlist
        self.callback = callback

        # Create GUI elements
        self.playlist_name_label = ctk.CTkLabel(root, text="Playlist Name:")
        self.playlist_name_label.place(x=10, y=10)

        self.playlist_name_entry = ctk.CTkEntry(root)
        self.playlist_name_entry.place(x=100, y=10)

        self.create_button = ctk.CTkButton(root, text="Create Playlist", command=self.create_playlist)
        self.create_button.place(x=60, y=50)

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
