from engine.scene import Scene
from pygame.locals import *


class Outro(Scene):

    def process_input(self, event):
        if event.type == KEYDOWN:
            self.next_state = ("GoodBye", None)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.app.font.render("Outro", False, (255, 255, 255)),
            (100, 100))
