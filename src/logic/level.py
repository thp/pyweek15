
import re


class Item:
    def __init__(self, name, is_enemy):
        self.name = name
        self.is_enemy = is_enemy

    def collide(self, player):
        if self.is_enemy:
            player.crashed()
            return 1
        elif self.name:
            player.picked_up(self.name)
            self.name = ''
            return -1

        return 0

    def __repr__(self):
        return '%s%s' % (self.name, ' (enemy)' if self.is_enemy else '')


class Row:
    WIDTH = 5

    def __init__(self, level, line):
        self.level = level

        # pad line to WIDTH chars
        line = line + (' '*(self.WIDTH-len(line)))

        self.items = []
        for char in line:
            self.items.append(self.level.lookup(char))

    def __repr__(self):
        return repr(self.items)


class Level:
    DEFAULT_SPEED = 10

    ENEMIES, PICKUP, META = range(3)

    def __init__(self, filename):
        self.charmap = {}
        self.rows = []
        self.speed = self.DEFAULT_SPEED
        self.background = 'test'

        self.messages = {}

        section = self.ENEMIES
        for line in open(filename):
            if ':enemies:' in line:
                section = self.ENEMIES
            elif ':pickups:' in line:
                section = self.PICKUP
            elif ':meta:' in line:
                section = self.META

            definition = re.match(r'^# ([^=]+)=(.*)$', line.strip())
            if definition:
                key, value = definition.groups()
                if section in (self.ENEMIES, self.PICKUP):
                    self.add_item(key, value, section == self.ENEMIES)
                elif section == self.META:
                    self.set_meta(key, value)

            if line.startswith('#'):
                continue

            if line.startswith('!'):
                index = len(self.rows)
                msg = line[1:].rstrip('\n')
                if index in self.messages:
                    self.messages[index] += '\n' + msg
                else:
                    self.messages[index] = msg
                continue

            self.rows.append(Row(self, line.rstrip('\n')))

    def get_message(self, y):
        return self.messages.get(y)

    def exceeds_row(self, y):
        return y >= self.rows.__len__()

    def add_item(self, char, name, is_enemy):
        assert char not in self.charmap
        self.charmap[char] = (name, is_enemy)

    def set_meta(self, key, value):
        if key == 'speed':
            self.speed = int(value)
        elif key == 'background':
            self.background = value.strip()

    def lookup(self, char):
        if char == ' ':
            return None
        return Item(*self.charmap[char])


if __name__ == '__main__':
    level = Level('level.txt')
    for row in level.rows:
        print row

