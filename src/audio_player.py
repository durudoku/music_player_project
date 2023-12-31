import tkinter as tk
from tkinter import ttk
import pygame
from PIL import Image, ImageTk
import customtkinter as ctk


class AudioPlayer:
    def __init__(self, root, file_path, main_page_app, track_name):
        self.root = root
        self.root.title("Audio Player")
        self.root.iconbitmap("icons/music.ico")

        self.main_page_app = main_page_app

        image_path = "album_covers/" + file_path + ".jpg"
        file_path = "songs/" + file_path + ".mp3"

        pygame.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        original_image = Image.open(image_path)
        resized_image = original_image.copy()
        resized_image.thumbnail((100, 100))

        self.photo = ImageTk.PhotoImage(resized_image)
        self.image_label = tk.Label(root, image=self.photo)
        self.image_label.grid(row=0, column=0, columnspan=3, pady=15, sticky="we")

        img_pause = ctk.CTkImage(Image.open("button_images/pause.png"))
        img_play = ctk.CTkImage(Image.open("button_images/play.png"))
        img_rewind = ctk.CTkImage(Image.open("button_images/rewind.png"))

        label_song_name = ctk.CTkLabel(root, text="Playing Now:\n" + track_name)
        label_song_name.grid(row=1, column=0, columnspan=3, pady=15, sticky="we")

        pause_button = ctk.CTkButton(root, text="", image=img_pause, command=self.pause_song, width=5)
        pause_button.grid(row=2, column=0, columnspan=1, pady=15, padx=(50, 0))

        unpause_button = ctk.CTkButton(root, text="", image=img_play, command=self.unpause_song, width=5)
        unpause_button.grid(row=2, column=1, columnspan=1, pady=15)

        restart_button = ctk.CTkButton(root, text="", image=img_rewind, command=self.restart, width=5)
        restart_button.grid(row=2, column=2, columnspan=1, pady=15, padx=(0, 50))

        root.protocol("WM_DELETE_WINDOW", self.on_close)

    def pause_song(self):
        pygame.mixer.music.pause()

    def unpause_song(self):
        pygame.mixer.music.unpause()

    def restart(self):
        pygame.mixer.music.play()

    def on_close(self):
        # Stop the song and quit Pygame
        pygame.mixer.music.stop()
        pygame.quit()

        # Close root window
        self.root.destroy()

        if self.main_page_app:
            self.main_page_app.current_audio_player = None


if __name__ == "__main__":
    root = ctk.CTk()
    file_path = "songs/joga.mp3"  # Provide a default song path
    audio_player = AudioPlayer(root, file_path, main_page_app=None)  # Set main_page_app to None initially
    root.mainloop()
