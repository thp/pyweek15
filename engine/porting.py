import os
import glob

from core import sin, cos, sqrt, time_seconds, randint, randuniform, load_image, render_text, Window, Sound
from core import draw_init, draw_clear, draw_quad, Texture, Framebuffer, ShaderProgram

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
