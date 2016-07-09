from resman import FONT_STD, FONT_SMALL
from vmath import Matrix4x4, Vec3

class Screen(object):
    SPACING = 10

    def __init__(self, app, width, height):
        self.app = app
        self.width = width
        self.height = height

        projection = Matrix4x4.perspective(90.0 / 180.0 * 3.1415, self.width / self.height, 0.0001, 200.0)
        modelview = Matrix4x4.lookAt(Vec3(0.0, 3.0, -1.0), Vec3(0.0, -29.0, 100.0), Vec3(0.0, 1.0, 0.0))
        self.modelview_projection = projection * modelview

    def draw_text(self, lines):
        spacing = 10
        surfaces = [self.app.resman.fonts[FONT_SMALL].render(line, True, (255, 255, 255)) for line in lines]
        total_height = (len(surfaces) - 1) * spacing + sum(surface.get_height() for surface in surfaces)
        y = (self.height - total_height) / 2
        for surface in surfaces:
            pos = ((self.width - surface.get_width()) / 2, y)
            self.app.renderer.draw(surface, pos)
            y += surface.get_height() + spacing

    def projection(self, x, y, z):
        result = self.modelview_projection.map_vec3(Vec3(x, y, z))
        return ((0.5 + 0.5 * -result.x) * self.width, (0.5 + 0.5 * -result.y) * self.height)

    def draw_sprite(self, sprite, pos, opacity, tint):
        p = lambda dx, dy, (x, y, z), f=0.45: self.projection(x+dx*f, y+dy*f, z)
        sprite.draw([p(-1, -1, pos), p(1, -1, pos), p(1, 1, pos), p(-1, 1, pos)], opacity, tint)

    def draw_stats(self, bonus, health):
        pos_x, pos_y = self.SPACING, self.SPACING
        icon = self.app.resman.sprites['pearlcount_icon-1']
        self.app.renderer.draw(icon, (pos_x, pos_y))

        pos_x += icon.w + self.SPACING
        text_surf = self.app.resman.fonts[FONT_STD].render('%d' % bonus, True, (255, 255, 0))
        self.app.renderer.draw(text_surf, (pos_x, pos_y-3))

        pos_x, pos_y = self.width, self.SPACING
        while health > 0:
            health, rest = health - 3, min(health, 3)
            sprite = self.app.resman.sprites['whale_ico-%d' % rest]
            icon_width = sprite.w
            pos_x -= icon_width + self.SPACING
            self.app.renderer.draw(sprite, (pos_x, pos_y))

    def draw_card(self, message, story=None, background=None, creatures=None):
        self.app.renderer.draw(background, (0, 0))

        pos_x = self.width/15
        card = self.app.resman.fonts[FONT_STD].render(message, False, (255, 255, 255))
        self.app.renderer.draw(card, (pos_x, self.height/2 + 50))

        if story:
            self.app.renderer.draw(self.app.resman.fonts[FONT_STD].render(story, False, (255, 255, 255)),
                                   (pos_x, self.height/2 + 100))

        if creatures:
            width = sum(creature.w for creature in creatures) + self.SPACING * len(creatures)
            pos_x = 3*self.width/4 - width/2
            pos_x = min(pos_x, self.width - width)
            for creature in creatures:
                pos_y = self.height/3 - creature.h/2
                self.app.renderer.draw(creature, (pos_x, pos_y))
                pos_x += creature.w + self.SPACING

    def draw_skip(self):
        text = self.app.resman.fonts[FONT_SMALL].render("[S] ... SKIP INTRO", False, (255, 255, 255))
        self.app.renderer.draw(text, (self.width - text.get_width() - self.SPACING,
                                      self.height - text.get_height() - self.SPACING))
