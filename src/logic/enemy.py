
from engine.sprite import Sprite

from logic.lamemath import center

from pygame import transform

# some objects have 2 or 3 frames
nr_frames = {
    "lanternfish": 3,
    "fishy_rainbow": 2,
    "fishy_red": 2,
    "fishy_deepsea": 2,
}


class Enemy(Sprite):
    def __init__(self, app, name):
        self.app = app
        if self.app.resman.get_sprite(name) is not None:
            self.init(name, 1)
        else:
            self.init(name + '_%d', nr_frames[name])

    def step(self):
        self.process()

    def draw(self, screen, points):
        sprite_name = self.current_sprite_name()
        sprite = self.lookup_sprite(sprite_name)

        w, h = sprite.get_size()
        left = min(point[0] for point in points)
        right = max(point[0] for point in points)
        bottom = max(point[1] for point in points)
        factor = min(1., float(right-left) / float(w))
        sprite = transform.scale(sprite, (int(w*factor), int(h*factor)))
        x, _ = center(points)
        x = left + (right-left)/2 - (w*factor)/2
        y = bottom - h*factor

        # align the enemy in the center of the polygon
        # and with the bottom (frontmost) edge of the
        # polygon aligned with the bottom of the enemy

        screen.blit(sprite, (x, y))
