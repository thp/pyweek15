from itertools import groupby
from operator import itemgetter

from engine.scene import Scene
from logic.level import Level
from logic.enemy import Enemy

import pygame
from pygame.locals import *

DEPTH = 15
WORLD_DEPTH = 10 # fudge factor... works for DEPTH @ 15

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
        super(Game, self).__init__(app)

        self.enemies = {}

        for key in ENEMY_NAMES:
            self.enemies[key] = Enemy(self.app, key)

        # reset everythin
        self.reset(hard=True)


    def reset(self, hard=False):
        self.time = 0.
        self.i = 0
        self.direction = 0
        self.boost = False
        self.speedup = 0

        if hard:
            self.levels = self.level_progression()
            self.level_nr = next(self.levels)
        filename = "levels/level-%i-%i.txt" % self.level_nr
        self.level = Level(self.app.get_filename(filename))

        self.app.player.reset(hard)


    def level_progression(self):
        def advance():
            for key, group in itr:
                for level in group:
                    print "next level:", level
                    # XXX move this into resource manager (levels need a
                    # reset button first)
                    yield level
                # XXX ugly, ugly side effect
                self.next_state = ("NextLevelGroup", None)
        
        levels = self.app.resman.levels
        try:
            # honor the command line swith for starting level
            idx = levels.index(self.app.start_level)
            levels = levels[idx:]
        except ValueError:
            pass

        itr = groupby(levels, itemgetter(0))
        return advance()


    def process(self):
        self.i += 1

        step = .01 * self.level.speed
        if self.boost:
            if self.speedup < MAX_SPEEDUP:
                self.speedup += SPEEDUP_STEP
            if self.speedup > MAX_SPEEDUP:
                self.speedup =MAX_SPEEDUP
        else:
            if self.speedup > 0:
                self.speedup -= SPEEDUP_STEP * 2
            if self.speedup < 0:
                self.speedup = 0

        self.time += step * (1 + self.speedup)

        if self.time > 1.:
            self.time -= 1.
            self.app.player.y += 1

        if self.level.exceeds_row(self.app.player.y):
            try:
                # advance a level and reset
                self.level_nr = next(self.levels)
                self.reset()
            except StopIteration:
                self.next_state = ("Victory", None)

            # TODO animate level end

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

            self.next_state = ("GameOver", None)

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

            if y < self.app.screen.height / 2:
                self.boost = True

            if y > self.app.screen.height * 3 / 4:
                self.app.player.jump()

            if x < self.app.screen.width / 3:
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


    def map_coords(self, lane, jump, distance):
        """
        Translate game coordinates to world coordinates.

        lane:     0..5
        jump:     not defined yet
        distance: 0..DEPTH+1 (number of rows)

        world coordinates: 1x1xWORLD_DEPTH
        """

        x = (lane + 0.5) / 5.0
        y = (500.0 - jump) / 500.0
        z = WORLD_DEPTH * (distance+0.5) / DEPTH

        return (x, y, z)


    def draw(self):
        self.app.screen.clear()
        backgrounds = self.app.resman.get_background(self.level.background)
        pos = int(self.time + self.app.player.y) % len(backgrounds)
        self.app.screen.display.blit(backgrounds[pos], (0, 0))

        x = self.app.player.x
        y = self.time
        player_points = self.mkpoints(x, y, self.app.player.height)

        # draw queue for back-to-front drawing of enemies
        draw_queue = [(y, self.app.player, player_points)]

        for yidx, offset in enumerate(range(self.app.player.y, self.app.player.y+DEPTH)):
            if offset < len(self.level.rows):
                for xidx, column in enumerate(self.level.rows[offset].items):
                    if column is None:
                        continue

                    x = xidx
                    y = yidx

                    if yidx == 1 and xidx == self.app.player.dest_x and self.app.player.height < 10:
                        c = column.collide(self.app.player)
                        if c > 0:
                            # do something when the player collides
                            if self.app.player.health % 3 == 0:
                                # lost a life
                                # reset to beginning of current level
                                self.reset()
                                self.next_state = ("LostLife", None)
                        elif c < 0:
                            # picked up a coin
                            player_points = [self.app.screen.projection(*point)
                                             for point in player_points]

                    points = self.mkpoints(x, y)
                    if column.name in self.enemies:
                        enemy = self.enemies[column.name]
                        draw_queue.append((y, enemy, points))
                    elif column.name:
                        print '[WARNING] Missing graphic:', column.name
                        self.app.screen.draw_polygon(pygame.Color('red'), points)

        # Draw all enemies (+player), back-to-front for proper stacking order
        for _, sprite, points in sorted(draw_queue, reverse=True):
            self.app.screen.draw_sprite(sprite, points)

        self.app.screen.draw_stats(self.app.player.coins_collected,
                                   self.app.player.health)


    def mkpoints(self, x, y, height=0.):
        return [
                self.map_coords(x-.45, height, y-.45 - self.time),
                self.map_coords(x+.45, height, y-.45 - self.time),
                self.map_coords(x+.45, height, y+.45 - self.time),
                self.map_coords(x-.45, height, y+.45 - self.time),
        ]

