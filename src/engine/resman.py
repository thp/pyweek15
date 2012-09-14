
import os
import glob
import pygame


class ResourceManager():
    def __init__(self, app):
        self.app = app
        self._surfaces = {}
        self._sounds = {}
        self._fonts = {}
        self._levels = {}

        current_dir = os.path.abspath(os.path.dirname(__file__))
        self.rsrc_dir = os.path.join(current_dir, '..', '..', 'data')

        self._load_all()

    def _path(self, *relative):
        return os.path.join(self.rsrc_dir, *relative)


    def _load_all(self):
        ## load sprites
        ext = ".png"
        for fn in glob.glob(self._path('sprites') + "/*%s" % ext):
            bn = os.path.basename(fn).replace(ext, "")
            surf = pygame.image.load(fn)
            surf = surf.convert_alpha()
            self._surfaces[bn] = surf

        import pygame.mixer as mixer

        ## load sfx
        ext = ".wav"
        for fn in glob.glob(self._path('sounds') + "/*%s" % ext):
            bn = os.path.basename(fn).replace(ext, "")
            sound = mixer.Sound(fn)
            self._sounds[bn] = sound

        ## load levels
        ext = ".txt"
        for fn in glob.glob(self._path("levels") + "/*%s" % ext):
            bn = os.path.basename(fn).replace(ext, "")
            level = None
            self._levels[bn] = level


    def get_sprite(self, name):
        return self._surfaces.get(name)

    def get_sound(self, name):
        return self._sounds[name]

    def load_font(self, name, size):
        font = pygame.font.Font(self._path('fonts', '%s.ttf' % name), size)
        self._fonts["%s_%s" % (name, size)] = font

    def get_font(self, name):
        return self._fonts[name]
