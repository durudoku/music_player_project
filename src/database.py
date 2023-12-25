import sqlite3

class Database:
    @staticmethod
    def create_table():
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
    Database.create_table()
