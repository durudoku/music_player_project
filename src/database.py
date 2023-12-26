import sqlite3
import json

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
        cursor = self.playlist_conn.cursor()
        cursor.execute("SELECT * FROM playlists")
        return cursor.fetchall()

    def get_playlist_songs(self, playlist_id):
        # Retrieve song IDs for a playlist
        cursor = self.playlist_conn.cursor()
        cursor.execute('SELECT songs FROM playlists WHERE id=?', (playlist_id,))
        result = cursor.fetchone()

        if result and result[0]:
            # Split the comma-separated string, filter out empty strings, and convert to a list of integers
            song_ids = [int(song_id) for song_id in result[0].split(',') if song_id]
            return song_ids
        else:
            return []

    # Song Operations
    def create_table_songs(self):
        cursor = self.song_conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY,
                track_name TEXT,
                artist_name TEXT,
                album_name TEXT,
                duration_ms INTEGER,
                file_path TEXT
            )
        ''')
        self.song_conn.commit()

    def create_table_playlist_songs(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS playlist_songs (playlist_id INTEGER, song_id INTEGER, FOREIGN KEY(playlist_id) REFERENCES playlists(id), FOREIGN KEY(song_id) REFERENCES songs(id), PRIMARY KEY(playlist_id, song_id))")
        self.conn.commit()

    def fetch_songs(self):
        cursor = self.song_conn.cursor()
        cursor.execute("SELECT * FROM songs")
        return cursor.fetchall()

    def get_song_by_track_name(self, track_name):
        cursor = self.song_conn.cursor()
        cursor.execute('SELECT * FROM songs WHERE track_name = ?', (track_name,))
        return cursor.fetchone()

    def get_song_by_id(self, song_id):
        cursor = self.song_conn.cursor()
        cursor.execute('SELECT * FROM songs WHERE id = ?', (song_id,))
        return cursor.fetchone()

    def update_or_save_song(self, song_id, track_name, artist_name, album_name, duration_ms, file_path):
        existing_song = self.get_song_by_id(song_id)

        if existing_song:
            # Song already exists, update the existing record
            self.update_song(song_id, track_name, artist_name, album_name, duration_ms, file_path)
        else:
            # Song doesn't exist, create a new record
            self.save_song(track_name, artist_name, album_name, duration_ms, file_path)

    def save_song(self, track_name, artist_name, album_name, duration_ms, file_path):
        cursor = self.song_conn.cursor()
        cursor.execute('''
            INSERT INTO songs (track_name, artist_name, album_name, duration_ms, file_path)
            VALUES (?, ?, ?, ?, ?)
        ''', (track_name, artist_name, album_name, duration_ms, file_path))
        self.song_conn.commit()

    def update_song(self, song_id, track_name, artist_name, album_name, duration_ms, file_path):
        cursor = self.song_conn.cursor()
        cursor.execute('''
            UPDATE songs
            SET track_name=?, artist_name=?, album_name=?, duration_ms=?, file_path=?
            WHERE id=?
        ''', (track_name, artist_name, album_name, duration_ms, file_path, song_id))
        self.song_conn.commit()

    def get_all_songs(self):
        cursor = self.song_conn.cursor()
        cursor.execute('SELECT * FROM songs')
        return cursor.fetchall()

    def delete_song(self, song_id):
        cursor = self.song_conn.cursor()
        cursor.execute('DELETE FROM songs WHERE id = ?', (song_id,))
        self.song_conn.commit()

    def add_song_to_playlist(self, playlist_id, song_details):
        cursor = self.playlist_conn.cursor()
        cursor.execute('SELECT songs FROM playlists WHERE id=?', (playlist_id,))
        playlist_songs = cursor.fetchone()

        if playlist_songs:
            # If the playlist has existing songs, update the songs list
            playlist_songs = playlist_songs[0] + ',' + str(song_details['song_id'])
            cursor.execute('UPDATE playlists SET songs=? WHERE id=?', (playlist_songs, playlist_id))
        else:
            # If the playlist has no existing songs, create a new list with the current song
            cursor.execute('UPDATE playlists SET songs=? WHERE id=?', (str(song_details['song_id']), playlist_id))

        # Commit the changes manually
        self.playlist_conn.commit()


    # User Operations
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
