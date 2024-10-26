import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import pygame
import os
from PIL import Image, ImageTk
import time

class Node:
    def __init__(self, song_path):
        self.song_path = song_path
        self.song_name = os.path.basename(song_path)
        self.next = None
        self.prev = None


class Playlist:
    def __init__(self):
        self.head = None
        self.current = None

    def add_song(self, song_path):
        new_node = Node(song_path)
        if not self.head:
            self.head = new_node
            self.current = self.head
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node
            new_node.prev = temp

    def play_song(self):
        if self.current:
            return self.current.song_path
        return None

    def next_song(self):
        if self.current and self.current.next:
            self.current = self.current.next
            return self.current.song_path
        return None

    def previous_song(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
            return self.current.song_path
        return None

    def get_current_song_name(self):
        if self.current:
            return self.current.song_name
        return "No song selected"

    def display_songs(self):
        songs = []
        temp = self.head
        while temp:
            songs.append(temp.song_name)
            temp = temp.next
        return songs


class MusicPlayerApp:
    def __init__(self, root):
        self.playlist = Playlist()
        self.is_paused = False
        self.song_length = 0
        pygame.mixer.init()


        root.title("Spotify-Like Music Player")
        root.geometry("600x700")
        root.configure(bg="#121212")  # Dark theme


        self.main_frame = tk.Frame(root, bg="lightblue", bd=5, relief="solid")
        self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)


        try:
            self.album_art = Image.open("im2.jpg").resize((200, 200))  # Try to load image
        except FileNotFoundError:

            self.album_art = Image.new('RGB', (200, 200), color=(73, 109, 137))  
        self.album_img = ImageTk.PhotoImage(self.album_art)
        self.album_label = tk.Label(self.main_frame, image=self.album_img, bg="lightblue")
        self.album_label.pack(pady=20)


        self.song_label = tk.Label(self.main_frame, text="No song selected", font=("Arial", 14), fg="lightblue")
        self.song_label.pack(pady=10)


        self.control_frame = tk.Frame(self.main_frame, bg="#1DB954")
        self.control_frame.pack(pady=20)


        button_style = {"bg": "#1DB954", "fg": "white", "font": ("Arial", 12), "bd": 0, "relief": "flat"}


        self.prev_button = tk.Button(self.control_frame, text="Prev", command=self.previous_song, **button_style)
        self.prev_button.grid(row=0, column=0, padx=20)

        self.play_button = tk.Button(self.control_frame, text="Play", command=self.play_or_pause_song, **button_style)
        self.play_button.grid(row=0, column=1, padx=20)

        self.next_button = tk.Button(self.control_frame, text="Next", command=self.next_song, **button_style)
        self.next_button.grid(row=0, column=2, padx=20)


        self.volume_slider = ttk.Scale(self.main_frame,from_=0, to_=1, orient="horizontal", command=self.set_volume)
        self.volume_slider.set(0.5)
        self.volume_slider.pack(pady=10)


        self.add_button = tk.Button(self.main_frame, text="Add Song", command=self.add_song, **button_style)
        self.add_button.pack(pady=5)

        self.display_button = tk.Button(self.main_frame, text="Display Playlist", command=self.display_playlist, **button_style)
        self.display_button.pack(pady=5)


        self.timer_label = tk.Label(self.main_frame, text="00:00", font=("Arial", 12), bg="#1DB954", fg="white")
        self.timer_label.pack(pady=5)


        for button in [self.play_button, self.prev_button, self.next_button, self.add_button, self.display_button]:
            button.bind("<Enter>", lambda e, b=button: b.config(bg="#158a48"))
            button.bind("<Leave>", lambda e, b=button: b.config(bg="#1DB954"))


    def add_song(self):
        song_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if song_path:
            self.playlist.add_song(song_path)
            messagebox.showinfo("Success", "Song added to playlist!")


    def play_or_pause_song(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.update_timer()
            self.play_button.config(text="Pause")
        else:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                self.is_paused = True
                self.play_button.config(text="Play")
            else:
                self.play_song()


    def play_song(self):
        song_path = self.playlist.play_song()
        if song_path:
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            self.is_paused = False
            self.song_length = pygame.mixer.Sound(song_path).get_length()
            self.update_song_label()
            self.play_button.config(text="Pause")
            self.update_timer()
        else:
            messagebox.showerror("Error", "No song to play!")


    def update_timer(self):
        if not self.is_paused:
            elapsed_time = pygame.mixer.music.get_pos() / 1000
            time_str = time.strftime('%M:%S', time.gmtime(elapsed_time))
            self.timer_label.config(text=time_str)
            if pygame.mixer.music.get_busy():
                self.timer_label.after(1000, self.update_timer)


    def next_song(self):
        song_path = self.playlist.next_song()
        if song_path:
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            self.is_paused = False
            self.play_button.config(text="Pause")
            self.update_song_label()
            self.update_timer()
        else:
            messagebox.showerror("Error", "No next song!")


    def previous_song(self):
        song_path = self.playlist.previous_song()
        if song_path:
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            self.is_paused = False
            self.play_button.config(text="Pause")
            self.update_song_label()
            self.update_timer()
        else:
            messagebox.showerror("Error", "No previous song!")


    def update_song_label(self):
        current_song_name = self.playlist.get_current_song_name()
        self.song_label.config(text=current_song_name)


    def display_playlist(self):
        songs = self.playlist.display_songs()
        playlist_text = "\n".join(songs) if songs else "No songs in the playlist."
        messagebox.showinfo("Playlist", playlist_text)


    def set_volume(self, value):
        pygame.mixer.music.set_volume(float(value))


root = tk.Tk()
app = MusicPlayerApp(root)
root.mainloop()
