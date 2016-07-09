import pygame
import os
import time

from resman import ResourceManager, AudioManager
from sprite import Player
from screen import Screen
from scene import Intermission
from renderer import Renderer
from game import Game

class TimeAccumulator:
    def __init__(self, fps):
        self.fps = fps
        self.step = 1. / float(self.fps)
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
    def __init__(self, title, width, height, fullscreen, entry, level_nr="1-1"):
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

        group, number = level_nr.split('-')
        group, number = int(group), int(number)
        self.start_level = (group, number)

        self._scenes = {'Game': Game(self)}
        for name in self.resman.intermissions.keys():
            self._scenes[name] = Intermission(self, name)

        self.scene = self._scenes[entry]
        self.old_scene = None
        self.scene_transition = 0.

    def go_to_scene(self, name):
        if name == "GoodBye":
            self.running = False
            return

        # scene wants to change!
        self.old_scene = self.scene
        self.scene_transition = 0.
        # XXX: Tell the renderer to snapshot old_scene for transition
        self.scene = self._scenes[name]
        self.scene.resume()

    def run(self):
        while self.running:
            self._clock.tick(self.fps)

            fading_out = self.old_scene and self.scene_transition < .5

            if not fading_out:
                events = pygame.event.get()
                for event in events:
                    self.scene.process_input(event)
                    self.screen.process_input(event)

                self.accumulator.update(self.scene.process)

            self.renderer.begin()

            if self.scene_transition >= .95:
                # Scene transition is done
                self.old_scene = None
            else:
                # Push forward the transition
                self.scene_transition += .05

            if self.old_scene:
                # Fading in of new scene part
                brightness = self.scene_transition
                # XXX: Tell renderer to fade between old_scene and self.scene
                self.renderer.global_tint = (brightness,)*3
                self.scene.draw()
            else:
                # No transition is in progress - just draw scene
                self.scene.draw()

            self.renderer.global_tint = 1., 1., 1.
            self.renderer.finish()
