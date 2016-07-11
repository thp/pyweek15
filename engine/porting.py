from core import sin, cos, sqrt, time_seconds, randint, randuniform, load_image, Window, Sound, Font, list_files
from core import draw_init, Texture, Framebuffer, ShaderProgram

def get_lines(filename):
    return open(filename).read().splitlines()

def file_path(*args):
    return '/'.join(('/'.join(__file__.split('/')[:-1]), '..', 'data') + args)

def find_files(parent, extension):
    return list_files(file_path(parent), extension)
