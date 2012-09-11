from engine.scene import Scene
from pygame.locals import *


class MainMenu(Scene):

    def process_input(self, event):
        if event.type == QUIT:
            self.next_state = ("GoodBye", None)
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.next_state = ("GoodBye", None)
