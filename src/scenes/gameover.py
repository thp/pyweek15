from engine.scene import Scene
from pygame.locals import *


class GameOver(Scene):

    def process_input(self, event):
        if event.type == QUIT:
            self.next_state = ("MainMenu", None)
        elif event.type == KEYDOWN:
            if event.key in [K_ESCAPE, K_RETURN, K_SPACE]:
                self.next_state = ("MainMenu", None)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.app.font.render("Game Over", False, (255, 255, 255)),
            (100, 100))
