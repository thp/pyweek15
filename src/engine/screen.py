import math

from resman import FONT_STD, FONT_SMALL
from vmath import Matrix4x4, Vec3

import pygame
from pygame.locals import *

class Screen(object):
    def __init__(self, app, title, width, height, fullscreen=True):
        self.app = app

        flags = pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE
        if fullscreen:
            flags |= pygame.FULLSCREEN

        self.width = width
        self.height = height

        if fullscreen:
            size = (0, 0)
        else:
            size = (width, height)

        self.display = pygame.display.set_mode(size, flags)

        size = self.display.get_size()

        # Scale to fill the screen, with letterboxing
        self.scale = min(float(size[0]) / float(self.width),
                         float(size[1]) / float(self.height))

        # Calculate the offset for symmetric letterboxing
        self.offset = ((size[0] - self.width*self.scale) / 2,
                       (size[1] - self.height*self.scale) / 2)

        pygame.display.set_caption(title)

        self.eye_z_target = -1.0
        self.eye_y_target = 3.0
        self.center_y_target = -29.0
        self.center_z_target = 100.0

        self.eye_z = self.eye_z_target
        self.eye_y = self.eye_y_target
        self.center_y = self.center_y_target
        self.center_z = self.center_z_target

        self.fov = 90.0

        self.reset_camera()
        self.before_draw()

    def reset_camera(self):
        self.eye_z = 0.0
        self.eye_y = 200.0

    def process(self):
        alpha = 0.1
        self.eye_y = self.eye_y * (1.0 - alpha) + self.eye_y_target * alpha
        self.eye_z = self.eye_z * (1.0 - alpha) + self.eye_z_target * alpha
        self.center_y = self.center_y * (1.0 - alpha) + self.center_y_target * alpha
        self.center_z = self.center_z * (1.0 - alpha) + self.center_z_target * alpha

    def process_input(self, event):
        if event.type == KEYDOWN:
            if event.key == K_1:
                self.eye_y += 1.0
            elif event.key == K_2:
                self.eye_y -= 1.0
            elif event.key == K_3:
                self.center_y += 1.0
            elif event.key == K_4:
                self.center_y -= 1.0
            elif event.key == K_5:
                self.fov += 1.0
            elif event.key == K_6:
                self.fov -= 1.0

    def before_draw(self):
        projection = Matrix4x4.perspective(self.fov / 180.0 * math.pi, self.width / self.height, 0.0001, 200.0)

        eye = Vec3(0.0, self.eye_y, self.eye_z)
        center = Vec3(0.0, self.center_y, self.center_z)
        up = Vec3(0.0, 1.0, 0.0)

        modelview = Matrix4x4.lookAt(eye, center, up)
        self.modelview_projection = projection * modelview

    def projection(self, x, y, z):
        """Project world coordinates onto the screen."""

        # x = -1..+1      (lane)
        # y = 0..1        (jump height)
        # z = 0..10(?)    (depth/distance)

        result = self.modelview_projection.map_vec3(Vec3(x, y, z))

        return ((0.5 + 0.5 * -result.x) * self.width, (0.5 + 0.5 * -result.y) * self.height)

    def draw_text(self, text):
        font = self.app.resman.font(FONT_SMALL)
        surface = font.render(text, False, pygame.Color('white'), pygame.Color('black'))
        pos = ((self.width-surface.get_width()) / 2, self.height-surface.get_height())
        self.app.renderer.draw(surface, pos)

    def draw_sprite(self, sprite, pos, opacity, tint):
        """Project a sprite onto the screen.
        Coordinates are given in world coordinates."""

        x, y, z = pos

        delta = 0.45

        points = [
                self.projection(x-delta, y-delta, z),
                self.projection(x+delta, y-delta, z),
                self.projection(x+delta, y+delta, z),
                self.projection(x-delta, y+delta, z),
        ]

        #pygame.draw.polygon(self.display, pygame.Color('blue'), points, 2)

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

