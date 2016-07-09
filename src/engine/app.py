import pygame
import time

from resman import ResourceManager, AudioManager
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
    def __init__(self, title, width, height, fullscreen, entry):
        pygame.init()

        self.running = True
        self._clock = pygame.time.Clock()
        self.fps = 30

        self.accumulator = TimeAccumulator(self.fps)

        self.renderer = Renderer(self)
        self.screen = Screen(self, title, width, height, fullscreen)

        self.audman = AudioManager(self)
        self.resman = ResourceManager(self)

        self.renderer.setup(self.screen.display.get_size())

        self.player = Player(self)

        self._scenes = {'Game': Game(self)}
        for name in self.resman.intermissions.keys():
            self._scenes[name] = Intermission(self, name)

        self.scene = self._scenes[entry]
        self.scene_transition = 0.

    def go_to_scene(self, name):
        if name == "GoodBye":
            self.running = False
            return

        self.scene_transition = 0.
        self.scene = self._scenes[name]
        self.scene.resume()

    def run(self):
        while self.running:
            self._clock.tick(self.fps)

            if self.scene_transition == 1.:
                events = pygame.event.get()
                for event in events:
                    self.scene.process_input(event)
                    self.screen.process_input(event)

                self.accumulator.update(self.scene.process)

            self.renderer.begin()

            if self.scene_transition >= .95:
                # Scene transition is done
                self.scene_transition = 1.0
            else:
                # Push forward the transition
                self.scene_transition += .05

            self.renderer.global_tint = (self.scene_transition,)*3

            self.scene.draw()
            self.renderer.finish()
            pygame.display.flip()
