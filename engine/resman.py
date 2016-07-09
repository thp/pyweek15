import os
import glob
import pygame
from collections import defaultdict

FONT_STD = ("visitor2", 38)
FONT_SMALL = ("visitor2", 25)

class ResourceManager():
    def __init__(self, app):
        self.app = app

        bn = lambda fn: os.path.splitext(os.path.basename(fn))[0]
        path = lambda *args: os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data', *args)
        gb = lambda *args: glob.glob(path(*args))
        img = lambda fn: self.upload_surface(pygame.image.load(fn).convert_alpha())
        lines = lambda fn: open(fn).read().splitlines()

        self.sprites = {bn(fn): img(fn) for fn in gb('sprites', "*.png")}
        self.creatures = {bn(fn): img(fn) for fn in gb('creatures', "*.png")}
        self.fonts = {(name, size): pygame.font.Font(path('fonts', '%s.ttf' % name), size)
                      for name, size in (FONT_STD, FONT_SMALL)}
        self.intermissions = {bn(fn): open(fn).read().splitlines() for fn in gb('intermissions', '*.txt')}
        self.shaders = {os.path.basename(fn): open(fn).read() for fn in gb('shaders', '*.*')}
        self.sounds = {bn(fn): pygame.mixer.Sound(fn) for fn in gb('sounds', '*.wav')}

        self.backgrounds = defaultdict(list)
        for fn in sorted(gb('backgrounds', "*.jpg")):
            self.backgrounds[bn(fn).split('-')[0]].append(img(fn))

        self.levels = []
        for fn in sorted(gb("levels", "*.txt")):
            _, group, number = bn(fn).split('-')
            self.levels.append((int(group), int(number), lines(fn)))

        pickup_lines = [line.split(':') for line in lines(path('pickups.txt')) if not line.startswith('#')]
        self.pickups = {thingie: (sfx, int(coins), int(lives)) for thingie, sfx, coins, lives in pickup_lines}

    def upload_surface(self, surf):
        return self.app.renderer.upload_texture(surf.get_width(), surf.get_height(),
                                                pygame.image.tostring(surf, 'RGBA', 1))

    def sfx(self, name):
        pygame.mixer.find_channel(True).play(self.sounds[name])
