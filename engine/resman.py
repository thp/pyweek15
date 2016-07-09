import os
import glob
import pygame
from collections import defaultdict

FONT_SMALL, FONT_STD, FONT_BIG = FONTS = 25, 38, 90

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
        self.fonts = {size: pygame.font.Font(path('fonts', 'visitor2.ttf'), size) for size in FONTS}
        self.intermissions = {bn(fn): lines(fn) for fn in gb('intermissions', '*.txt')}
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

    def render_text(self, font, text):
        return self.upload_surface(self.fonts[font].render(text, True, (255, 255, 255)))

    def sfx(self, name):
        pygame.mixer.find_channel(True).play(self.sounds[name])

class Item(object):
    def __init__(self, name, is_enemy):
        self.name = name
        self.is_enemy = is_enemy

    def collide(self, player):
        if self.is_enemy:
            return player.crashed()
        elif self.name:
            player.picked_up(self.name)
            self.name = ''
        return False

class Level(object):
    ENEMIES, PICKUP, META, CONTENT = range(4)

    def __init__(self, leveldata, width=5):
        self.charmap = {}
        self.rows = []
        self.background = 'test'

        section = self.ENEMIES
        for line in leveldata:
            if line == '---':
                section += 1
            elif section < self.CONTENT:
                key, value = line.split('=', 1)
                if section in (self.ENEMIES, self.PICKUP):
                    self.charmap[key] = (value, section == self.ENEMIES)
                elif section == self.META and key == 'background':
                    self.background = value.strip()
            else:
                line = line + (' ' * width)
                self.rows.append([Item(*self.charmap[line[i]]) if line[i] != ' ' else None for i in range(width)])
