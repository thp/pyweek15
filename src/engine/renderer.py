import time
import array

from OpenGL.GL import *

class Texture():
    def __init__(self, w, h, rgba):
        self.w = w
        self.h = h
        self._texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self._texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.w, self.h, 0, GL_RGBA, GL_UNSIGNED_BYTE, rgba)

    def __del__(self):
        glDeleteTextures(self._texture_id)

def build_shader(typ, source):
    shader_id = glCreateShader(typ)
    glShaderSource(shader_id, source)
    glCompileShader(shader_id)
    return shader_id

class ShaderEffect:
    def __init__(self, vertex_shader, fragment_shader):
        self.vertex_shader = build_shader(GL_VERTEX_SHADER, vertex_shader)
        self.fragment_shader = build_shader(GL_FRAGMENT_SHADER, fragment_shader)
        self.program = glCreateProgram()
        glAttachShader(self.program, self.vertex_shader)
        glAttachShader(self.program, self.fragment_shader)
        glLinkProgram(self.program)

    def use(self):
        glUseProgram(self.program)

    def attrib(self, name):
        return glGetAttribLocation(self.program, name)

    def uniform(self, name):
        return glGetUniformLocation(self.program, name)

class Framebuffer:
    def __init__(self, width, height):
        self.texcoords = array.array('f', [0, 0, 0, 1, 1, 0, 1, 1])
        self.vtxcoords = array.array('f', [-1, -1, -1, 1, 1, -1, 1, 1])
        self.started = time.time()
        self.width = width
        self.height = height
        self.texture_id = glGenTextures(1)
        self.framebuffer_id = glGenFramebuffers(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glBindTexture(GL_TEXTURE_2D, 0)
        self.bind()
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.texture_id, 0)
        self.unbind()

    def __del__(self):
        glDeleteFramebuffers(self.framebuffer_id)
        glDeleteTextures(self.texture_id)

    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer_id)

    def unbind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def rerender(self, effect):
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        effect.use()
        pos = effect.attrib('position')
        glEnableVertexAttribArray(pos)
        glVertexAttribPointer(pos, 2, GL_FLOAT, GL_FALSE, 0, self.vtxcoords.tostring())
        tex = effect.attrib('texcoord')
        glEnableVertexAttribArray(tex)
        glVertexAttribPointer(tex, 2, GL_FLOAT, GL_FALSE, 0, self.texcoords.tostring())
        glUniform2f(effect.uniform('dimensions'), self.width, self.height)
        glUniform1f(effect.uniform('time'), time.time() - self.started)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glDisableVertexAttribArray(pos)
        glDisableVertexAttribArray(tex)

class Renderer:
    def __init__(self, app):
        self.app = app
        self.fbs = [None, None]
        self.effect_pipeline = []
        self.postprocessed = False
        self.global_tint = 1., 1., 1.

    def setup(self, size):
        width, height = size
        offset_x, offset_y = self.app.screen.offset
        scale = self.app.screen.scale

        glClearColor(0, 0, 0, 1)
        glViewport(0, 0, width, height)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.fbs = [Framebuffer(width, height), Framebuffer(width, height)]

        self.draw_sprites = ShaderEffect(self.app.resman.get_shader('draw_sprites.vsh'),
                                         self.app.resman.get_shader('draw_sprites.fsh'))

        self.blur_effect = ShaderEffect(self.app.resman.get_shader('effect_vertex_shader.vsh'),
                                        self.app.resman.get_shader('blur_effect.fsh'))

        self.underwater_effect = ShaderEffect(self.app.resman.get_shader('effect_vertex_shader.vsh'),
                                              self.app.resman.get_shader('underwater_effect.fsh'))

        self.effect_pipeline = [self.blur_effect, self.underwater_effect]

        self.draw_sprites.use()
        glUniform2f(self.draw_sprites.uniform('size'), width, height)
        glUniform2f(self.draw_sprites.uniform('offset'), offset_x, offset_y)
        glUniform1f(self.draw_sprites.uniform('scale'), scale)

    def upload_texture(self, width, height, rgba):
        return Texture(width, height, rgba)

    def begin(self):
        if self.effect_pipeline:
            self.postprocessed = False
            self.fbs[0].bind()
        glClear(GL_COLOR_BUFFER_BIT)

    def draw(self, sprite, pos, scale=1., opacity=1., tint=(1., 1., 1.)):
        self.draw_sprites.use()

        if not isinstance(sprite, Texture):
            # Upload dynamically-created sprite to texture memory
            sprite = self.upload_texture(sprite.get_width(), sprite.get_height(), self.app.resman.get_rgba(sprite))

        w, h = map(float, (sprite.w, sprite.h))
        x, y = map(float, pos)

        r, g, b = tint
        gr, gg, gb = self.global_tint

        glUniform4f(self.draw_sprites.uniform('color'), r*gr, g*gg, b*gb, opacity)

        glBindTexture(GL_TEXTURE_2D, sprite._texture_id)

        vertices = array.array('f', [x, y, x, y+h*scale, x+w*scale, y, x+w*scale, y+h*scale])
        vertices_data = vertices.tostring()
        position_loc = self.draw_sprites.attrib('position')
        glEnableVertexAttribArray(position_loc)
        glVertexAttribPointer(position_loc, 2, GL_FLOAT, GL_FALSE, 0, vertices_data)

        texcoords = array.array('f', [0., 1., 0., 0., 1., 1., 1., 0.])
        texcoord_data = texcoords.tostring()
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

        self.fbs[0].unbind()

        a, b = self.fbs
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
        self.global_tint = 1., 1., 1.

        if self.effect_pipeline and not self.postprocessed:
            self.postprocess()
