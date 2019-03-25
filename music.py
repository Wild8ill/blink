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
        self.music = simplegui.load_sound(self.song_dict.get("main"))
        self.music.set_volume(0.7)
        self.isPlaying = True

    def load_song(self, song):
        self.music = self.song_dict.get(song)

    def status(self):
        return self.isPlaying

    def play(self):
        self.isPlaying = False
        self.music.play()

    def stop(self):
        self.music.stop()