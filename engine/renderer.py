from core import time, ShaderProgram, Framebuffer

class Renderer():
    def __init__(self, app):
        self.app = app
        self.postprocessed = False
        self.global_tint = 1., 1., 1.
        self.started = time.time()

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.fbs = []

        mkshader = lambda vert, frag: ShaderProgram(self.app.resman.shaders[vert], self.app.resman.shaders[frag])
        self.draw_sprites = mkshader('draw_sprites.vsh', 'draw_sprites.fsh')
        self.effect_pipeline = []

        if Framebuffer.supported():
            self.fbs = [Framebuffer(width, height), Framebuffer(width, height)]
            self.blur_effect = mkshader('effect_vertex_shader.vsh', 'blur_effect.fsh')
            self.underwater_effect = mkshader('effect_vertex_shader.vsh', 'underwater_effect.fsh')
            self.effect_pipeline.extend([self.blur_effect, self.underwater_effect])

    def begin(self):
        Framebuffer.begin()
        if self.effect_pipeline:
            self.postprocessed = False
            self.fbs[0].bind()

    def draw(self, texture, pos, scale=1., opacity=1., tint=(1., 1., 1.)):
        x, y = pos
        r, g, b = tint
        gr, gg, gb = self.global_tint
        hs, ws = texture.h * scale, texture.w * scale
        self.draw_sprites.draw_quad(texture, [x,y,x,y+hs,x+ws,y,x+ws,y+hs], {
            'color': (r*gr, g*gg, b*gb, opacity),
            'size': (self.width, self.height),
        })

    def render_effect(self, effect, fbo):
        effect.draw_quad(fbo.texture, [-1,-1,-1,1,1,-1,1,1], {
            'time': (time.time() - self.started) % 314.1592653589793,
            'size': (fbo.texture.w, fbo.texture.h),
        })

    def postprocess(self):
        if self.effect_pipeline and not self.postprocessed:
            self.fbs[0].unbind()
            a, b = self.fbs
            for idx, effect in enumerate(self.effect_pipeline[:-1]):
                b.bind()
                self.render_effect(effect, a)
                b.unbind()
                a, b = b, a
            self.render_effect(self.effect_pipeline[-1], a)
            self.postprocessed = True

    def finish(self):
        self.global_tint = 1., 1., 1.
        self.postprocess()
        Framebuffer.finish()
