from engine.scene import Scene
from pygame.locals import *


class Outro(Scene):

    def process_input(self, event):
        self.next_state = ("GoodBye", None)  # skip me
        if event.type == KEYDOWN:
            self.next_state = ("GoodBye", None)

    def draw(self):
        self.app.screen.draw_card("Outro")
