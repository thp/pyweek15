
import re


class Item:
    def __init__(self, name, is_enemy):
        self.name = name
        self.is_enemy = is_enemy

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
    def __init__(self, filename):
        self.charmap = {}
        self.rows = []
        is_enemy = False
        for line in open(filename):
            if ':enemies:' in line:
                is_enemy = True
            elif ':pickups:' in line:
                is_enemy = False

            definition = re.match(r'^# (.)=(.*)$', line.strip())
            if definition:
                char, name = definition.groups()
                self.add_item(char, name, is_enemy)

            if line.startswith('#'):
                continue

            self.rows.append(Row(self, line.rstrip('\n')))

    def add_item(self, char, name, is_enemy):
        assert char not in self.charmap
        self.charmap[char] = Item(name, is_enemy)

    def lookup(self, char):
        if char == ' ':
            return None
        return self.charmap[char]


if __name__ == '__main__':
    level = Level('level.txt')
    for row in level.rows:
        print row

