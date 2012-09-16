
import pygame
from pygame import transform

import random
import array

from OpenGL.GL import *

texcoords = array.array('f', [
    0, 1,
    0, 0,
    1, 1,
    1, 0,
])

class SpriteProxy:
    def __init__(self, sprite):
        self._sprite = sprite
        self._texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self._texture_id)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        self._load_from(sprite)

    def __del__(self):
        # Make sure to cleanup GL state to not leak textures
        glDeleteTextures(self._texture_id)

    def _load_from(self, sprite):
        glBindTexture(GL_TEXTURE_2D, self._texture_id)
        self._sprite = sprite
        w, h = self._sprite.get_size()
        data = pygame.image.tostring(sprite, 'RGBA', 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h,
                0, GL_RGBA, GL_UNSIGNED_BYTE, data)

    def __getattr__(self, name):
        # Forward normal attribute requests to the sprite itself
        return getattr(self._sprite, name)

class Renderer:
    IS_OPENGL = True

    def __init__(self, app):
        self.app = app
        self.tmp_sprite = None
        self.global_offset_x = 0
        self.global_offset_y = 0
        self.global_tint = 1., 1., 1.

    def setup(self, size):
        glClearColor(0, 0, 0, 1)

        width, height = size
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, height, 0, 0, 1)

        glTexCoordPointer(2, GL_FLOAT, 0, texcoords.tostring())
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnable(GL_TEXTURE_2D)

        glEnableClientState(GL_VERTEX_ARRAY)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def register_sprite(self, name, sprite):
        # Upload the sprite as a texture
        return SpriteProxy(sprite)

    def begin(self):
        glClear(GL_COLOR_BUFFER_BIT)

    def draw(self, sprite, pos, scale=1., opacity=1., tint=(1., 1., 1.)):
        if not hasattr(sprite, '_sprite'):
            # Upload dynamically-created sprite to texture memory
            if self.tmp_sprite is None:
                self.tmp_sprite = SpriteProxy(sprite)
            else:
                self.tmp_sprite._load_from(sprite)
            sprite = self.tmp_sprite

        w, h = map(float, sprite.get_size())
        x, y = map(float, pos)
        x += self.global_offset_x
        y += self.global_offset_y

        r, g, b = tint
        gr, gg, gb = self.global_tint
        glColor(r*gr, g*gg, b*gb, opacity)
        vertices = array.array('f', [
            x, y, 0.,
            x, y+h*scale, 0.,
            x+w*scale, y, 0.,
            x+w*scale, y+h*scale, 0.,
        ])

        glBindTexture(GL_TEXTURE_2D, sprite._texture_id)
        glVertexPointer(3, GL_FLOAT, 0, vertices.tostring())
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    def finish(self):
        pygame.display.flip()

