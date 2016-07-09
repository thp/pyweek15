from scene import Scene
from level import Level
from sprite import Enemy

import math

from pygame.locals import *

MAX_SPEEDUP = 4
SPEEDUP_STEP = .1
KEYBOARD_REPEAT_MOD = 7
MIN_DEST_X = 0
MAX_DEST_X = 4

class Game(Scene):
    def __init__(self, app):
        super(Game, self).__init__(app, 'Game')
        self.enemies = {}
        self.reset(hard=True)

    def reset(self, hard=False):
        self.time = 0.
        self.i = 0
        self.direction = 0
        self.boost = False
        self.speedup = 0
        self.app.screen.reset_camera()
        if hard:
            self.levels = self.level_progression()
            self.level_info = next(self.levels)
        self.level = Level(self.level_info)
        self.app.player.reset(hard)

    def level_progression(self):
        last_group_nr, last_level_nr = None, None
        for group_nr, level_nr, level_data in sorted(self.app.resman.levels):
            if last_group_nr is not None and last_group_nr != group_nr:
                self.app.go_to_scene('NextLevelGroup_%d_%d' % (last_group_nr, last_level_nr))
            yield level_data
            last_group_nr = group_nr
            last_level_nr = level_nr
        self.app.go_to_scene('Victory')

    def process(self):
        self.app.screen.process()

        self.i += 1

        step = .01 * self.level.speed
        if self.boost:
            if self.speedup < MAX_SPEEDUP:
                self.speedup += SPEEDUP_STEP
            if self.speedup > MAX_SPEEDUP:
                self.speedup = MAX_SPEEDUP
        else:
            if self.speedup > 0:
                self.speedup -= SPEEDUP_STEP * 2
            if self.speedup < 0:
                self.speedup = 0

        self.time += step * (1 + self.speedup)

        while self.time > 1.:
            self.time -= 1.
            self.app.player.y += 1

        if self.app.player.y > len(self.level.rows):
            try:
                # advance a level and reset
                self.level_info = next(self.levels)
                self.reset()
            except StopIteration:
                pass

            # TODO: animate level end

        if self.i % KEYBOARD_REPEAT_MOD == 0:
            next_x = max(MIN_DEST_X, min(MAX_DEST_X, self.app.player.dest_x + self.direction))

        self.app.player.step()
        for enemy in self.enemies.values():
            enemy.step()

        if self.app.player.health <= 0:
            self.reset(hard=True)
            self.app.go_to_scene('GameOver')

    def process_input(self, event):
        def go_left():
            self.direction = -1
            self.i = 0
            if self.app.player.dest_x > MIN_DEST_X:
                self.app.player.dest_x -= 1

        def go_right():
            self.direction = 1
            self.i = 0
            if self.app.player.dest_x < MAX_DEST_X:
                self.app.player.dest_x += 1

        if event.type == MOUSEBUTTONDOWN:
            x, y = event.pos

            if y < self.app.screen.height / 4:
                self.boost = True
            elif y > self.app.screen.height * 3 / 4:
                self.app.player.jump()
            elif x < self.app.screen.width / 3:
                go_left()
            elif x > self.app.screen.width * 2 / 3:
                go_right()

        elif event.type == MOUSEBUTTONUP:
            self.direction = 0
            self.boost = False
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                pass
            elif event.key == K_SPACE:
                self.app.player.jump()
            elif event.key == K_LEFT:
                go_left()
            elif event.key == K_RIGHT:
                go_right()
            elif event.key == K_UP:
                self.boost = True
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                self.direction = 0
            elif event.key == K_RIGHT:
                self.direction = 0
            elif event.key == K_UP:
                self.boost = False
        super(Game, self).process_input(event)


    def draw(self):
        draw_queue = [(self.app.player, (self.app.player.x - 2.0, self.app.player.height / 100, 1.0))]

        # Fade in enemy sprites coming from the back
        fade_offset = 3.0
        fade_width = 10.0
        fade_distance = int(fade_offset + fade_width + 1)
        for yidx, offset in enumerate(range(self.app.player.y, self.app.player.y+fade_distance)):
            if offset >= len(self.level.rows):
                break

            for xidx, column in enumerate(self.level.rows[offset]):
                if column is None:
                    continue

                if yidx == 1 and xidx == self.app.player.dest_x and self.app.player.height < 10:
                    if column.collide(self.app.player):
                        self.reset()
                        self.app.go_to_scene('LostLife')

                if column.name:
                    if column.name not in self.enemies:
                        self.enemies[column.name] = Enemy(self.app, column.name)
                    enemy = self.enemies[column.name]
                    draw_queue.append((enemy, (xidx - 2.0, 0.0, yidx - self.time)))

        self.app.screen.before_draw()
        backgrounds = self.app.resman.get_background(self.level.background)
        self.app.renderer.draw(backgrounds[int(self.time + self.app.player.y) % len(backgrounds)], (0, 0))

        # Draw all enemies (+player), back-to-front for proper stacking order
        for sprite, pos in reversed(draw_queue):
            tint = 1., 1., 1.
            if self.level.background == 'surreal':
                # Special FX for the Surreal level - tint like crazy!
                tint = [.5+.5*math.sin(self.i*.009), .5+.5*math.sin(.9+self.i*.004), .5+.5*math.sin(4.5+self.i*.2)]

            # Fade in enemy sprites coming from the back
            opacity = max(0.0, 1.0 - (pos[2] - fade_offset) / fade_width)
            self.app.screen.draw_sprite(sprite, pos, opacity, map(lambda x: x*opacity, tint))

        self.app.renderer.begin_overlay()
        self.app.screen.draw_stats(self.app.player.coins_collected, self.app.player.health)
