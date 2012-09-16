from engine.scene import Scene
from pygame.locals import *


class GameOver(Scene):

    def process_input(self, event):
        if event.type == QUIT:
            self.next_state = ("Start", None)
        elif event.type == KEYDOWN:
            if event.key in [K_ESCAPE, K_RETURN, K_SPACE]:
                self.next_state = ("Start", None)

    def draw(self):
        self.app.screen.draw_card("Game Over")
