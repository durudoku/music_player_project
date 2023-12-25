import sqlite3

class Database:
    def __init__(self):
        self.user_conn = sqlite3.connect("users.db")
        self.playlist_conn = sqlite3.connect("playlist.db")
        self.song_conn = sqlite3.connect("song.db")
        self.conn = sqlite3.connect("music.db")

    def create_tables(self):
        self.create_table_users()
        self.create_table_playlists()
        self.create_table_songs()

    # Playlist Operations
    def create_table_playlists(self):
        connection = self.playlist_conn
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS playlists (id INTEGER PRIMARY KEY, name TEXT, songs TEXT)")
        connection.commit()

    def add_playlist(self, name, songs=None):
        cursor = self.playlist_conn.cursor()
        songs = songs if songs is not None else ""
        cursor.execute("INSERT INTO playlists (name, songs) VALUES (?, ?)", (name, songs))
        self.playlist_conn.commit()

    def remove_playlist(self, playlist_id):
        cursor = self.playlist_conn.cursor()
        cursor.execute("DELETE FROM playlists WHERE id=?", (playlist_id,))
        self.playlist_conn.commit()

    def fetch_playlists(self):
        connection = self.playlist_conn
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM playlists")
        playlists = cursor.fetchall()
        return playlists

    # Song Operations
    def create_table_songs(self):
        connection = self.song_conn
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY, name TEXT, artist TEXT, playlist TEXT)")
        connection.commit()

    def create_table_playlist_songs(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS playlist_songs (playlist_id INTEGER, song_id INTEGER, FOREIGN KEY(playlist_id) REFERENCES playlists(id), FOREIGN KEY(song_id) REFERENCES songs(id), PRIMARY KEY(playlist_id, song_id))")
        self.conn.commit()

    def fetch_songs_for_playlist_id(self, playlist_id):
        cursor = self.playlist_conn.cursor()
        cursor.execute("SELECT * FROM playlists WHERE id=?", (playlist_id,))
        playlist = cursor.fetchone()
        if playlist:
            return playlist[2]  # Assuming songs are stored in the third column (index 2)
        else:
            return None

    @staticmethod
    def create_table_users():
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, password TEXT)"
        )
        connection.commit()
        connection.close()

    @staticmethod
    def add_user(name, email, password):
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        connection.commit()
        connection.close()

    @staticmethod
    def check_email_exists(email):
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        connection.close()
        return user is not None

    @staticmethod
    def check_credentials(email, password):
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        connection.close()
        return user is not None

if __name__ == "__main__":
    db_instance = Database()
    db_instance.create_tables()
