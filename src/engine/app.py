import pygame
import os
from resman import ResourceManager
from audman import AudioManager
from screen import Screen


class App(object):
    def __init__(self, title, width, height, fullscreen,
                 scenes, entry, level_nr=0, debug=False,
                 opengl=False):
        pygame.init()

        self.debug = debug

        self._clock = pygame.time.Clock()
        self.fps = 30

        if opengl:
            from renderer_opengl import Renderer
        else:
            from renderer_blit import Renderer

        self.renderer = Renderer(self)
        self.screen = Screen(self, title, width, height, fullscreen)
        self.renderer.setup(self.screen.display.get_size())

        self.resman = ResourceManager(self)
        self.audman = AudioManager(self)

        self.level_nr = level_nr
        self.last_level = len(self.resman._levels) - 1

        self._scenes = []
        for scene in scenes:
            s = scene(self)
            self._scenes.append(s)
        self.scene = self._get_scene(entry)
        self.old_scene = None
        self.scene_transition = 0.

    def _get_scene(self, s):
        for astate in self._scenes:
            if astate.__class__.__name__ == s:
                return astate

    def get_filename(self, basename):
        return self.resman._path(basename)

    def next_level(self):
        return None if self.level_nr == self.last_level else int(self.level_nr) + 1

    def run(self):
        while True:
            self._clock.tick(self.fps)

            fading_out = self.old_scene and self.scene_transition < .5

            if not fading_out:
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
                            self.old_scene = self.scene
                            self.scene_transition = 0.
                            self.scene = self._get_scene(next_scene)
                            self.scene.resume(scene_arg)

            self.renderer.begin()

            if self.scene_transition >= .95:
                # Scene transition is done
                self.old_scene = None
            else:
                # Push forward the transition
                self.scene_transition += .1

            if self.old_scene:
                # Transition is in progress
                if self.scene_transition < .5:
                    # Fading out of old scene part
                    brightness = 1. - self.scene_transition * 2
                    self.renderer.global_tint = (brightness,)*3
                    self.old_scene.draw()
                else:
                    # Fading in of new scene part
                    brightness = (self.scene_transition-.5) * 2
                    self.renderer.global_tint = (brightness,)*3
                    self.scene.draw()
            else:
                # No transition is in progress - just draw scene
                self.scene.draw()

            self.renderer.global_tint = 1., 1., 1.
            if self.debug:
                self.screen.draw_debug()

            self.renderer.finish()

