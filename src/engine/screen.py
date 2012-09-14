import pygame


class Screen(object):
    def __init__(self, app, title, width, height, fullscreen=True):
        self.app = app

        flags = 0
        if fullscreen:
            flags = pygame.FULLSCREEN

        self.width = width
        self.height = height

        self.display = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption(title)

        # position of the camera
        self.zeye = width * 1.2   # Assumed distance from Screen
        self.xeye = width * 0.5   # Middle of the screen
        self.yeye = height * 0.33 # High horizon


    def update(self):
        pygame.display.update()


    def projection(self, x, y, z):
        """Project world coordinates onto the screen.
        The world's dimensions are 1x1xWORLD_DEPTH"""

        x = x * self.width
        y = y * self.height
        z = z * self.width

        # projection
        xs = (self.zeye * (x - self.xeye)) / (self.zeye + z) + self.xeye
        ys = (self.zeye * (y - self.yeye)) / (self.zeye + z) + self.yeye

        return (xs, ys)

 
    def draw_polygon(self, color, points):
        """Project a polygon onto the screen.
        Coordinates are given in world coordinates."""
        points = [self.projection(*point) for point in points]
        pygame.draw.polygon(self.display, color, points, 1)


    def draw_sprite(self, sprite, points):
        """Project a sprite onto the screen.
        Coordinates are given in world coordinates."""
        points = [self.projection(*point) for point in points]
        sprite.draw(self.display, points)


    def draw_stats(self, bonus, health):
        """Draw bonus and health bar."""
        font = self.app.resman.font("visitor2", 48)

        # bonus
        text_surf = font.render('%d' % bonus, True, (255, 255, 0))
        self.display.blit(text_surf, (10, 0))
        self.display.blit(self.app.resman.get_sprite("pearl_icon"), (35, -26))

        # health
        icon_width = 30
        max_icons = 3
        icon_spacing = 10
        x_offset = self.width - (max_icons * (icon_width + icon_spacing) + icon_spacing)
        y_offset = 5

        for i in range(max_icons-1, -1, -1):
            health, rest = min(health, 3*i), max(health - 3*i, 0)
            sprite = self.app.resman.get_sprite("whale_ico_%d" % rest)
            self.display.blit(sprite, (x_offset + i * (icon_width + icon_spacing), y_offset))


    def draw_message(self, message):
        """Overlay a message to the player."""
        font = self.app.resman.font("visitor2", 48)

        msg_surf = font.render(message, True, (255, 255, 255))
        w, h = msg_surf.get_size()
        pos = (self.width / 2 - w / 2, self.height / 2 - h / 2)

        rect = (pos[0] - 10, pos[1] - 10, w + 20, h + 20)
        pygame.draw.rect(self.display, (0, 0, 0), rect)
        self.display.blit(msg_surf, pos)
