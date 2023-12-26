import tkinter as tk
from tkinter import ttk, scrolledtext
from database import Database

class AddSongApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Song Database")

        self.db = Database()
        self.db.create_table_songs()

        self.setup_ui()
        self.load_songs()

    def setup_ui(self):
        ttk.Label(self.root, text="Track Name:").pack()
        self.track_name_entry = ttk.Entry(self.root)
        self.track_name_entry.pack()

        ttk.Label(self.root, text="Artist Name:").pack()
        self.artist_name_entry = ttk.Entry(self.root)
        self.artist_name_entry.pack()

        ttk.Label(self.root, text="Album Name:").pack()
        self.album_name_entry = ttk.Entry(self.root)
        self.album_name_entry.pack()

        ttk.Label(self.root, text="Duration (ms):").pack()
        self.duration_ms_entry = ttk.Entry(self.root)
        self.duration_ms_entry.pack()

        ttk.Label(self.root, text="File Path:").pack()
        self.file_path_entry = ttk.Entry(self.root)
        self.file_path_entry.pack()

        save_button = ttk.Button(self.root, text="Save", command=self.save_song_to_database)
        save_button.pack()

        delete_button = ttk.Button(self.root, text="Delete", command=self.delete_song)
        delete_button.pack()

        self.tree = ttk.Treeview(self.root, columns=("ID", "Track Name", "Artist Name", "Album Name", "Duration", "File Path"), show="headings")
        self.tree.pack(pady=10)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Track Name", text="Track Name")
        self.tree.heading("Artist Name", text="Artist Name")
        self.tree.heading("Album Name", text="Album Name")
        self.tree.heading("Duration", text="Duration (ms)")
        self.tree.heading("File Path", text="File Path")

        # Set column widths
        self.tree.column("ID", width=30)
        self.tree.column("Track Name", width=150)
        self.tree.column("Artist Name", width=150)
        self.tree.column("Album Name", width=150)
        self.tree.column("Duration", width=80)
        self.tree.column("File Path", width=200)

        self.tree.bind("<Double-1>", self.edit_selected_song)

        self.file_path_details = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=40, height=5)
        self.file_path_details.pack()

        self.file_path_details.bind("<Button-1>", self.clear_and_unfocus)

    def clear_and_unfocus(self, event):
        self.clear_entry_fields()

        self.tree.selection_remove(self.tree.selection())

    def load_songs(self):
        # Clear existing items in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load existing songs from the database and populate the Treeview
        songs = self.db.get_all_songs()
        for song in songs:
            self.tree.insert("", "end", values=song)

    def save_song_to_database(self):
        track_name = self.track_name_entry.get()
        artist_name = self.artist_name_entry.get()
        album_name = self.album_name_entry.get()
        duration_ms = self.duration_ms_entry.get()
        file_path = self.file_path_entry.get()

        # Get the selected song ID if there are selected items
        selected_items = self.tree.selection()
        if selected_items:
            song_id = self.tree.item(selected_items[0], "values")[0]
        else:
            song_id = None

        # Use the ID to update or create the song record
        self.db.update_or_save_song(song_id, track_name, artist_name, album_name, duration_ms, file_path)

        self.clear_entry_fields()
        self.load_songs()

    def clear_entry_fields(self):
        self.track_name_entry.delete(0, tk.END)
        self.artist_name_entry.delete(0, tk.END)
        self.album_name_entry.delete(0, tk.END)
        self.duration_ms_entry.delete(0, tk.END)
        self.file_path_entry.delete(0, tk.END)

    def edit_selected_song(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            song_details = self.tree.item(item, "values")

            # Populate entry fields and ScrolledText with selected song details
            self.track_name_entry.delete(0, tk.END)
            self.track_name_entry.insert(0, song_details[1])

            self.artist_name_entry.delete(0, tk.END)
            self.artist_name_entry.insert(0, song_details[2])

            self.album_name_entry.delete(0, tk.END)
            self.album_name_entry.insert(0, song_details[3])

            self.duration_ms_entry.delete(0, tk.END)
            self.duration_ms_entry.insert(0, song_details[4])

            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, song_details[5])

            self.file_path_details.delete(1.0, tk.END)
            self.file_path_details.insert(tk.END, song_details[5])

    def delete_song(self):
        # Get selected items
        selected_items = self.tree.selection()

        # Check if there are selected items
        if selected_items:
            item = self.tree.item(selected_items[0], "values")
            song_id = item[0]

            # Delete the selected song
            self.db.delete_song(song_id)

            # Reload songs after deletion
            self.load_songs()


if __name__ == "__main__":
    root = tk.Tk()
    app = AddSongApp(root)
    root.mainloop()
