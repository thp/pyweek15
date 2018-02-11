from .resman import FONT_STD, FONT_SMALL, FONT_BIG
from .vmath import Matrix4x4, Vec3


BTNSCALE = 1.5

class Button(object):
    def __init__(self, button, x, y, w, h, callback):
        self.button = button
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.finger = -1
        self.callback = callback

    def _contains(self, x, y):
        return self.x <= x < self.x + self.w and self.y <= y < self.y + self.h

    def on_pressed(self, x, y, finger):
        if self._contains(x, y):
            self.callback(True, self.button)
            self.finger = finger

    def on_moved(self, x, y, finger):
        if self.finger == finger:
            if not self._contains(x, y):
                self.callback(False, self.button)
                self.finger = -1
        elif self.finger == -1:
            if self._contains(x, y):
                self.callback(True, self.button)
                self.finger = finger

    def on_released(self, x, y, finger):
        if self.finger == finger:
            self.callback(False, self.button)
            self.finger = -1


class Screen(object):
    SPACING = 10

    def __init__(self, app, width, height):
        self.app = app
        self.width = width
        self.height = height
        self.touch = True
        self.buttons = []

        projection = Matrix4x4.perspective(90.0 / 180.0 * 3.1415, self.width // self.height, 0.0001, 200.0)
        modelview = Matrix4x4.lookAt(Vec3(0.0, 3.0, -1.0), Vec3(0.0, -29.0, 100.0), Vec3(0.0, 1.0, 0.0))
        self.modelview_projection = projection * modelview

    def draw_text(self, lines):
        surfaces = [self.app.resman.render_text(FONT_BIG, line) for line in lines]
        total_height = (len(surfaces) - 1) * self.SPACING + sum(surface.h for surface in surfaces)
        y = (self.height - total_height) / 2
        for surface in surfaces:
            self.app.renderer.draw(surface, ((self.width - surface.w) / 2, y))
            y += surface.h + self.SPACING

    def process_touch(self, event, x, y, finger):
        if not self.touch:
            return

        for button in self.buttons:
            if event == 0:
                button.on_pressed(x, y, finger)
            elif event == 1:
                button.on_moved(x, y, finger)
            elif event == 2:
                button.on_released(x, y, finger)

    def projection(self, x, y, z):
        result = self.modelview_projection.map_vec3(Vec3(x, y, z))
        return ((0.5 + 0.5 * -result.x) * self.width, (0.5 + 0.5 * -result.y) * self.height)

    def draw_sprite(self, sprite, pos, opacity, tint):
        p = lambda dx, dy, pos, f=0.45: self.projection(pos[0]+dx*f, pos[1]+dy*f, pos[2])
        sprite.draw([p(-1, -1, pos), p(1, -1, pos), p(1, 1, pos), p(-1, 1, pos)], opacity, tint)

    def draw_stats(self, bonus, health):
        icon = self.app.resman.sprites['pearlcount_icon-1']
        self.app.renderer.draw(icon, (self.SPACING, self.SPACING))

        text = self.app.resman.render_text(FONT_STD, '%d' % bonus)
        self.app.renderer.draw(text, (self.SPACING * 2 + icon.w, self.SPACING + (icon.h - text.h) / 2))

        pos_x, pos_y = self.width, self.SPACING
        while health > 0:
            health, rest = health - 3, min(health, 3)
            sprite = self.app.resman.sprites['whale_ico-%d' % rest]
            pos_x -= sprite.w + self.SPACING
            self.app.renderer.draw(sprite, (pos_x, pos_y))

    def set_buttons(self, ids, callback):
        btnpadding = 10
        btnsize = 64

        x = btnpadding
        y = self.height - btnpadding - btnsize * BTNSCALE

        self.buttons = []
        for button in ids:
            if button is None:
                x = self.width - (len(ids) - ids.index(None) - 1) * (btnsize * BTNSCALE + btnpadding)
                continue

            self.buttons.append(Button(button, x, y, btnsize * BTNSCALE, btnsize * BTNSCALE, callback))

            x += btnpadding + btnsize * BTNSCALE

    def draw_buttons(self, intermission):
        if not self.touch:
            return

        for button in self.buttons:
            self.app.renderer.draw(self.app.resman.buttons[button.button], (button.x, button.y),
                    BTNSCALE, 0.5 if button.finger == -1 else 1.0)

    def draw_card(self, message, story, background, creatures, skipable):
        self.app.renderer.draw(background, (0, 0))

        pos_x = self.width/15
        self.app.renderer.draw(self.app.resman.render_text(FONT_STD, message), (pos_x, self.height/2 + 50))
        self.app.renderer.draw(self.app.resman.render_text(FONT_STD, story), (pos_x, self.height/2 + 100))

        width = sum(creature.w for creature in creatures) + self.SPACING * len(creatures)
        pos_x = 3*self.width/4 - width/2
        pos_x = min(pos_x, self.width - width)
        for creature in creatures:
            pos_y = self.height/3 - creature.h/2
            self.app.renderer.draw(creature, (pos_x, pos_y))
            pos_x += creature.w + self.SPACING

        if skipable and not self.touch:
            text = self.app.resman.render_text(FONT_SMALL, "[S] ... SKIP INTRO")
            self.app.renderer.draw(text, (self.width - text.w - self.SPACING, self.height - text.h - self.SPACING))
