from engine.scene import Scene
from pygame.locals import *


class Outro(Scene):

    def process_input(self, event):
        self.next_state = ("GoodBye", None)  # skip me
        if event.type == KEYDOWN:
            self.next_state = ("GoodBye", None)

    def draw(self, screen):
        return # skip me
        screen.fill((0, 0, 0))
        screen.blit(self.app.font.render("Outro", False, (255, 255, 255)),
            (100, 100))
