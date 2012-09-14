import pygame
import os
from resman import ResourceManager
from audman import AudioManager


class App(object):
    def __init__(self, screen, scenes, entry, level_nr=0):
        self.screen = screen

        self._clock = pygame.time.Clock()
        self.fps = 30

        self.resman = ResourceManager(self)
        self.audman = AudioManager(self)

        self.resman.load_font("visitor2", 48)
        self.font = self.resman.get_font("visitor2_48")
        self.resman.load_font("visitor2", 20)
        self.font_small = self.resman.get_font("visitor2_20")

        self.level_nr = level_nr
        self.last_level = len(self.resman._levels) + 1

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

            self.scene.draw(self.screen.display)

            # write fps
            fps_surf = self.font_small.render("FPS: %2.2f" % self._clock.get_fps(),
                False, (255, 255, 255), (0, 0, 0))
            self.screen.display.blit(fps_surf, (0, 0))

            self.screen.update()

