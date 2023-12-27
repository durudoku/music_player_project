import sqlite3


class Database:
    def __init__(self):
        self.user_conn = sqlite3.connect("users.db")
        self.playlist_conn = sqlite3.connect("playlist.db")
        self.song_conn = sqlite3.connect("song.db")

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
        cursor = self.playlist_conn.cursor()
        cursor.execute('SELECT songs FROM playlists WHERE id=?', (playlist_id,))
        result = cursor.fetchone()

        if result and result[0]:
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

    def fetch_songs(self):
        cursor = self.song_conn.cursor()
        cursor.execute("SELECT * FROM songs")
        return cursor.fetchall()

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
            # If the playlist has existing songs
            playlist_songs = playlist_songs[0] + ',' + str(song_details['song_id'])
            cursor.execute('UPDATE playlists SET songs=? WHERE id=?', (playlist_songs, playlist_id))
        else:
            cursor.execute('UPDATE playlists SET songs=? WHERE id=?', (str(song_details['song_id']), playlist_id))

        self.playlist_conn.commit()

    # User Operations
    def create_table_users(self):
        cursor = self.user_conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                password TEXT
            )
        ''')
        self.user_conn.commit()

    def add_user(self, name, email, password):
        cursor = self.user_conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        self.user_conn.commit()

    def check_email_exists(self, email):
        cursor = self.user_conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        self.user_conn.commit()
        return user is not None

    def check_credentials(self, email, password):
        cursor = self.user_conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        self.user_conn.commit()
        return user is not None

    def get_all_users(self):
        cursor = self.user_conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()

    def remove_user(self, user_id):
        cursor = self.user_conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        self.user_conn.commit()


if __name__ == "__main__":
    db_instance = Database()
    db_instance.create_tables()
