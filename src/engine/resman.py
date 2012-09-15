
import os
import glob
import pygame


class ResourceManager():
    def __init__(self, app):
        self.app = app
        self._surfaces = {}
        self._backgrounds = {}
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
        for fn in sorted(glob.glob(self._path('sprites', "*.png"))):
            bn, _ = os.path.splitext(os.path.basename(fn))
            surf = pygame.image.load(fn)
            surf = surf.convert_alpha()
            self._surfaces[bn] = surf

        ## load backgrounds
        for fn in sorted(glob.glob(self._path('backgrounds', "*.jpg"))):
            bn, _ = os.path.splitext(os.path.basename(fn))
            print bn
            surf = pygame.image.load(fn)
            self._backgrounds[bn] = surf

        import pygame.mixer as mixer

        ## load sfx
        for fn in glob.glob(self._path('sounds', "*.wav")):
            bn, _ = os.path.splitext(os.path.basename(fn))
            sound = mixer.Sound(fn)
            self._sounds[bn] = sound

        ## load levels
        for fn in glob.glob(self._path("levels", "*.txt")):
            bn, _ = os.path.splitext(os.path.basename(fn))
            level = None
            self._levels[bn] = level


    def get_sprite(self, name):
        return self._surfaces.get(name)

    def get_background(self, name):
        return self._backgrounds.get(name)

    def get_sound(self, name):
        return self._sounds[name]


    def font(self, font_spec):
        (name, size) = font_spec
        if not (name, size) in self._fonts:
            font = pygame.font.Font(self._path('fonts', '%s.ttf' % name), size)
            self._fonts[(name, size)] = font
        return self._fonts[(name, size)]
