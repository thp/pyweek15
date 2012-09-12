class PickupScore(object):
    def __init__(self, app, (x, y), text, color=(255, 255, 100),
            fading=5, antigravity=4):
        self.x = x
        self.y = y
        self.text = text
        self.alpha = 255
        self.fading = fading
        self.antigravity = antigravity
        self.surf = app.font.render(text, True, color)

    def change_alpha(self, surface, alpha=255):
        size = surface.get_size()
        try:
            for y in xrange(size[1]):
                for x in xrange(size[0]):
                    r, g, b, a = surface.get_at((x, y))
                    surface.set_at((x, y), (r, g, b, alpha if a else 0))
        except:
            return surface
        return surface

    def process(self):
        """ It can be forgotten if it's faded out to below 0 """
        self.alpha -= self.fading
        self.y -= self.antigravity
        self.surf = self.change_alpha(self.surf, self.alpha)
        return self.alpha

    def draw(self, screen):
        screen.blit(self.surf, (self.x, self.y))
