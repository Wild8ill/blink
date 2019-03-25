try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class Music:
    def __init__(self):
        self.song_dict = {
            "main": "https://storage.googleapis.com/cs1830/The%20Show%20Must%20Be%20Go.mp3",
            "cool": "music/song2.mpg"
        }
        # Music Setup
        self.currentSong = self.song_dict.get("cool") # The Current Song Address
        self.song = simplegui.load_sound(self.currentSong) # The Current Song Loaded

        # Default Song
        self.song.set_volume(0.7)
        self.isPlaying = False

    # Load the song
    def load_song(self, song):
        self.currentSong = self.song_dict.get(song)
        self.song = simplegui.load_sound(self.currentSong)

    def status(self):
        return self.isPlaying

    # Play the song
    def play_song(self):
        self.isPlaying = True
        self.song.play()

    # Stop the song
    def stop_song(self):
        self.isPlaying = False
        self.song.stop()