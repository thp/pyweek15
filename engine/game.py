from scene import Scene
from level import Level
from sprite import Enemy

import math

class Game(Scene):
    FADE_OFFSET = 3
    FADE_WIDTH = 10
    FADE_DISTANCE = int(FADE_OFFSET + FADE_WIDTH + 1)
    MAX_SPEEDUP = 4

    def __init__(self, app):
        super(Game, self).__init__(app, 'Game')
        self.enemies = {}

    def resume(self):
        pass

    def reset(self, hard=False):
        self.time = 0.
        self.boost = False
        self.speedup = 0
        self.camera_y = 0
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
        if self.boost:
            if self.speedup < self.MAX_SPEEDUP:
                self.speedup += 0.1
            if self.speedup > self.MAX_SPEEDUP:
                self.speedup = self.MAX_SPEEDUP
        else:
            if self.speedup > 0:
                self.speedup -= 0.2
            if self.speedup < 0:
                self.speedup = 0

        self.time += 0.1 * (1 + self.speedup)
        self.time, dy = math.modf(self.time)
        self.app.player.y += int(dy)

        if self.app.player.y > len(self.level.rows):
            if (self.app.player.y - self.camera_y) > self.FADE_DISTANCE:
                try:
                    self.level_info = next(self.levels)
                    self.reset()
                except StopIteration:
                    pass
        else:
            self.camera_y = max(0, self.app.player.y + self.time)

        self.app.player.step()
        for enemy in self.enemies.values():
            enemy.step()

        if self.app.player.health <= 0:
            self.reset(hard=True)
            self.app.go_to_scene('GameOver')

    def process_input(self, pressed, key):
        if pressed:
            if key == ' ':
                self.app.player.jump()
            elif key in ('left', 'right'):
                self.app.player.dest_x = max(0, min(4, self.app.player.dest_x + (-1 if (key == 'left') else 1)))
            elif key == 'up':
                self.boost = True
        elif key == 'up':
            self.boost = False

    def draw(self):
        draw_queue = [(self.app.player, (self.app.player.x - 2.0, self.app.player.height / 100,
                                         (self.app.player.y + self.time - self.camera_y) + 1.0))]

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
        self.app.renderer.draw(backgrounds[int(self.time + self.app.player.y) % len(backgrounds)], (0, 0))

        for sprite, pos in reversed(draw_queue):
            tint = 1., 1., 1.
            if self.level.background == 'surreal':
                # Special FX for the Surreal level - tint like crazy!
                tint = [.5+.5*math.sin(a+(self.time+self.app.player.y)*b) for a, b in ((0,4.5),(.9,2.0),(4.5,9.5))]

            # Fade in enemy sprites coming from the back
            opacity = max(0.0, 1.0 - (pos[2] - float(self.FADE_OFFSET)) / float(self.FADE_WIDTH))
            self.app.screen.draw_sprite(sprite, pos, opacity, map(lambda x: x*opacity, tint))

        self.app.renderer.postprocess()
        if self.app.player.y < 0:
            self.app.screen.draw_text(['Get Ready'])
        elif self.app.player.y > len(self.level.rows):
            self.app.screen.draw_text(['Level clear!', 'Collected: ... / ...', 'Lives used: ...'])
        self.app.screen.draw_stats(self.app.player.coins_collected, self.app.player.health)
