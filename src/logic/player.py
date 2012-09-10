
class Player:
    GRAVITY = 1.2 #.981

    def __init__(self):
        self.x = 0
        self.y = 0
        self.dest_x = 0
        self.height = 0
        self.vertical_velocity = 0
        self.coins_collected = 0
        self.health = 100

    def jump(self):
        if self.height == 0:
            self.vertical_velocity = 10

    def picked_up(self, thingie):
        print 'i picked up a', thingie
        if thingie == 'coin':
            self.coins_collected += 1

    def crashed(self):
        print 'AARGH!'
        self.health -= 1

    def step(self):
        self.x = self.x * .5 + self.dest_x * .5
        self.height += self.vertical_velocity
        if self.height < 0:
            self.height = 0
            self.vertical_velocity *= -.6
            if abs(self.vertical_velocity) < 2:
                self.vertical_velocity = 0
                self.height = 0
        self.vertical_velocity -= self.GRAVITY


