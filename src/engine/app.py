import pygame
import os

from resman import ResourceManager
from audman import AudioManager
from logic.player import Player
from screen import Screen


class App(object):
    def __init__(self, title, width, height, fullscreen,
                 scenes, entry, level_nr=0, debug=False):

        self.debug = debug

        self._clock = pygame.time.Clock()
        self.fps = 30

        self.screen = Screen(self, title, width, height, fullscreen)

        self.resman = ResourceManager(self)
        self.audman = AudioManager(self)

        self.player = Player(self)

        self.level_nr = level_nr
        self.last_level = len(self.resman._levels) - 1

        self._scenes = []
        for scene in scenes:
            s = scene(self)
            self._scenes.append(s)
        self.scene = self._get_scene(entry)

    def _get_scene(self, s):
        for astate in self._scenes:
            if astate.__class__.__name__ == s:
                return astate

    def get_filename(self, basename):
        return os.path.join(os.path.dirname(__file__), '..', '..', 'data', basename)

    def next_level(self):
        return None if self.level_nr == self.last_level else int(self.level_nr) + 1

    def run(self):
        while True:
            self._clock.tick(self.fps)

            events = pygame.event.get()
            for event in events:
                self.scene.process_input(event)

            p = self.scene.process()
            if p:
                next_scene, scene_arg = p
                if next_scene:
                    if next_scene == "GoodBye":
                        break
                    else:
                        # scene wants to change!
                        self.scene = self._get_scene(next_scene)
                        self.scene.resume(scene_arg)

            self.scene.draw()
            self.screen.update()
