import pygame

class Screen(object):
    def __init__(self, title, width, height, fullscreen=True):
        flags = 0
        if fullscreen:
            flags = pygame.FULLSCREEN

        self.display = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption(title)

        # position of the camera
        self.zeye = width * 1.2   # Assumed distance from Screen
        self.xeye = width * 0.5   # Middle of the screen
        self.yeye = height * 0.33 # High horizon


    def update(self):
        pygame.display.update()


    def projection(self, x, y, z):
        """Project 3D coordinates onto the screen."""

        # projection
        xs = (self.zeye * (x - self.xeye)) / (self.zeye + z) + self.xeye
        ys = (self.zeye * (y - self.yeye)) / (self.zeye + z) + self.yeye

        return (xs, ys)

