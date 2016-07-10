import array
import pygame
import os
import glob

from core import sin, cos, sqrt, time_seconds, randint, randuniform
from core import draw_init, draw_clear, draw_quad, Texture, Framebuffer, ShaderProgram

from pygame.locals import KEYDOWN, KEYUP, QUIT, K_ESCAPE, K_SPACE, K_s, K_LEFT, K_RIGHT, K_UP

KEYMAP = {K_ESCAPE: 'esc', K_SPACE: ' ', K_s: 's', K_LEFT: 'left', K_RIGHT: 'right', K_UP: 'up'}

def create_window(width, height, title):
    pygame.init()
    result = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
    pygame.display.set_caption(title)
    return result

def swap_buffers():
    pygame.display.flip()

def next_event():
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            return True, False, None, None
        elif event.type == KEYDOWN:
            return False, True, True, KEYMAP.get(event.key, None)
        elif event.type == KEYUP:
            return False, True, False, KEYMAP.get(event.key, None)

    return False, False, None, None

def load_image(filename):
    surf = pygame.image.load(filename).convert_alpha()
    return (surf.get_width(), surf.get_height(), pygame.image.tostring(surf, 'RGBA', 1))

def get_lines(filename):
    return open(filename).read().splitlines()

def file_path(*args):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data', *args)

def find_files(*args):
    return glob.glob(file_path(*args))

class Font():
    def __init__(self, filename, size):
        self._font = pygame.font.Font(filename, size)

    def render(self, text):
        surf = self._font.render(text, True, (255, 255, 255))
        return (surf.get_width(), surf.get_height(), pygame.image.tostring(surf, 'RGBA', 1))

class Sound():
    def __init__(self, filename):
        self._sound = pygame.mixer.Sound(filename)

    def play(self):
        pygame.mixer.find_channel(True).play(self._sound)
