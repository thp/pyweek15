from core import Image, Font, Sound, VFS

FONT_SMALL, FONT_STD, FONT_BIG = FONTS = 1.6, 2.1, 5.6

def bn_ext(filename):
    pos = filename.rfind('/')
    return filename[pos+1:] if pos != -1 else filename

def bn(filename):
    filename = bn_ext(filename)
    pos = filename.rfind('.')
    return filename[:pos] if pos != -1 else filename

def get_lines(filename):
    return VFS.read_file(filename).splitlines()

def find_files(parent, extensions):
    return [filename for filename in VFS.list_files(parent) if any(filename.endswith(ext) for ext in extensions)]

class ResourceManager():
    def __init__(self, app):
        self.app = app

        self.sprites = {bn(fn): Image.load(fn) for fn in find_files('sprites', ('.png',))}
        self.creatures = {bn(fn): Image.load(fn) for fn in find_files('creatures', ('.png',))}
        self.intermissions = {bn(fn): get_lines(fn) for fn in find_files('intermissions', ('.txt',))}
        self.shaders = {bn_ext(fn): '\n'.join(get_lines(fn)) for fn in find_files('shaders', ('.fsh', '.vsh'))}
        self.sounds = {bn(fn): Sound(fn) for fn in find_files('sounds', ('.wav',))}
        self.fonts = {size: Font(size) for size in FONTS}

        self.backgrounds = {}
        for fn in sorted(find_files('backgrounds', ('.jpg',))):
            self.backgrounds.setdefault(bn(fn).split('-')[0], []).append(Image.load(fn))

        self.levels = []
        for fn in sorted(find_files("levels", ('.txt',))):
            _, group, number = bn(fn).split('-')
            self.levels.append((int(group), int(number), get_lines(fn)))

        pickup_lines = [line.split(':') for line in get_lines('pickups.txt') if not line.startswith('#')]
        self.pickups = {thingie: (sfx, int(coins), int(lives)) for thingie, sfx, coins, lives in pickup_lines}

    def render_text(self, font, text):
        return self.fonts[font].render(text)

    def sfx(self, name):
        self.sounds[name].play()

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
