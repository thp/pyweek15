
import pygame
from pygame import transform

import random
import array

try:
    from OpenGL.GL import *
    is_gles = False
except ImportError:
    print "Warning: Cannot import OpenGL - trying fallback on GLES v1"
    # on MeeGo Harmattan
    from gles1 import *
    from ctypes import *
    sdl = CDLL('libSDL-1.2.so.0')
    is_gles = True

class SpriteProxy:
    def __init__(self, sprite):
        self._sprite = sprite
        self._texcoords = None
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glActiveTexture(GL_TEXTURE0)
        if is_gles:
            texture_id = GLint(0)
            glGenTextures(1, byref(texture_id))
            texture_id = texture_id.value
        else:
            texture_id = glGenTextures(1)
        self._texture_id = texture_id
        glBindTexture(GL_TEXTURE_2D, self._texture_id)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        self._load_from(sprite)

    def __del__(self):
        # Make sure to cleanup GL state to not leak textures
        glDeleteTextures(self._texture_id)

    def _make_powerof2(self, surface):
        if not is_gles:
            return surface

        # Converts a surface so that it becomes a power-of-2 surface
        # (both width and height are a power of 2)

        w, h = surface.get_size()
        def next_power_of2(i):
            x = 2
            while x < i:
                x *= 2
            return x

        result = pygame.Surface((next_power_of2(w), next_power_of2(h)),
            0, 32).convert_alpha()
        result.fill((0, 0, 0, 0))
        result.blit(surface, (0, 0))
        return result

    def _load_from(self, sprite):
        w0, h0 = sprite.get_size()
        self._sprite = sprite

        # Make power-of-2 textures for GLES v1 devices
        sprite = self._make_powerof2(sprite)
        w, h = sprite.get_size()

        wf = float(w0)/float(w)
        hf = float(h0)/float(h)

        # Account for the different texture size by making
        # the texture coordinates use only part of the image
        self._texcoords = array.array('f', [
            0, 1,
            0, 1.-hf,
            wf, 1,
            wf, 1.-hf,
        ])

        data = pygame.image.tostring(sprite, 'RGBA', 1)
        glBindTexture(GL_TEXTURE_2D, self._texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h,
                0, GL_RGBA, GL_UNSIGNED_BYTE, data)

    def __getattr__(self, name):
        # Forward normal attribute requests to the sprite itself
        return getattr(self._sprite, name)

class Renderer:
    IS_OPENGL = True
    IS_OPENGL_ES = is_gles

    def __init__(self, app):
        if is_gles:
            sdl.SDL_GL_SetAttribute(17, 1) #SDL_GL_CONTEXT_MAJOR_VERSION

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
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_TEXTURE_2D)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
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
        glTexCoordPointer(2, GL_FLOAT, 0, sprite._texcoords.tostring())
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    def finish(self):
        if is_gles:
            sdl.SDL_GL_SwapBuffers()
        else:
            pygame.display.flip()

