
from engine.sprite import Sprite

from logic.lamemath import center, center_in, shade_color

from pygame import transform

class Enemy(Sprite):
    def __init__(self, app, name):
        self.app = app
        self.init(name + '_%d', 3)

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

