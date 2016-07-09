from sprite import Sprite

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
        sprite = self.lookup_sprite(sprite_name)

        w, h = sprite.get_size()
        left = min(point[0] for point in points)
        right = max(point[0] for point in points)
        bottom = max(point[1] for point in points)
        factor = min(4.0, float(right-left) / float(w))

        x = left + (right-left)/2 - (w*factor)/2
        y = bottom - h*factor

        # align the enemy in the center of the polygon
        # and with the bottom (frontmost) edge of the
        # polygon aligned with the bottom of the enemy
        self.app.renderer.draw(sprite, (x, y), factor, opacity, tint)
