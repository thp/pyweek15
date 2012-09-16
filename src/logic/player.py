from engine.sprite import Sprite
from logic.lamemath import center

import math

class Player(Sprite):
    GRAVITY = 1.2  # .981
    BLINKING_FRAMES = 20

    def __init__(self, app, health=100, coins_collected=0):
        self.x = 2
        self.y = 0
        self.dest_x = 2
        self.height = 0
        self.vertical_velocity = 0
        self.coins_collected = coins_collected
        self.max_health = health
        self.health = health
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
        if thingie == 'pearl':
            self.coins_collected += 1
            self.app.audman.sfx("pearl" + str(int(self.dest_x+1)))
        elif thingie == 'oyster_1_pearl':
            self.coins_collected += 1
            self.app.audman.sfx("pearl")
        elif thingie == 'oyster_2_pearl':
            self.coins_collected += 2
            self.app.audman.sfx("pearl")
        elif thingie == 'oyster_3_pearl':
            self.coins_collected += 3
            self.app.audman.sfx("pearl")
        elif thingie.startswith("fishy"):
            # [11:47pm] lobbbe_: what about that: you get your health back to full if you eat a fishy,
            # and if your health is already full - and only then - you get an extra life?
            self.app.audman.sfx("fishy")
            if self.health <= self.max_health - 3:
                self.health += 3
            else:
                self.health = self.max_health

    def crashed(self):
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


    def draw(self, screen, points, opacity):
        xoffset, yoffset, opacity = 0., 0., 1.
        tint = 1., 1., 1.

        if self.blinking:
            value = 1. - abs(math.sin(self.blinking*.2))
            tint = 1, value, value
            yoffset = math.sin(self.blinking*.5) * 5.

        sprite_name = self.current_sprite_name()

        sprite_name = sprite_name.replace('whale_', 'whale_%s-' % self.dest_x)
        sprite = self.lookup_sprite(sprite_name)

        w, h = sprite.get_size()
        coords = center(points)
        coords = (coords[0] - w / 2 + xoffset, coords[1] - h / 2 + yoffset)
        self.app.renderer.draw(sprite, coords, 1., opacity, tint)

