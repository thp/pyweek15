import pygame
import os
from resman import ResourceManager
from audman import AudioManager


class App(object):
    def __init__(self, title, resolution, scenes, entry):
        pygame.init()
        self.screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption(title)

        self._clock = pygame.time.Clock()
        self.fps = 30

        self.resman = ResourceManager(self)
        self.audman = AudioManager(self)

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

    def run(self):
        running = True

        while running:
            self._clock.tick(self.fps)

            p = self.scene.process()
            if p:
                next_scene, scene_arg = p
                if next_scene:
                    if next_scene == "GoodBye":
                        running = False
                    else:
                        # scene wants to change!
                        self.scene = self._get_scene(next_scene)
                        self.scene.resume(scene_arg)

            events = pygame.event.get()
            for event in events:
                self.scene.process_input(event)

            self.scene.draw(self.screen)

            pygame.display.flip()

        pygame.quit()
