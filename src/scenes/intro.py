from engine.scene import Scene
from pygame.locals import *


class Intro(Scene):
    def process_input(self, event):
        if event.type == KEYDOWN:
            self.next_state = ("MainMenu", None)

    def draw(self):
        self.app.screen.draw_card("Intro")
