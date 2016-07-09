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
        self._draw(sprite_name, points, 4.0, opacity, tint, True)
