from porting import time_seconds, Texture, ShaderProgram, Framebuffer, draw_init, draw_quad, draw_clear

class Renderer():
    def __init__(self, app):
        self.app = app
        self.postprocessed = False
        self.global_tint = 1., 1., 1.
        self.started = time_seconds()

    def resize(self, width, height):
        draw_init()
        self.fbs = [Framebuffer(width, height), Framebuffer(width, height)]

        mkshader = lambda vert, frag: ShaderProgram(self.app.resman.shaders[vert], self.app.resman.shaders[frag])
        self.draw_sprites = mkshader('draw_sprites.vsh', 'draw_sprites.fsh')
        self.blur_effect = mkshader('effect_vertex_shader.vsh', 'blur_effect.fsh')
        self.underwater_effect = mkshader('effect_vertex_shader.vsh', 'underwater_effect.fsh')
        self.effect_pipeline = [self.blur_effect, self.underwater_effect]

        self.draw_sprites.bind()
        self.draw_sprites.uniform2f('size', width, height)

    def upload_texture(self, width, height, rgba):
        return Texture(width, height, rgba)

    def begin(self):
        if self.effect_pipeline:
            self.postprocessed = False
            self.fbs[0].bind()
        draw_clear()

    def draw(self, texture, pos, scale=1., opacity=1., tint=(1., 1., 1.)):
        x, y = pos
        r, g, b = tint
        gr, gg, gb = self.global_tint
        hs, ws = texture.h * scale, texture.w * scale

        self.draw_sprites.enable_arrays(texture, [x,y,x,y+hs,x+ws,y,x+ws,y+hs], [0,1,0,0,1,1,1,0])
        self.draw_sprites.uniform4f('color', r*gr, g*gg, b*gb, opacity)
        draw_quad()

    def render_effect(self, effect, fbo):
        effect.enable_arrays(fbo.texture, [-1,-1,-1,1,1,-1,1,1], [0,0,0,1,1,0,1,1])
        effect.uniform2f('dimensions', fbo.texture.w, fbo.texture.h)
        effect.uniform1f('time', time_seconds() - self.started)
        draw_quad()

    def postprocess(self):
        if self.effect_pipeline and not self.postprocessed:
            self.fbs[0].unbind()
            a, b = self.fbs
            for idx, effect in enumerate(self.effect_pipeline[:-1]):
                b.bind()
                draw_clear()
                self.render_effect(effect, a)
                b.unbind()
                a, b = b, a
            draw_clear()
            self.render_effect(self.effect_pipeline[-1], a)
            self.postprocessed = True

    def finish(self):
        self.global_tint = 1., 1., 1.
        self.postprocess()
