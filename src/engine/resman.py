import os
import glob
import pygame
import sys

FONT_STD = ("visitor2", 38)
FONT_SMALL = ("visitor2", 25)

import pygame.mixer as mixer

class AudioManager():
    def __init__(self, app):
        self.app = app
        self.sounds = {}

    def register_sound(self, name, filename):
        self.sounds[name] = mixer.Sound(filename)

    def sfx(self, name):
        mixer.find_channel(True).play(self.sounds[name])


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

        for fn in sorted(glob.glob(_path('sprites', "*.png"))):
            bn, _ = os.path.splitext(os.path.basename(fn))
            surf = pygame.image.load(fn).convert_alpha()
            surf = self.app.renderer.register_sprite(bn, surf)
            self._surfaces[bn] = surf

        for fn in sorted(glob.glob(_path('backgrounds', "*.jpg"))):
            bn, _ = os.path.splitext(os.path.basename(fn))
            key, frame = bn.split('-')
            surf = self.app.renderer.register_sprite(bn, pygame.image.load(fn))
            if key in self._backgrounds:
                self._backgrounds[key].append(surf)
            else:
                self._backgrounds[key] = [surf]

        for fn in glob.glob(_path('creatures', "*.png")):
            bn, _ = os.path.splitext(os.path.basename(fn))
            surf = pygame.image.load(fn)
            surf = surf.convert_alpha()
            self._creatures[bn] = surf

        for fn in glob.glob(_path('sounds', '*.wav')):
            bn, _ = os.path.splitext(os.path.basename(fn))
            self.app.audman.register_sound(bn, fn)

        for name, size in (FONT_STD, FONT_SMALL):
            self._fonts[(name, size)] = pygame.font.Font(_path('fonts', '%s.ttf' % name), size)

        name, size = FONT_SMALL
        font = pygame.font.Font(_path('fonts', '%s.ttf' % name), size)
        self._fonts[FONT_SMALL] = font

        self.levels = []
        for fn in sorted(glob.glob(_path("levels", "*.txt"))):
            bn, _ = os.path.splitext(os.path.basename(fn))
            _, group, number = bn.split('-')
            self.levels.append((int(group), int(number), open(fn).read().splitlines()))

        self.intermissions = {}
        for filename in glob.glob(_path('intermissions', '*.txt')):
            name, _ = os.path.splitext(os.path.basename(filename))
            self.intermissions[name] = open(filename).read().splitlines()

        self._shaders = {}
        for filename in glob.glob(_path('shaders', '*.*')):
            self._shaders[os.path.basename(filename)] = open(filename).read()

    def get_sprite(self, name):
        return self._surfaces.get(name)

    def get_background(self, name):
        return self._backgrounds.get(name)

    def get_creature(self, name):
        return self._creatures.get(name)

    def get_shader(self, name):
        return self._shaders.get(name)

    def font(self, font_spec):
        return self._fonts[font_spec]
