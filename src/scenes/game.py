
from engine.scene import Scene
from logic.level import Level
from logic.player import Player

from logic.lamemath import center, center_in, shade_color

from pygame import draw, font
from pygame.locals import *

import math

# XXX: This should be removed once we have proper gfx
colors = {
    'coin': (255, 255, 0),
    'stone': (0, 0, 255),
    'lanternfish': (0, 255, 0),
    'sixpack': (100, 100, 100),
}

MIN_DEST_X = 0
MAX_DEST_X = 4

class Game(Scene):
    DEPTH = 15

    # keyboard repeat rate (modulo) -> higher value = less repeat
    KEYBOARD_REPEAT_MOD = 7

    def __init__(self, app):
        super(Game, self).__init__(app)
        self.time = 0.
        self.i = 0
        self.direction = 0
        self.font = font.SysFont('dejavu sans', 16)

        self.level = Level(app.get_filename('levels/level1.txt'))
        self.player = Player(app)

        self.width = 0
        self.height = 0

    def resume(self, *args):
        pass

    def process(self):
        self.i += 1

        self.time += .01 * self.level.speed
        if self.time > 1.:
            self.time -= 1.
            self.player.y += 1

        if self.i % self.KEYBOARD_REPEAT_MOD == 0:
            next_x = self.player.dest_x + self.direction
            if next_x >= MIN_DEST_X and next_x <= MAX_DEST_X:
                self.player.dest_x += self.direction

        self.player.step()

        if self.player.health <= 0:
            print 'YOU ARE DEAD!'
            self.next_state = ("GoodBye", None)

        return super(Game, self).process()

    def process_input(self, event):
        def go_left():
            self.direction = -1
            self.i = 0
            if self.player.dest_x > MIN_DEST_X:
                self.player.dest_x -= 1

        def go_right():
            self.direction = 1
            self.i = 0
            if self.player.dest_x < MAX_DEST_X:
                self.player.dest_x += 1

        if event.type == QUIT:
            self.next_state = ("GoodBye", None)
        elif event.type == MOUSEBUTTONDOWN:
            x, y = event.pos

            if y < self.height / 2:
                self.player.jump()

            if x < self.width / 3:
                go_left()
            elif x > self.width * 2 / 3:
                go_right()
        elif event.type == MOUSEBUTTONUP:
            self.direction = 0
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                pass
            elif event.key == K_SPACE:
                self.player.jump()
            elif event.key == K_ESCAPE:
                self.next_state = ("GoodBye", None)
            elif event.key == K_LEFT:
                go_left()
            elif event.key == K_RIGHT:
                go_right()
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                self.direction = 0
            elif event.key == K_RIGHT:
                self.direction = 0

    def map_coords(self, x, y, z):
        """
        Map 3D coordinates to 2D coordinates

        These are not "real" screen coordinates, but imaginary 2D coordinates
        based on the lanes (x = 0..5, y = ???, z = 0..DEPTH+1)
        """
        w = self.width
        h = self.height
        z = self.DEPTH - z + self.time
        xoffset = (x-2)*100./(.0000001+math.pow(self.DEPTH-z+2, .2))
        yoffset = z*(h/float(self.DEPTH))
        xoffset *= yoffset/500.
        return (w/2+xoffset, h/5 + yoffset*2/3 - y)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.app.resman.get_sprite('bg'), (0, 0))
        self.width, self.height = screen.get_size()
        for yidx, offset in enumerate(range(self.player.y, self.player.y+self.DEPTH)):
            if offset < len(self.level.rows):
                for xidx, column in enumerate(self.level.rows[offset].items):
                    if column is None:
                        continue

                    color = colors.get(column.name, (0, 0, 0))

                    x = xidx
                    y = yidx

                    if yidx == 1 and xidx == self.player.dest_x and self.player.height < 10:
                        if column.collide(self.player):
                            # do something when the player collides
                            pass

                    points = self.mkpoints(x, y)
                    color = shade_color(color, yidx-self.time, self.DEPTH)
                    draw.polygon(screen, color, points)
                    #text_surf = self.font.render('%d/%d' % (xidx, yidx), True, (255, 0, 255))
                    #screen.blit(text_surf, center_in(text_surf, center(points)))

        x = self.player.x
        y = self.time
        points = self.mkpoints(x, y, self.player.height)
        self.player.draw(screen, points[3])
        draw.polygon(screen, (255, 255, 255), points, 1)

        text_surf = self.font.render('Coins: %d' % (self.player.coins_collected,), True, (255, 255, 0))
        screen.blit(text_surf, (20, 20))

        text_surf = self.font.render('Health:', True, (0, 255, 0))
        screen.blit(text_surf, (self.width - 100 - 20 - 10 - text_surf.get_size()[0], 20 + 15./2 - text_surf.get_size()[1]/2.))
        draw.rect(screen, (90, 0, 0), (self.width - 100 - 20, 20, 100, 15))
        draw.rect(screen, (0, 90, 0), (self.width - 100 - 20, 20, self.player.health, 15))

    def mkpoints(self, x, y, height=0.):
        return [
                self.map_coords(x-.45, height, y-.45),
                self.map_coords(x+.45, height, y-.45),
                self.map_coords(x+.45, height, y+.45),
                self.map_coords(x-.45, height, y+.45),
        ]

