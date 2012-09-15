from engine.scene import Scene
from pygame.locals import *


class Victory(Scene):

    def process_input(self, event):
        if event.type == QUIT:
            self.next_state = ("MainMenu", None)
        elif event.type == KEYDOWN:
            if event.key in [K_ESCAPE, K_RETURN, K_SPACE]:
                self.next_state = ("MainMenu", None)

    def draw(self):
        self.app.screen.draw_card("VICTORY!")
