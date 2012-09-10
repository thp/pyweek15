
from ..engine.scene import Scene
from ..logic.level import Level

import pygame
from pygame import draw, font
from pygame.locals import *

import math

colors = {
    'coin': (255, 255, 0),
    'stone': (0, 0, 255),
    'lanternfish': (0, 255, 0),
    'sixpack': (100, 100, 100),
}

def center(points):
    sum_x, sum_y = map(sum, zip(*points))
    return float(sum_x) / len(points), float(sum_y) / len(points)

def center_in(surf, center_point):
    x, y = center_point
    w, h = surf.get_size()
    return x-w/2, y-h/2

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dest_x = 0

    def step(self):
        self.x = self.x * .5 + self.dest_x * .5



class Game(Scene):
    DEPTH = 15

    def __init__(self, app):
        super(Game, self).__init__(app)
        self.time = 0.
        self.font = font.SysFont('dejavu sans', 16)

        self.level = Level(app.get_filename('level.txt'))
        self.player = Player()

        self.width = 0
        self.height = 0

    def resume(self, *args):
        pass

    def process(self):
        self.time += .1
        if self.time > 1.:
            self.time -= 1.
            self.player.y += 1
        self.player.step()

        return super(Game, self).process()

    def process_input(self, event):
        if event.type == QUIT:
            self.next_state = ("GoodBye", None)
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                pass
            elif event.key == K_LEFT:
                self.player.dest_x -= 1
            elif event.key == K_RIGHT:
                self.player.dest_x += 1
            elif event.key == K_ESCAPE:
                self.next_state = ("GoodBye", None)

    def map_coords(self, x, y, z):
        w = self.width
        h = self.height
        xoffset = (x-2)*100./(.0000001+math.pow(self.DEPTH-z+2, .2))
        yoffset = z*(h/float(self.DEPTH))
        xoffset *= yoffset/500.
        return (w/2+xoffset, h/5 + yoffset*2/3)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.width, self.height = screen.get_size()
        for yidx, offset in enumerate(range(self.player.y, self.player.y+self.DEPTH)):
            if offset < len(self.level.rows):
                for xidx, column in enumerate(self.level.rows[offset].items):
                    if column is None:
                        continue

                    color = colors.get(column.name, (0, 0, 0))

                    y = self.DEPTH - yidx + self.time
                    x = xidx

                    if yidx == 1 and xidx == self.player.dest_x:
                        color = (255, 0, 0)

                    points = [
                            self.map_coords(x-.45, 0, y-.45),
                            self.map_coords(x+.45, 0, y-.45),
                            self.map_coords(x+.45, 0, y+.45),
                            self.map_coords(x-.45, 0, y+.45),
                    ]
                    draw.polygon(screen, color, points)
                    text_surf = self.font.render('%d/%d' % (xidx, yidx), True, (255, 0, 255))
                    screen.blit(text_surf, center_in(text_surf, center(points)))

        x = self.player.x
        y = self.DEPTH
        points = [
                self.map_coords(x-.45, 0, y-.45),
                self.map_coords(x+.45, 0, y-.45),
                self.map_coords(x+.45, 0, y+.45),
                self.map_coords(x-.45, 0, y+.45),
        ]
        draw.polygon(screen, (255, 255, 255), points)

