
import os
import glob
import pygame


def resource_path(relative):
    basedir = os.path.join(os.getcwd())
    return os.path.join(
        basedir,
        relative
    )


class ResourceManager():
    LOCATION_SPRITES = resource_path("data/sprites")
    LOCATION_SOUNDS = resource_path("data/sounds")

    def __init__(self, app):
        self.app = app
        self._surfaces = {}
        self._sounds = {}
        self._load_all()

    def _load_all(self):
        ## load sprites
        ext = ".png"
        for fn in glob.glob(ResourceManager.LOCATION_SPRITES + "/*%s" % ext):
            bn = os.path.basename(fn).replace(ext, "")
            surf = pygame.image.load(fn)
            surf = surf.convert_alpha()
            self._surfaces[bn] = surf

        import pygame.mixer as mixer

        ## load sfx
        ext = ".wav"
        for fn in glob.glob(ResourceManager.LOCATION_SOUNDS + "/*%s" % ext):
            bn = os.path.basename(fn).replace(ext, "")
            sound = mixer.Sound(fn)
            self._sounds[bn] = sound

    def get_sprite(self, name):
        return self._surfaces[name]

    def get_sound(self, name):
        return self._sounds[name]
