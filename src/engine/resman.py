
import os
import glob
import pygame
import sys

FONT_STD = ("visitor2", 38)
FONT_SMALL = ("visitor2", 25)


class ResourceManager():
    def __init__(self, app):
        self.app = app
        self._surfaces = {}
        self._backgrounds = {}
        self._creatures = {}
        self._sounds = {}
        self._fonts = {}

        current_dir = os.path.abspath(os.path.dirname(__file__))
        self.rsrc_dir = os.path.join(current_dir, '..', '..', 'data')
        if getattr(sys, 'frozen', None):
            self.rsrc_dir = os.path.join(sys._MEIPASS, 'data')  # pyInstaller production environment

        self._load_all()

    def _path(self, *relative):
        return os.path.join(self.rsrc_dir, *relative)

    def _load_all(self):
        ## load sprites
        for fn in sorted(glob.glob(self._path('sprites', "*.png"))):
            bn, _ = os.path.splitext(os.path.basename(fn))
            surf = pygame.image.load(fn).convert_alpha()
            surf = self.app.renderer.register_sprite(bn, surf)
            self._surfaces[bn] = surf

        ## load backgrounds
        for fn in sorted(glob.glob(self._path('backgrounds', "*.jpg"))):
            bn, _ = os.path.splitext(os.path.basename(fn))
            key, frame = bn.split('-')
            surf = self.app.renderer.register_sprite(bn, pygame.image.load(fn))
            if key in self._backgrounds:
                self._backgrounds[key].append(surf)
            else:
                self._backgrounds[key] = [surf]

        ## load intermission assets
        for fn in glob.glob(self._path('creatures', "*.png")):
            bn, _ = os.path.splitext(os.path.basename(fn))
            surf = pygame.image.load(fn)
            surf = surf.convert_alpha()
            self._creatures[bn] = surf


        import pygame.mixer as mixer

        ## load sfx (wav and optionally ogg files if they exist)
        for extension in ('*.wav', '*.ogg'):
            for fn in glob.glob(self._path('sounds', extension)):
                bn, _ = os.path.splitext(os.path.basename(fn))
                sound = mixer.Sound(fn)
                self._sounds[bn] = sound

        ## load fonts
        name, size = FONT_STD
        font = pygame.font.Font(self._path('fonts', '%s.ttf' % name), size)
        self._fonts[FONT_STD] = font

        name, size = FONT_SMALL
        font = pygame.font.Font(self._path('fonts', '%s.ttf' % name), size)
        self._fonts[FONT_SMALL] = font

        ## load levels
        self.levels = []

        for fn in sorted(glob.glob(self._path("levels", "*.txt"))):
            bn, _ = os.path.splitext(os.path.basename(fn))
            _, group, number = bn.split('-')
            self.levels.append((int(group), int(number)))

        ## load intermissions
        self.intermissions = {}
        for filename in glob.glob(self._path('intermissions', '*.txt')):
            name, _ = os.path.splitext(os.path.basename(filename))
            self.intermissions[name] = open(filename).read().splitlines()

    def get_sprite(self, name):
        return self._surfaces.get(name)

    def get_background(self, name):
        return self._backgrounds.get(name)

    def get_creature(self, name):
        return self._creatures.get(name)

    def get_sound(self, name):
        return self._sounds[name]


    def font(self, font_spec):
        return self._fonts[font_spec]
