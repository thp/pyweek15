from .scene import Scene
from .resman import Level
from .sprite import Enemy
from core import math

class Game(Scene):
    FADE_OFFSET = 6
    FADE_WIDTH = 10
    FADE_DISTANCE = int(FADE_OFFSET + FADE_WIDTH + 1)

    def __init__(self, app):
        super(Game, self).__init__(app, 'Game')
        self.enemies = {}

    def resume(self):
        self.app.screen.set_buttons(['left', 'right', None, 'swim', 'jump'], self.on_button_pressed)

    def on_button_pressed(self, pressed, button):
        self.process_input(pressed, {
            'jump': ' ',
            'swim': 'up',
        }.get(button, button))

    def reset(self, hard=False):
        self.time = 0.
        self.boost = False
        self.speedup = 0
        self.camera_y = 0
        self.done = False
        self.started = False
        if hard:
            self.levels = self.level_progression()
            self.level_info = next(self.levels)
        self.level = Level(self.level_info)
        self.app.player.reset(hard)

    def level_progression(self, last_group_nr=None):
        for group_nr, level_nr, level_data in sorted(self.app.resman.levels):
            if last_group_nr != group_nr:
                self.app.go_to_scene('LevelGroupIntro-%d' % (group_nr,))
            yield level_data
            last_group_nr = group_nr
        self.app.go_to_scene('Victory')

    def process(self):
        self.speedup = max(0, min(4, self.speedup + (0.1 if self.boost else -0.2)))
        self.time += 0.1 * (1 + self.speedup)
        dy = int(self.time)
        self.app.player.y += dy
        self.time -= dy

        if self.app.player.y > len(self.level.rows):
            if not self.done:
                self.app.resman.sfx('261597__kwahmah-02__bubbles2')
                self.done = True
            if (self.app.player.y - self.camera_y) > self.FADE_DISTANCE:
                try:
                    self.level_info = next(self.levels)
                    self.reset()
                except StopIteration:
                    pass
        else:
            if not self.started:
                self.app.resman.sfx('110393__soundscalpel-com__water-splash')
                self.started = True
            self.camera_y = max(0, self.app.player.y + self.time)

        self.app.player.step()
        for enemy in self.enemies.values():
            enemy.step()

        if self.app.player.health <= 0:
            self.reset(hard=True)
            self.app.go_to_scene('GameOver')

    def process_input(self, pressed, key):
        if key == 'up':
            self.boost = pressed
        elif pressed and key == ' ':
            self.app.player.jump()
        elif pressed and key in ('left', 'right'):
            self.app.player.dest_x = max(0, min(4, self.app.player.dest_x + (-1 if (key == 'left') else 1)))

    def process_touch(self, event, x, y, finger):
        self.app.screen.process_touch(event, x, y, finger)

    def draw(self):
        now, height = self.app.player.y + self.time, self.app.player.height / 100
        draw_queue = [(self.app.player, (self.app.player.x - 2.0, height, now - self.camera_y + 1.0))]

        for yidx, offset in enumerate(range(self.app.player.y, self.app.player.y+self.FADE_DISTANCE)):
            if offset > 0 and offset < len(self.level.rows):
                for xidx, column in enumerate(self.level.rows[offset]):
                    if column:
                        if yidx == 1 and xidx == self.app.player.dest_x and self.app.player.height < 10:
                            if column.collide(self.app.player):
                                self.reset()
                                self.app.go_to_scene('LostLife')

                        if column.name:
                            if column.name not in self.enemies:
                                self.enemies[column.name] = Enemy(self.app, column.name)
                            draw_queue.append((self.enemies[column.name], (xidx - 2.0, 0.0, yidx - self.time)))

        backgrounds = self.app.resman.backgrounds[self.level.background]
        self.app.renderer.draw(backgrounds[int(now) % len(backgrounds)], (0, 0))

        for sprite, pos in reversed(draw_queue):
            tint = 1., 1., 1.
            if self.level.background == 'surreal':
                # Special FX for the Surreal level - tint like crazy!
                tint = [.5+.5*math.sin(a+now*b) for a, b in ((0,4.5),(.9,2.0),(4.5,9.5))]

            # Fade in enemy sprites coming from the back
            opacity = min(1.0, max(0.0, 1.0 - (pos[2] - float(self.FADE_OFFSET)) / float(self.FADE_WIDTH)))
            self.app.screen.draw_sprite(sprite, pos, opacity, map(lambda x: x*opacity, tint))

        self.app.renderer.postprocess()
        if self.app.player.y < 0:
            self.app.screen.draw_text(['Get Ready'])
        elif self.app.player.y > len(self.level.rows):
            self.app.screen.draw_text(['Level clear'])
        self.app.screen.draw_stats(self.app.player.coins_collected, self.app.player.health)
        self.app.screen.draw_buttons(False)
