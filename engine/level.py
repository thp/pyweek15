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
                line = line.rstrip('\n') + (' ' * width)
                self.rows.append([Item(*self.charmap[line[i]]) if line[i] != ' ' else None for i in range(width)])
