import pygame

class Screen(object):
    def __init__(self, title, width, height, fullscreen=True):
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
