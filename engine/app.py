import time

import pygame
from pygame.locals import KEYDOWN, KEYUP, QUIT, K_ESCAPE, K_SPACE, K_s, K_LEFT, K_RIGHT, K_UP

from resman import ResourceManager
from sprite import Player
from screen import Screen
from scene import Intermission
from renderer import Renderer
from game import Game

class TimeAccumulator:
    def __init__(self, fps):
        self.step = 1. / float(fps)
        self.accumulated = 0
        self.last_time = time.time()

    def update(self, callback):
        now = time.time()
        self.accumulated += (now - self.last_time)
        self.last_time = now
        while self.accumulated > self.step:
            self.accumulated -= self.step
            callback()

class App(object):
    KEYMAP = {K_SPACE: ' ', K_s: 's', K_LEFT: 'left', K_RIGHT: 'right', K_UP: 'up'}

    def __init__(self, title, width, height, fullscreen, entry):
        pygame.init()
        self.display = pygame.display.set_mode((0, 0) if fullscreen else (width, height), pygame.OPENGL |
                                               pygame.DOUBLEBUF | (pygame.FULLSCREEN if fullscreen else 0))
        pygame.display.set_caption(title)
        dpy_width, dpy_height = self.display.get_size()

        self.running = True
        self.fps = 30
        self.accumulator = TimeAccumulator(self.fps)
        self.renderer = Renderer(self)
        self.screen = Screen(self, width, height, dpy_width, dpy_height)
        self.resman = ResourceManager(self)
        self.player = Player(self)

        self.renderer.setup(dpy_width, dpy_height)

        self._scenes = {'Game': Game(self)}
        for name in self.resman.intermissions.keys():
            self._scenes[name] = Intermission(self, name)
        self._scenes['Game'].reset(hard=True)
        self.go_to_scene(entry)

    def go_to_scene(self, name):
        if name == "GoodBye":
            self.running = False
        else:
            self.scene_transition = 0.
            self.scene = self._scenes[name]
            self.scene.resume()

    def run(self):
        while self.running:
            self.scene_transition += .05
            if self.scene_transition >= .95:
                self.scene_transition = 1.0
                events = pygame.event.get()
                for event in events:
                    if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
                        self.running = False
                    elif event.type in (KEYDOWN, KEYUP):
                        self.scene.process_input((event.type == KEYDOWN), self.KEYMAP.get(event.key, None))
                self.accumulator.update(self.scene.process)

            self.renderer.begin()
            self.renderer.global_tint = (self.scene_transition,)*3
            self.scene.draw()
            self.renderer.finish()
            pygame.display.flip()
