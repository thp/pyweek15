from core import time, Window
from .resman import ResourceManager
from .sprite import Player
from .screen import Screen
from .scene import Intermission
from .renderer import Renderer
from .game import Game

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

    def __init__(self, title, width, height, entry):
        self.window = Window(width, height, title)

        self.running = True
        self.accumulator = TimeAccumulator(30)
        self.renderer = Renderer(self)
        self.screen = Screen(self, width, height)
        self.resman = ResourceManager(self)
        self.player = Player(self)
        self.renderer.resize(width, height)

        self._scenes = {'Game': Game(self)}
        for name, filedata in self.resman.intermissions.items():
            self._scenes[name] = Intermission(self, name, filedata)
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
                event, args = self.window.next_event()
                if event == 0:
                    ...  # No event
                elif event == 1:
                    self.running = False
                elif event == 2:
                    self.screen.touch = False
                    pressed, key = args
                    if pressed and key == 'esc':
                        self.running = False
                    else:
                        self.scene.process_input(pressed, key)
                elif event == 3:
                    event, x, y, finger = args
                    self.scene.process_touch(event, x, y, finger)
                self.accumulator.update(self.scene.process)

            self.renderer.begin()
            self.renderer.global_tint = (self.scene_transition,)*3
            self.scene.draw()
            self.renderer.finish()
            self.window.swap_buffers()
            yield
