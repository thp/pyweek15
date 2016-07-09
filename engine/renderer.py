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
        glBindAttribLocation(self.program, 0, 'position')
        glBindAttribLocation(self.program, 1, 'texcoord')
        glLinkProgram(self.program)

    def use(self):
        glUseProgram(self.program)

    def uniform(self, name):
        return glGetUniformLocation(self.program, name)

    def enable_arrays(self, position, texcoord):
        self.use()
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, array.array('f', position).tostring())
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, array.array('f', texcoord).tostring())

class Framebuffer:
    def __init__(self, width, height):
        self.started = time.time()
        self.framebuffer_id = glGenFramebuffers(1)
        self.texture = Texture(width, height, None)
        self.bind()
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.texture._texture_id, 0)
        self.unbind()

    def __del__(self):
        glDeleteFramebuffers(self.framebuffer_id)

    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer_id)

    def unbind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def rerender(self, effect):
        effect.enable_arrays([-1,-1,-1,1,1,-1,1,1], [0,0,0,1,1,0,1,1])
        glUniform2f(effect.uniform('dimensions'), self.texture.w, self.texture.h)
        glUniform1f(effect.uniform('time'), time.time() - self.started)
        glBindTexture(GL_TEXTURE_2D, self.texture._texture_id)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

class Renderer:
    def __init__(self, app):
        self.app = app
        self.postprocessed = False
        self.global_tint = 1., 1., 1.

    def resize(self, width, height):
        glClearColor(0, 0, 0, 1)
        glViewport(0, 0, width, height)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)

        self.fbs = [Framebuffer(width, height), Framebuffer(width, height)]

        mkshader = lambda vert, frag: ShaderEffect(self.app.resman.shaders[vert], self.app.resman.shaders[frag])
        self.draw_sprites = mkshader('draw_sprites.vsh', 'draw_sprites.fsh')
        self.blur_effect = mkshader('effect_vertex_shader.vsh', 'blur_effect.fsh')
        self.underwater_effect = mkshader('effect_vertex_shader.vsh', 'underwater_effect.fsh')
        self.effect_pipeline = [self.blur_effect, self.underwater_effect]

        self.draw_sprites.use()
        glUniform2f(self.draw_sprites.uniform('size'), width, height)

    def upload_texture(self, width, height, rgba):
        return Texture(width, height, rgba)

    def begin(self):
        if self.effect_pipeline:
            self.postprocessed = False
            self.fbs[0].bind()
        glClear(GL_COLOR_BUFFER_BIT)

    def draw(self, sprite, pos, scale=1., opacity=1., tint=(1., 1., 1.)):
        if not isinstance(sprite, Texture):
            # Upload dynamically-created sprite to texture memory
            sprite = self.app.resman.upload_surface(sprite)

        x, y = pos
        r, g, b = tint
        gr, gg, gb = self.global_tint
        hs, ws = sprite.h * scale, sprite.w * scale

        self.draw_sprites.enable_arrays([x,y,x,y+hs,x+ws,y,x+ws,y+hs], [0,1,0,0,1,1,1,0])
        glBindTexture(GL_TEXTURE_2D, sprite._texture_id)
        glUniform4f(self.draw_sprites.uniform('color'), r*gr, g*gg, b*gb, opacity)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    def postprocess(self):
        if self.effect_pipeline and not self.postprocessed:
            self.fbs[0].unbind()
            a, b = self.fbs
            for idx, effect in enumerate(self.effect_pipeline[:-1]):
                b.bind()
                glClear(GL_COLOR_BUFFER_BIT)
                a.rerender(effect)
                b.unbind()
                a, b = b, a
            glClear(GL_COLOR_BUFFER_BIT)
            a.rerender(self.effect_pipeline[-1])
            self.postprocessed = True

    def finish(self):
        self.global_tint = 1., 1., 1.
        self.postprocess()
