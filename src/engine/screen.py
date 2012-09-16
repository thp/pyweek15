import pygame
from resman import FONT_STD, FONT_SMALL


class Screen(object):
    def __init__(self, app, title, width, height, fullscreen=True):
        self.app = app

        flags = 0
        if fullscreen:
            flags |= pygame.FULLSCREEN

        if self.app.renderer.IS_OPENGL:
            if self.app.renderer.IS_OPENGL_ES:
                flags |= 0x00000040 # SDL_OPENGLES
            else:
                flags |= pygame.OPENGL

        self.width = width
        self.height = height

        self.display = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption(title)

        # position of the camera
        self.zeye = width * 1.2   # Assumed distance from Screen
        self.xeye = width * 0.5   # Middle of the screen
        self.yeye = height * 0.33 # High horizon


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
            self.app.renderer.draw(surface, pos)


    def draw_polygon(self, color, points):
        """Project a polygon onto the screen.
        Coordinates are given in world coordinates."""
        points = [self.projection(*point) for point in points]
        pygame.draw.polygon(self.display, color, points, 1)


    def draw_sprite(self, y, sprite, points, tint):
        """Project a sprite onto the screen.
        Coordinates are given in world coordinates."""
        points = [self.projection(*point) for point in points]

        # Fade in enemy sprites coming from the back
        if y > 10:
            opacity = 1. - (y-10)/5.
            tint = map(lambda x: x*opacity, tint)
        else:
            opacity = 1.

        sprite.draw(self.display, points, opacity, tint)


    def draw_stats(self, bonus, health):
        """Draw bonus and health bar."""
        font = self.app.resman.font(FONT_STD)
        offset = 10

        # bonus
        pos_x, pos_y = offset, offset
        icon = self.app.resman.get_sprite("pearlcount_icon-1")
        self.app.renderer.draw(icon, (offset, offset))

        pos_x += icon.get_width() + offset
        text_surf = font.render('%d' % bonus, True, (255, 255, 0))
        self.app.renderer.draw(text_surf, (pos_x, pos_y-3))

        # health
        pos_x, pos_y = self.width, offset

        while health > 0:
            health, rest = health - 3, min(health, 3)
            sprite = self.app.resman.get_sprite("whale_ico-%d" % rest)
            icon_width = sprite.get_width()
            pos_x -= icon_width + offset
            self.app.renderer.draw(sprite, (pos_x, pos_y))


    def draw_message(self, message):
        """Overlay a message to the player."""
        font = self.app.resman.font(FONT_SMALL)

        msg_surf = font.render(message, True, (255, 255, 255))
        w, h = msg_surf.get_size()
        pos = (self.width / 2 - w / 2, self.height / 2 - h / 2)

        rect = (pos[0] - 10, pos[1] - 10, w + 20, h + 20)
        pygame.draw.rect(self.display, (0, 0, 0), rect)
        self.app.renderer.draw(msg_surf, pos)


    def draw_card(self, message, story=None, background=None, creatures=None):
        if background:
            self.app.renderer.draw(background, (0, 0))
        else:
            self.display.fill(pygame.Color('black'))

        font = self.app.resman.font(FONT_STD)
        color = pygame.Color('white')

        # main message
        pos_x = self.width/15
        card = font.render(message, False, color)
        self.app.renderer.draw(card, (pos_x, self.height/2 + 50))

        # additional message
        if story:
            card = font.render(story, False, color)
            self.app.renderer.draw(card, (pos_x, self.height/2 + 100))

        if creatures:
            width = sum(creature.get_width() for creature in creatures)
            width += 20 * len(creatures)

            pos_x = 3*self.width/4 - width/2
            pos_x = min(pos_x, self.width - width)
            for creature in creatures:
                pos_y = self.height/3 - creature.get_height()/2
                self.app.renderer.draw(creature, (pos_x, pos_y))
                pos_x += creature.get_width() + 20


    def draw_skip(self):
        font = self.app.resman.font(FONT_SMALL)
        text = font.render("[S] ... SKIP INTRO", False, pygame.Color('white'))
        pos = (self.width - text.get_width() - 10,
               self.height - text.get_height() - 10)
        self.app.renderer.draw(text, pos)

