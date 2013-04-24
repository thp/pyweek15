
import pygame

from pygame import transform

class Renderer:
    IS_OPENGL = False

    def __init__(self, app):
        self.app = app
        self.global_offset_x = 0
        self.global_offset_y = 0
        # The global tint is ignored in this renderer
        self.global_tint = 1., 1., 1.

    def setup(self, size):
        pass

    def register_sprite(self, name, sprite):
        return sprite

    def begin(self):
        self.app.screen.display.fill((0, 0, 0))

    def begin_overlay(self):
        pass

    def draw(self, sprite, pos, scale=None, opacity=1., tint=None):
        # Opacity is ignored in this blitting renderer
        # Tint is also ignored in this blitting renderer
        x, y = pos
        x += self.global_offset_x
        y += self.global_offset_y
        if scale is not None:
            w, h = sprite.get_size()
            sprite = transform.scale(sprite, (int(w*scale), int(h*scale)))
        self.app.screen.display.blit(sprite, (x, y))

    def finish(self):
        pygame.display.update()

