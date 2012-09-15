import pygame
from resman import FONT_STD, FONT_SMALL


class Screen(object):
    def __init__(self, app, title, width, height, fullscreen=True):
        self.app = app

        flags = 0
        if fullscreen:
            flags = pygame.FULLSCREEN

        self.width = width
        self.height = height

        self.display = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption(title)

        # position of the camera
        self.zeye = width * 1.2   # Assumed distance from Screen
        self.xeye = width * 0.5   # Middle of the screen
        self.yeye = height * 0.33 # High horizon


    def clear(self):
        self.display.fill(pygame.Color('black'))

    def update(self):
        self.draw_debug()
        pygame.display.update()


    def projection(self, x, y, z):
        """Project world coordinates onto the screen.
        The world's dimensions are 1x1xWORLD_DEPTH"""

        x = x * self.width
        y = y * self.height
        z = z * self.width

        # projection
        xs = (self.zeye * (x - self.xeye)) / (self.zeye + z) + self.xeye
        ys = (self.zeye * (y - self.yeye)) / (self.zeye + z) + self.yeye

        return (xs, ys)

 
    def draw_debug(self):
            # display fps
            font = self.app.resman.font(FONT_SMALL)
            surface = font.render("FPS: %2.2f" % self.app._clock.get_fps(), False,
                                  pygame.Color('white'), pygame.Color('black'))
            pos = (self.width-surface.get_width(), self.height-surface.get_height())
            self.display.blit(surface, pos)


    def draw_polygon(self, color, points):
        """Project a polygon onto the screen.
        Coordinates are given in world coordinates."""
        points = [self.projection(*point) for point in points]
        pygame.draw.polygon(self.display, color, points, 1)


    def draw_sprite(self, sprite, points):
        """Project a sprite onto the screen.
        Coordinates are given in world coordinates."""
        points = [self.projection(*point) for point in points]
        sprite.draw(self.display, points)


    def draw_stats(self, bonus, health):
        """Draw bonus and health bar."""
        font = self.app.resman.font(FONT_STD)
        offset = 10

        # bonus
        pos_x, pos_y = offset, offset
        icon = self.app.resman.get_sprite("pearlcount_icon")
        self.display.blit(icon, (offset, offset))

        pos_x += icon.get_width() + offset
        text_surf = font.render('%d' % bonus, True, (255, 255, 0))
        self.display.blit(text_surf, (pos_x, pos_y-3))

        # health
        pos_x, pos_y = self.width, offset

        while health > 0:
            health, rest = health - 3, min(health, 3)
            sprite = self.app.resman.get_sprite("whale_ico_%d" % rest)
            icon_width = sprite.get_width()
            pos_x -= icon_width + offset
            self.display.blit(sprite, (pos_x, pos_y))


    def draw_message(self, message):
        """Overlay a message to the player."""
        font = self.app.resman.font(FONT_SMALL)

        msg_surf = font.render(message, True, (255, 255, 255))
        w, h = msg_surf.get_size()
        pos = (self.width / 2 - w / 2, self.height / 2 - h / 2)

        rect = (pos[0] - 10, pos[1] - 10, w + 20, h + 20)
        pygame.draw.rect(self.display, (0, 0, 0), rect)
        self.display.blit(msg_surf, pos)


    def draw_card(self, message, additional=None):
        self.display.fill(pygame.Color('black'))
        font = self.app.resman.font(FONT_STD)
        color = pygame.Color('white')

        offset = self.height/6 if additional else 0

        # main message
        card = font.render(message, False, color)
        center = ((self.width - card.get_width())/2,
                  (self.height - card.get_height())/2 - offset)
        self.display.blit(card, center)

        # additional message
        if additional:
            card = font.render(additional, False, color)
            center = ((self.width - card.get_width())/2,
                      (self.height - card.get_height())/2 + offset)
            self.display.blit(card, center)
