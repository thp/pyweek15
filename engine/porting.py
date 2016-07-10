from core import sin, cos, sqrt, time_seconds, randint, randuniform, load_image, render_text, Window, Sound, list_files
from core import draw_init, draw_clear, draw_quad, Texture, Framebuffer, ShaderProgram

def get_lines(filename):
    return open(filename).read().splitlines()

def file_path(*args):
    return '/'.join(('/'.join(__file__.split('/')[:-1]), '..', 'data') + args)

def find_files(parent, extension):
    return list_files(file_path(parent), extension)

class Font():
    def __init__(self, size):
        self.size = size

    def render(self, text):
        result = render_text(text)
        result.w *= self.size
        result.h *= self.size
        return result
