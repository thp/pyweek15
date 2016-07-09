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
        self._fonts = {}

        current_dir = os.path.abspath(os.path.dirname(__file__))

        def _path(*relative):
            return os.path.join(current_dir, '..', '..', 'data', *relative)

        ## load sprites
        for fn in sorted(glob.glob(_path('sprites', "*.png"))):
            bn, _ = os.path.splitext(os.path.basename(fn))
            surf = pygame.image.load(fn).convert_alpha()
            surf = self.app.renderer.register_sprite(bn, surf)
            self._surfaces[bn] = surf

        ## load backgrounds
        for fn in sorted(glob.glob(_path('backgrounds', "*.jpg"))):
            bn, _ = os.path.splitext(os.path.basename(fn))
            key, frame = bn.split('-')
            surf = self.app.renderer.register_sprite(bn, pygame.image.load(fn))
            if key in self._backgrounds:
                self._backgrounds[key].append(surf)
            else:
                self._backgrounds[key] = [surf]

        ## load intermission assets
        for fn in glob.glob(_path('creatures', "*.png")):
            bn, _ = os.path.splitext(os.path.basename(fn))
            surf = pygame.image.load(fn)
            surf = surf.convert_alpha()
            self._creatures[bn] = surf

        ## load sfx
        for fn in glob.glob(_path('sounds', '*.wav')):
            bn, _ = os.path.splitext(os.path.basename(fn))
            self.app.audman.register_sound(bn, fn)

        ## load fonts
        name, size = FONT_STD
        font = pygame.font.Font(_path('fonts', '%s.ttf' % name), size)
        self._fonts[FONT_STD] = font

        name, size = FONT_SMALL
        font = pygame.font.Font(_path('fonts', '%s.ttf' % name), size)
        self._fonts[FONT_SMALL] = font

        ## load levels
        self.levels = []
        for fn in sorted(glob.glob(_path("levels", "*.txt"))):
            bn, _ = os.path.splitext(os.path.basename(fn))
            _, group, number = bn.split('-')
            self.levels.append((int(group), int(number), open(fn).read().splitlines()))

        ## load intermissions
        self.intermissions = {}
        for filename in glob.glob(_path('intermissions', '*.txt')):
            name, _ = os.path.splitext(os.path.basename(filename))
            self.intermissions[name] = open(filename).read().splitlines()

    def get_sprite(self, name):
        return self._surfaces.get(name)

    def get_background(self, name):
        return self._backgrounds.get(name)

    def get_creature(self, name):
        return self._creatures.get(name)

    def font(self, font_spec):
        return self._fonts[font_spec]
