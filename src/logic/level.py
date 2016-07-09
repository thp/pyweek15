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
    ENEMIES, PICKUP, META = range(3)

    def __init__(self, leveldata):
        self.charmap = {}
        self.rows = []
        self.speed = 10
        self.background = 'test'

        width = 5
        section = self.ENEMIES
        for line in leveldata:
            if ':enemies:' in line:
                section = self.ENEMIES
            elif ':pickups:' in line:
                section = self.PICKUP
            elif ':meta:' in line:
                section = self.META

            if line.startswith('#'):
                if '=' in line:
                    key, value = (x.strip() for x in line[1:].strip().split('=', 1))
                    if section in (self.ENEMIES, self.PICKUP):
                        assert key not in self.charmap
                        self.charmap[key] = (value, section == self.ENEMIES)
                    elif section == self.META:
                        if key == 'background':
                            self.background = value.strip()
                continue

            line = line.rstrip('\n') + (' ' * width)
            self.rows.append([Item(*self.charmap[line[i]]) if line[i] != ' ' else None for i in range(width)])
