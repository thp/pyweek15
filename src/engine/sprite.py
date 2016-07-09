import math

def make_sequence(frames):
    return range(1, frames+1) + range(frames-1, 1, -1)

class Sprite(object):
    def init(self, basename, frames, duration=.2):
        self.duration = duration

        if frames == 0:
            self.sprites = [basename]
        else:
            self.sprites = ['%s-%d' % (basename, x) for x in make_sequence(frames)]

        self.frames_per_sprite = int(duration * self.app.fps)
        self.current_sprite = 0
        self.current_frame = 0

    def process(self):
        self.current_frame += 1
        if self.current_frame == self.frames_per_sprite:
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.current_frame = 0

    def current_sprite_name(self):
        return self.sprites[self.current_sprite]

    def _draw(self, sprite_name, points, max_scale, opacity, tint, align_bottom):
        sprite = self.app.resman.get_sprite(sprite_name)
        w, h = sprite.get_size()
        left = min(point[0] for point in points)
        right = max(point[0] for point in points)
        bottom = max(point[1] for point in points)
        factor = min(max_scale, float(right-left) / float(w))

        x = (right+left)/2 - (w*factor)/2
        if align_bottom:
            y = bottom - h*factor
        else:
            center = tuple(float(x) / len(points) for x in map(sum, zip(*points)))
            y = center[1] - h / 2

        self.app.renderer.draw(sprite, (x, y), factor, opacity, tint)

class Enemy(Sprite):
    def __init__(self, app, name):
        self.app = app
        frames = 0
        while self.app.resman.get_sprite('%s-%d' % (name, frames+1)) is not None:
            frames += 1
        self.init(name, frames)

    def step(self):
        self.process()

    def draw(self, screen, points, opacity, tint):
        sprite_name = self.current_sprite_name()
        self._draw(sprite_name, points, 4.0, opacity, tint, True)

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

        sprite_name = self.current_sprite_name().replace('whale', 'whale_%s' % self.dest_x)
        self._draw(sprite_name, points, 1.0, opacity, tint, False)
