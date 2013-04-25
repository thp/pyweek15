
import pygame
from pygame import transform

import time
import math
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

def build_shader(typ, source):
    shader_id = glCreateShader(typ)
    glShaderSource(shader_id, source)
    glCompileShader(shader_id)
    log = glGetShaderInfoLog(shader_id)
    if log:
        print 'Shader Info Log:', log
    return shader_id

class ShaderEffect:
    def __init__(self, vertex_shader, fragment_shader):
        self.vertex_shader = build_shader(GL_VERTEX_SHADER, vertex_shader)
        self.fragment_shader = build_shader(GL_FRAGMENT_SHADER, fragment_shader)
        self.program = glCreateProgram()
        glAttachShader(self.program, self.vertex_shader)
        glAttachShader(self.program, self.fragment_shader)
        glLinkProgram(self.program)
        log = glGetProgramInfoLog(self.program)
        if log:
            print 'Program Info Log:', log

    def use(self):
        glUseProgram(self.program)

    def attrib(self, name):
        return glGetAttribLocation(self.program, name)

    def uniform(self, name):
        return glGetUniformLocation(self.program, name)


class Framebuffer:
    def __init__(self, width, height):
        self.started = time.time()
        self.width = width
        self.height = height
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height,
                0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glBindTexture(GL_TEXTURE_2D, 0)
        self.framebuffer_id = glGenFramebuffers(1)

        self.bind()
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,
                GL_TEXTURE_2D, self.texture_id, 0)
        self.unbind()

    def __del__(self):
        glDeleteFramebuffers(self.framebuffer_id)
        glDeleteTextures(self.texture_id)

    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer_id)

    def unbind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def rerender(self, effect):
        # render self.texture_id as full screen quad
        texcoords = array.array('f', [
            0, 0,
            0, 1,
            1, 0,
            1, 1,
        ])
        vtxcoords = array.array('f', [
            -1, -1, 0,
            -1, 1, 0,
            1, -1, 0,
            1, 1, 0,
        ])

        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        effect.use()

        vtxcoords_s = vtxcoords.tostring()
        pos = effect.attrib('position')
        glEnableVertexAttribArray(pos)
        glVertexAttribPointer(pos, 3, GL_FLOAT, GL_FALSE, 0, vtxcoords_s)

        texcoords_s = texcoords.tostring()
        tex = effect.attrib('texcoord')
        glEnableVertexAttribArray(tex)
        glVertexAttribPointer(tex, 2, GL_FLOAT, GL_FALSE, 0, texcoords_s)

        dim = effect.uniform('dimensions')
        glUniform2f(dim, self.width, self.height)

        tim = effect.uniform('time')
        glUniform1f(tim, time.time() - self.started)

        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

        glDisableVertexAttribArray(pos)
        glDisableVertexAttribArray(tex)
        glUseProgram(0)

class Renderer:
    IS_OPENGL = True
    IS_OPENGL_ES = is_gles

    def __init__(self, app):
        if is_gles:
            sdl.SDL_GL_SetAttribute(17, 1) #SDL_GL_CONTEXT_MAJOR_VERSION

        self.app = app
        self.tmp_sprite = None
        self.framebuffer = None
        self.framebuffer2 = None
        self.effect_pipeline = []
        self.postprocessed = False
        self.global_offset_x = 0
        self.global_offset_y = 0
        self.global_tint = 1., 1., 1.

    def setup(self, size):
        glClearColor(0, 0, 0, 1)

        width, height = size
        offset_x, offset_y = self.app.screen.offset
        scale = self.app.screen.scale

        glViewport(0, 0, width, height)

        glEnable(GL_TEXTURE_2D)

        self.framebuffer = Framebuffer(width, height)
        self.framebuffer2 = Framebuffer(width, height)

        effect_vertex_shader = """
            attribute vec4 position;
            attribute vec2 texcoord;

            varying vec2 tex;

            void main()
            {
                gl_Position = position;
                tex = texcoord;
            }
        """

        self.draw_sprites = ShaderEffect("""
            attribute vec4 position;
            attribute vec2 texcoord;

            uniform vec2 size;
            uniform vec2 offset;
            uniform float scale;

            varying vec2 tex;

            void main()
            {
                gl_Position.x = 2.0 * (position.x*scale + offset.x) / size.x - 1.0;
                gl_Position.y = 1.0 - 2.0 * (position.y*scale + offset.y) / size.y;
                gl_Position.z = 0.0;
                gl_Position.w = 1.0;

                tex = texcoord;
            }
        """, """
            uniform sampler2D sampler;
            uniform vec4 color;

            varying vec2 tex;

            void main()
            {
                gl_FragColor = color * texture2D(sampler, tex);
            }
        """)

        self.sepia_effect = ShaderEffect(effect_vertex_shader, """
            uniform sampler2D sampler;

            varying vec2 tex;

            void main()
            {
                vec4 color = texture2D(sampler, tex);
                float mean = (color.x + color.y + color.z) / 3.0;
                gl_FragColor = vec4(mean * 1.2, mean * 1.1, mean, 1);
            }
        """)

        self.blur_effect = ShaderEffect(effect_vertex_shader, """
            uniform sampler2D sampler;
            uniform vec2 dimensions;

            varying vec2 tex;

            void main()
            {
                float radius = 10.0 * abs(0.3 - tex.y);
                vec2 offset = vec2(radius / dimensions.x, radius / dimensions.y);
                gl_FragColor = 0.3 * texture2D(sampler, tex)
                             + 0.1 * texture2D(sampler, tex + vec2(0, -offset.y))
                             + 0.1 * texture2D(sampler, tex + vec2(0, offset.y))
                             + 0.1 * texture2D(sampler, tex + vec2(-offset.x, 0))
                             + 0.1 * texture2D(sampler, tex + vec2(offset.x, 0))
                             + 0.075 * texture2D(sampler, tex + vec2(-offset.x, -offset.y))
                             + 0.075 * texture2D(sampler, tex + vec2(offset.x, offset.y))
                             + 0.075 * texture2D(sampler, tex + vec2(-offset.x, offset.y))
                             + 0.075 * texture2D(sampler, tex + vec2(offset.x, -offset.y));
            }
        """)

        self.underwater_effect = ShaderEffect(effect_vertex_shader, """
            uniform sampler2D sampler;
            uniform vec2 dimensions;
            uniform float time;

            varying vec2 tex;

            void main()
            {
                // Shift texture lookup sideways depending on Y coordinate + time
                vec2 pos = tex + vec2(6.0*sin(pow(tex.y, 2.0)*20.0+time)/dimensions.x, 0.0);
                vec4 color = texture2D(sampler, pos);

                // Vignette effect (brightest at center, darker towards edges)
                float lum = 1.0 - length(tex - vec2(0.5, 0.5));

                // blue-green'ish tint base color
                vec4 tint = vec4(0.0, 0.01, 0.05, 1.0);

                // Vignette color is also blue-green'ish
                vec4 vignette = vec4(lum * 0.7, lum * 0.9, lum, 1.0);

                gl_FragColor = tint + vignette * color;
            }
        """)

        self.effect_pipeline = [self.blur_effect, self.underwater_effect]#, self.sepia_effect]

        # Configure constant uniforms of draw_sprites
        self.draw_sprites.use()
        size_loc = self.draw_sprites.uniform('size') # vec2
        offset_loc = self.draw_sprites.uniform('offset') # vec2
        scale_loc = self.draw_sprites.uniform('scale') # float
        glUniform2f(size_loc, width, height)
        glUniform2f(offset_loc, offset_x, offset_y)
        glUniform1f(scale_loc, scale)
        glUseProgram(0)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def register_sprite(self, name, sprite):
        # Upload the sprite as a texture
        return SpriteProxy(sprite)

    def begin(self):
        if self.effect_pipeline:
            self.postprocessed = False
            self.framebuffer.bind()
        glClear(GL_COLOR_BUFFER_BIT)

    def draw(self, sprite, pos, scale=1., opacity=1., tint=(1., 1., 1.)):
        self.draw_sprites.use()

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

        color_loc = self.draw_sprites.uniform('color') # vec4
        glUniform4f(color_loc, r*gr, g*gg, b*gb, opacity)

        vertices = array.array('f', [
            x, y, 0.,
            x, y+h*scale, 0.,
            x+w*scale, y, 0.,
            x+w*scale, y+h*scale, 0.,
        ])

        glBindTexture(GL_TEXTURE_2D, sprite._texture_id)

        vertices_data = vertices.tostring()
        position_loc = self.draw_sprites.attrib('position')
        glEnableVertexAttribArray(position_loc)
        glVertexAttribPointer(position_loc, 3, GL_FLOAT, GL_FALSE, 0, vertices_data)

        texcoord_data = sprite._texcoords.tostring()
        texcoord_loc = self.draw_sprites.attrib('texcoord')
        glEnableVertexAttribArray(texcoord_loc)
        glVertexAttribPointer(texcoord_loc, 2, GL_FLOAT, GL_FALSE, 0, texcoord_data)

        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

        glDisableVertexAttribArray(texcoord_loc)
        glDisableVertexAttribArray(position_loc)

        glUseProgram(0)

    def begin_overlay(self):
        # Force postprocessing NOW, so overlays will be drawn as-is
        self.postprocess()

    def postprocess(self):
        if not self.effect_pipeline:
            return

        self.framebuffer.unbind()

        # Apply effects by drawing between framebuffers and
        # finally rendering the last effect to the screen
        a, b = self.framebuffer, self.framebuffer2

        for idx, effect in enumerate(self.effect_pipeline):
            if idx < len(self.effect_pipeline) - 1:
                b.bind()
            glClear(GL_COLOR_BUFFER_BIT)
            a.rerender(effect)
            if idx < len(self.effect_pipeline) - 1:
                b.unbind()
            a, b = b, a

        self.postprocessed = True

    def finish(self):
        if self.effect_pipeline and not self.postprocessed:
            self.postprocess()

        if is_gles:
            sdl.SDL_GL_SwapBuffers()
        else:
            pygame.display.flip()

