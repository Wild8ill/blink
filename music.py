try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class Music:
    def __init__(self):
        self.song_dict = {
            "1": "http://commondatastorage.googleapis.com/blink-asset/city.ogg",
            "2": "http://commondatastorage.googleapis.com/blink-asset/song2.ogg",
            "3": "http://commondatastorage.googleapis.com/blink-asset/song3.ogg"
        }
        # Music Setup
        self.currentSong = self.song_dict.get("2") # The Current Song Address
        self.song = simplegui.load_sound(self.currentSong) # The Current Song Loaded

        # Default Song
        self.song.set_volume(0.1)
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