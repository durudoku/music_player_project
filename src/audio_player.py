import tkinter as tk
import pygame
from PIL import Image, ImageTk

class AudioPlayer:
    def __init__(self, root, file_path, main_page_app):
        self.root = root
        self.root.title("Audio Player")
        self.root.geometry("300x300+100+100")

        self.main_page_app = main_page_app

        image_path = "album_covers/" + file_path + ".jpg"
        file_path = "songs/" + file_path + ".mp3"

        # Pygame
        pygame.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        # Image
        original_image = Image.open(image_path)
        resized_image = original_image.copy()
        resized_image.thumbnail((100, 100))

        self.photo = ImageTk.PhotoImage(resized_image)
        self.image_label = tk.Label(root, image=self.photo)
        self.image_label.pack(padx=10, pady=10)

        stop_button = tk.Button(root, text="Stop", command=self.stop_song)
        stop_button.pack(pady=10)

        restart_button = tk.Button(root, text="Restart", command=self.restart)
        restart_button.pack(pady=10)

        root.protocol("WM_DELETE_WINDOW", self.on_close)

    def stop_song(self):
        pygame.mixer.music.stop()

    def restart(self):
        pygame.mixer.music.play()

    def on_close(self):
        # Stop the song and quit Pygame
        pygame.mixer.music.stop()
        pygame.quit()

        # Close the root window
        self.root.destroy()

        # Update the reference in the MainPageApp to None
        if self.main_page_app:
            self.main_page_app.current_audio_player = None

if __name__ == "__main__":
    root = tk.Tk()
    file_path = "songs/joga.mp3"  # Provide a default song path
    audio_player = AudioPlayer(root, file_path, main_page_app=None)  # Set main_page_app to None initially
    root.mainloop()