
from engine.scene import Scene
from logic.level import Level
from logic.enemy import Enemy

import math
from itertools import *
from operator import *

import pygame
from pygame.locals import *

MAX_SPEEDUP = 4
SPEEDUP_STEP = .1

# keyboard repeat rate (modulo) -> higher value = less repeat
KEYBOARD_REPEAT_MOD = 7


MIN_DEST_X = 0
MAX_DEST_X = 4

# This is not just enemies, but also pick-ups (for whatever reason)
ENEMY_NAMES = [
    'coral_a',
    'coral_b',
    'coral_c',
    'coral_d',
    'pearl',
    'fishy_rainbow',
    'fishy_red',
    'fishy_deepsea',
    'diver',
    'seaweed',
    'lanternfish',
    'shell',
    'sandboxtoys',
    'oyster_0_pearl',
    'oyster_1_pearl',
    'oyster_2_pearl',
    'oyster_3_pearl',
    'rock_m',
    'rock_l',
    'rock_s',
    'jellyfish_a',
    'jellyfish_b',
    'starfish',
    'shoe',
]

class Game(Scene):
    def __init__(self, app):
        super(Game, self).__init__(app, 'Game')

        self.enemies = {}

        for key in ENEMY_NAMES:
            self.enemies[key] = Enemy(self.app, key)

        # reset everything
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
            self.level_nr = next(self.levels)
        filename = "levels/level-%i-%i.txt" % self.level_nr
        # XXX move this into resource manager (levels need a
        # reset button first)
        self.level = Level(self.app.get_filename(filename))

        self.app.player.reset(hard)


    def level_progression(self):
        def advance():
            for key, group in itr:
                for level in group:
                    #print "next level:", level
                    yield level
                # XXX ugly, ugly side effect
                self.next_state = "NextLevelGroup_%i_%i" % level

        levels = self.app.resman.levels
        try:
            # honor the command line switch for starting level
            idx = levels.index(self.app.start_level)
            levels = levels[idx:]
        except ValueError:
            pass

        itr = groupby(levels, itemgetter(0))
        return advance()




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

        if self.level.exceeds_row(self.app.player.y):
            try:
                # advance a level and reset
                self.level_nr = next(self.levels)
                self.reset()
            except StopIteration:
                self.next_state = "Victory"

            # TODO: animate level end


        if self.i % KEYBOARD_REPEAT_MOD == 0:
            next_x = self.app.player.dest_x + self.direction
            if next_x >= MIN_DEST_X and next_x <= MAX_DEST_X:
                self.app.player.dest_x += self.direction

        self.app.player.step()
        for enemy in self.enemies.values():
            enemy.step()

        if self.app.player.health <= 0:
            # reset player and game
            self.reset(hard=True)
            self.next_state = "GameOver"

        return super(Game, self).process()

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
        backgrounds = self.app.resman.get_background(self.level.background)
        pos = int(self.time + self.app.player.y) % len(backgrounds)
        self.app.renderer.draw(backgrounds[pos], (0, 0))

        x = self.app.player.x
        y = self.time

        # draw queue for back-to-front drawing of enemies
        draw_queue = [(y, self.app.player, (x - 2.0, self.app.player.height / 100, 1.0))]

        # Fade in enemy sprites coming from the back
        fade_offset = 3.0
        fade_width = 10.0
        fade_distance = int(fade_offset + fade_width + 1)
        for yidx, offset in enumerate(range(self.app.player.y, self.app.player.y+fade_distance)):
            if offset >= len(self.level.rows):
                break

            for xidx, column in enumerate(self.level.rows[offset].items):
                if column is None:
                    continue

                x = xidx - 2.0
                y = yidx

                if yidx == 1 and xidx == self.app.player.dest_x and self.app.player.height < 10:
                    if column.collide(self.app.player):
                        # lost a life
                        # reset to beginning of current level
                        self.reset()
                        self.next_state = "LostLife"

                if column.name in self.enemies:
                    enemy = self.enemies[column.name]
                    draw_queue.append((y, enemy, (x, 0.0, y - self.time)))

                elif column.name:
                    print '[WARNING] Missing graphic:', column.name

        self.app.screen.before_draw()

        # Draw all enemies (+player), back-to-front for proper stacking order
        for y, sprite, pos in reversed(draw_queue):
            opacity = 1.0

            if self.level.background == 'surreal':
                # Special FX for the Surreal level - tint like crazy!
                tint = [
                    .5+.5*math.sin(self.i*.009),
                    .5+.5*math.sin(.9+self.i*.004),
                    .5+.5*math.sin(4.5+self.i*.2),
                ]
            else:
                tint = 1., 1., 1.

            # Fade in enemy sprites coming from the back
            opacity = max(0.0, 1.0 - ((y - self.time) - fade_offset) / fade_width)
            tint = map(lambda x: x*opacity, tint)

            self.app.screen.draw_sprite(sprite, pos, opacity, tint)

        self.app.renderer.begin_overlay()
        self.app.screen.draw_stats(self.app.player.coins_collected,
                                   self.app.player.health)
