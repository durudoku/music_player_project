import tkinter as tk
import pygame

class AudioPlayer:
    def __init__(self, root, file_path):
        self.root = root
        self.root.title("Audio Player")
        self.root.geometry("300x300+100+100")

        # Initialize Pygame
        pygame.init()

        # Load the selected song
        pygame.mixer.music.load(file_path)

        # Play the song
        pygame.mixer.music.play()

        # Button to stop the song
        stop_button = tk.Button(root, text="Stop", command=self.stop_song)
        stop_button.pack(pady=10)

        # Bind the window close event to stop the song and close the Pygame mixer
        root.protocol("WM_DELETE_WINDOW", self.on_close)



    def stop_song(self):
        pygame.mixer.music.stop()

    def on_close(self):
        # Stop the song and quit Pygame
        pygame.mixer.music.stop()
        pygame.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    file_path = "songs/joga.mp3"  # Provide a default song path
    audio_player = AudioPlayer(root, file_path)
    root.mainloop()
