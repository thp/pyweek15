from engine.sprite import Sprite

from pygame import transform

from logic.lamemath import center, center_in, shade_color

class Player(Sprite):
    GRAVITY = 1.2  # .981
    BLINKING_FRAMES = 20

    def __init__(self, app):
        self.x = 2
        self.y = 0
        self.dest_x = 2
        self.height = 0
        self.vertical_velocity = 0
        self.coins_collected = 0
        self.health = 100
        self.can_jump = True
        self.app = app
        self.blinking = 0
        self.init('whale_%d', 3)

    def jump(self):
        if self.can_jump:
            self.vertical_velocity = 15
            self.can_jump = False
            self.app.audman.sfx("jump", 1)

    def picked_up(self, thingie):
        print 'i picked up a', thingie
        if thingie == 'coin':
            self.coins_collected += 1
            self.app.audman.sfx("coin")

    def crashed(self):
        print 'AARGH!'
        if not self.blinking:
            self.health -= 1
            self.app.audman.sfx("crash")
            self.blinking = self.BLINKING_FRAMES

    def step(self):
        self.x = self.x * .5 + self.dest_x * .5
        self.height += self.vertical_velocity
        if self.height < 0:
            self.can_jump = True
            self.height = 0
            self.vertical_velocity *= -.5
            if abs(self.vertical_velocity) < 2:
                self.vertical_velocity = 0
                self.height = 0
        self.vertical_velocity -= self.GRAVITY
        if self.blinking:
            self.blinking -= 1
        self.process()

    def draw(self, screen, points):
        if self.blinking and (self.blinking / 3) % 2 == 0:
            return

        sprite_name = self.current_sprite_name()

        # XXX: When the "b", and "c" images of the whale are
        # here, change the chars= line to something like this:
        # (note that "b" and "a" get mirrored below when dest_x >= 3)
        chars = ['a', 'b', 'c', 'b', 'a']
        #chars = ['a', 'a', 'a', 'a', 'a']

        sprite_name = sprite_name.replace('whale_', 'whale_%s_' % chars[self.dest_x])
        sprite = self.lookup_sprite(sprite_name)

        if self.dest_x >= 3:
            sprite = transform.flip(sprite, True, False)

        w, h = sprite.get_size()
        coords = center(points)
        coords = (coords[0] - w / 2 + self.blinking % 5, coords[1] - h / 2)
        screen.blit(sprite, coords)

