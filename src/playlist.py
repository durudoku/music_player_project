import tkinter as tk
from database import Database

class PlaylistGUI:
    def __init__(self, root, callback):
        self.root = root
        self.root.title("Create Playlist")

        # Initialize database operations
        self.db = Database()

        # Callback function to update the main page after adding a new playlist
        self.callback = callback

        # Create GUI elements
        self.playlist_name_label = tk.Label(root, text="Playlist Name:")
        self.playlist_name_label.pack(pady=10)

        self.playlist_name_entry = tk.Entry(root)
        self.playlist_name_entry.pack(pady=10)

        self.create_button = tk.Button(root, text="Create Playlist", command=self.create_playlist)
        self.create_button.pack(pady=10)

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
    root = tk.Tk()
    playlist_gui = PlaylistGUI(root, callback=None)  # Pass the callback function if needed
    root.mainloop()