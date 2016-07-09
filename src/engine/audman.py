import pygame.mixer as mixer

class AudioManager:
    def __init__(self, app):
        self.app = app
        self.sounds = {}

    def register_sound(self, name, filename):
        self.sounds[name] = mixer.Sound(filename)

    def sfx(self, name):
        mixer.find_channel(True).play(self.sounds[name])
