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
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.w, self.h, 0, GL_RGBA, GL_UNSIGNED_BYTE, rgba)

    __del__ = lambda self: glDeleteTextures(self._texture_id)

class ShaderEffect():
    def __init__(self, vertex_shader, fragment_shader):
        self.program = glCreateProgram()
        for shader_type, shader_src in ((GL_VERTEX_SHADER, vertex_shader), (GL_FRAGMENT_SHADER, fragment_shader)):
            shader_id = glCreateShader(shader_type)
            glShaderSource(shader_id, shader_src)
            glCompileShader(shader_id)
            glAttachShader(self.program, shader_id)
        glBindAttribLocation(self.program, 0, 'position')
        glBindAttribLocation(self.program, 1, 'texcoord')
        glLinkProgram(self.program)

    use = lambda self: glUseProgram(self.program)
    uniform = lambda self, name: glGetUniformLocation(self.program, name)
    __del__ = lambda self: glDeleteProgram(self.program)

    def enable_arrays(self, texture, position, texcoord):
        self.use()
        glBindTexture(GL_TEXTURE_2D, texture._texture_id)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, array.array('f', position).tostring())
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, array.array('f', texcoord).tostring())

class Framebuffer():
    def __init__(self, width, height):
        self.started = time.time()
        self.framebuffer_id = glGenFramebuffers(1)
        self.texture = Texture(width, height, None)
        self.bind()
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.texture._texture_id, 0)
        self.unbind()

    __del__ = lambda self: glDeleteFramebuffers(self.framebuffer_id)
    bind = lambda self: glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer_id)
    unbind = lambda self: glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def rerender(self, effect):
        effect.enable_arrays(self.texture, [-1,-1,-1,1,1,-1,1,1], [0,0,0,1,1,0,1,1])
        glUniform2f(effect.uniform('dimensions'), self.texture.w, self.texture.h)
        glUniform1f(effect.uniform('time'), time.time() - self.started)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

class Renderer():
    def __init__(self, app):
        self.app = app
        self.postprocessed = False
        self.global_tint = 1., 1., 1.

    def resize(self, width, height):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
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

    def draw(self, texture, pos, scale=1., opacity=1., tint=(1., 1., 1.)):
        x, y = pos
        r, g, b = tint
        gr, gg, gb = self.global_tint
        hs, ws = texture.h * scale, texture.w * scale

        self.draw_sprites.enable_arrays(texture, [x,y,x,y+hs,x+ws,y,x+ws,y+hs], [0,1,0,0,1,1,1,0])
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
