class AudioManager:
    def __init__(self, app):
        self.app = app
        self.channels = []

        import pygame.mixer as mixer

        c = mixer.Channel(0)
        self.channels.append(c)
        c = mixer.Channel(1)
        self.channels.append(c)

    def sfx(self, name, channel_nr=0):
        sound = self.app.resman.get_sound(name)
        channel = self.channels[channel_nr]
        channel.play(sound)
