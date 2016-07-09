import os
import glob
import pygame

FONT_STD = ("visitor2", 38)
FONT_SMALL = ("visitor2", 25)

class AudioManager():
    def __init__(self, app):
        self.app = app
        self.sounds = {}

    def register_sound(self, name, filename):
        self.sounds[name] = pygame.mixer.Sound(filename)

    def sfx(self, name):
        pygame.mixer.find_channel(True).play(self.sounds[name])


class ResourceManager():
    def __init__(self, app):
        self.app = app
        self.sprites = {}
        self.backgrounds = {}
        self.creatures = {}
        self.fonts = {}

        current_dir = os.path.abspath(os.path.dirname(__file__))

        def _path(*relative):
            return os.path.join(current_dir, '..', 'data', *relative)

        for fn in sorted(glob.glob(_path('sprites', "*.png"))):
            bn, _ = os.path.splitext(os.path.basename(fn))
            surf = self.upload_surface(pygame.image.load(fn).convert_alpha())
            self.sprites[bn] = surf

        for fn in sorted(glob.glob(_path('backgrounds', "*.jpg"))):
            bn, _ = os.path.splitext(os.path.basename(fn))
            key, frame = bn.split('-')
            surf = self.upload_surface(pygame.image.load(fn).convert_alpha())
            if key in self.backgrounds:
                self.backgrounds[key].append(surf)
            else:
                self.backgrounds[key] = [surf]

        for fn in glob.glob(_path('creatures', "*.png")):
            bn, _ = os.path.splitext(os.path.basename(fn))
            surf = pygame.image.load(fn)
            surf = surf.convert_alpha()
            self.creatures[bn] = self.upload_surface(surf)

        for fn in glob.glob(_path('sounds', '*.wav')):
            bn, _ = os.path.splitext(os.path.basename(fn))
            self.app.audman.register_sound(bn, fn)

        for name, size in (FONT_STD, FONT_SMALL):
            self.fonts[(name, size)] = pygame.font.Font(_path('fonts', '%s.ttf' % name), size)

        self.levels = []
        for fn in sorted(glob.glob(_path("levels", "*.txt"))):
            bn, _ = os.path.splitext(os.path.basename(fn))
            _, group, number = bn.split('-')
            self.levels.append((int(group), int(number), open(fn).read().splitlines()))

        self.intermissions = {os.path.splitext(os.path.basename(filename))[0]: open(filename).read().splitlines()
                              for filename in glob.glob(_path('intermissions', '*.txt'))}

        self.shaders = {os.path.basename(filename): open(filename).read()
                        for filename in glob.glob(_path('shaders', '*.*'))}

        pickup_lines = [line.strip().split(':') for line in open(_path('pickups.txt')) if not line.startswith('#')]
        self.pickups = {thingie: (sfx, int(coins), int(lives)) for thingie, sfx, coins, lives in pickup_lines}

    def upload_surface(self, surf):
        return self.app.renderer.upload_texture(surf.get_width(), surf.get_height(),
                                                pygame.image.tostring(surf, 'RGBA', 1))
