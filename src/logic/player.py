from engine.sprite import Sprite
import math

class Player(Sprite):
    GRAVITY = 1.2  # .981
    BLINKING_FRAMES = 20
    INITIAL_HEALTH = 9
    MAX_HEALTH = 30

    def __init__(self, app):
        self.app = app
        self.health = 0

        self.init('whale', 3)
        self.reset()


    def reset(self, hard=False):
        self.x = 2
        self.y = 0
        self.dest_x = 2
        self.height = 0
        self.vertical_velocity = 0
        self.can_jump = True
        self.blinking = 0

        if hard:
            self.coins_collected = 0
            self.health = self.INITIAL_HEALTH
            self.max_health = self.MAX_HEALTH

    def jump(self):
        if self.can_jump:
            self.vertical_velocity = 15
            self.can_jump = False
            self.app.audman.sfx("jump")

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
            lives = int(self.health/3) + 1
            self.health = min(lives*3, self.MAX_HEALTH)

    def crashed(self):
        if not self.blinking:
            self.health -= 1
            self.app.audman.sfx("crash")
            self.blinking = self.BLINKING_FRAMES

        return (self.health % 3 == 0)

    def step(self):
        self.x = self.x * .5 + self.dest_x * .5
        self.height += self.vertical_velocity
        if self.height < 0:
            self.can_jump = True
            self.height = 0
            self.vertical_velocity = 0
        self.vertical_velocity -= self.GRAVITY
        if self.blinking:
            self.blinking -= 1
        self.process()


    def draw(self, screen, points, opacity, tint):
        xoffset, yoffset, opacity = 0., 0., 1.
        tint = 1., 1., 1.

        if self.blinking:
            value = 1. - abs(math.sin(self.blinking*.2))
            tint = 1, value, value
            yoffset = math.sin(self.blinking*.5) * 5.

        sprite_name = self.current_sprite_name()

        sprite_name = sprite_name.replace('whale', 'whale_%s' % self.dest_x)
        sprite = self.lookup_sprite(sprite_name)

        w, h = sprite.get_size()
        center = tuple(float(x) / len(points) for x in map(sum, zip(*points)))
        center = (center[0] - w / 2 + xoffset, center[1] - h / 2 + yoffset)
        self.app.renderer.draw(sprite, center, 1., opacity, tint)

