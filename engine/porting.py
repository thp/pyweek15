import array
import pygame
import os
import glob

from core import sin, cos, sqrt, time_seconds, randint, randuniform
from core import draw_init, draw_clear, draw_quad, Texture, Framebuffer

from OpenGL.GL import *

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

class ShaderProgram():
    def __init__(self, vertex_shader, fragment_shader):
        self.program = glCreateProgram()
        for shader_type, shader_src in ((GL_VERTEX_SHADER, vertex_shader), (GL_FRAGMENT_SHADER, fragment_shader)):
            shader_id = glCreateShader(shader_type)
            glShaderSource(shader_id, shader_src)
            glCompileShader(shader_id)
            glAttachShader(self.program, shader_id)
        glBindAttribLocation(self.program, 0, 'position')
        glBindAttribLocation(self.program, 1, 'texcoord')
        glLinkProgram(self.program)

    bind = lambda self: glUseProgram(self.program)
    uniform = lambda self, name: glGetUniformLocation(self.program, name)
    uniform1f = lambda self, name, v0: glUniform1f(self.uniform(name), v0)
    uniform2f = lambda self, name, v0, v1: glUniform2f(self.uniform(name), v0, v1)
    uniform4f = lambda self, name, v0, v1, v2, v3: glUniform4f(self.uniform(name), v0, v1, v2, v3)
    __del__ = lambda self: glDeleteProgram(self.program)

    def enable_arrays(self, texture, position, texcoord):
        self.bind()
        texture.bind()
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, array.array('f', position).tostring())
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, array.array('f', texcoord).tostring())
