import tkinter as tk
import pygame
from PIL import Image, ImageTk

class AudioPlayer:
    def __init__(self, root, file_path):
        self.root = root
        self.root.title("Audio Player")
        self.root.geometry("300x300+100+100")

        file_path = "songs/" + file_path + ".mp3"
        image_path = "album_covers/" + file_path + ".jpg"

        # Initialize Pygame
        pygame.init()
        print(file_path)
        # Load the selected song
        pygame.mixer.music.load(file_path)

        # Play the song
        pygame.mixer.music.play()

        self.image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(self.image)

        # Create a label to display the image
        self.image_label = tk.Label(root, image=self.photo)
        self.image_label.pack(padx=10, pady=10)

        # Button to stop the song
        stop_button = tk.Button(root, text="Stop", command=self.stop_song)
        stop_button.pack(pady=10)

        restart_button = tk.Button(root, text="Restart", command=self.restart)
        restart_button.pack(pady=10)

        # Bind the window close event to stop the song and close the Pygame mixer
        root.protocol("WM_DELETE_WINDOW", self.on_close)

    def stop_song(self):
        pygame.mixer.music.stop()

    def restart(self):
        pygame.mixer.music.play()

    def on_close(self):
        # Stop the song and quit Pygame
        pygame.mixer.music.stop()
        pygame.quit()
        self.root.destroy()
