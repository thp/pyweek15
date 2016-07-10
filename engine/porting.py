import pygame
import os
import glob

from core import sin, cos, sqrt, time_seconds, randint, randuniform, load_image, render_text
from core import draw_init, draw_clear, draw_quad, Texture, Framebuffer, ShaderProgram

from pygame.locals import KEYDOWN, KEYUP, QUIT, K_ESCAPE, K_SPACE, K_s, K_LEFT, K_RIGHT, K_UP

KEYMAP = {K_ESCAPE: 'esc', K_SPACE: ' ', K_s: 's', K_LEFT: 'left', K_RIGHT: 'right', K_UP: 'up'}

class Window():
    def __init__(self, width, height, title):
        pygame.init()
        self.display = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption(title)

    def swap_buffers(self):
        pygame.display.flip()

    def next_event(self):
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                return True, False, None, None
            elif event.type == KEYDOWN:
                return False, True, True, KEYMAP.get(event.key, None)
            elif event.type == KEYUP:
                return False, True, False, KEYMAP.get(event.key, None)

        return False, False, None, None

def get_lines(filename):
    return open(filename).read().splitlines()

def file_path(*args):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data', *args)

def find_files(*args):
    return glob.glob(file_path(*args))

class Font():
    def __init__(self, size):
        self.size = size

    def render(self, text):
        result = render_text(text)
        result.w *= self.size
        result.h *= self.size
        return result

class Sound():
    def __init__(self, filename):
        self._sound = pygame.mixer.Sound(filename)

    def play(self):
        pygame.mixer.find_channel(True).play(self._sound)
