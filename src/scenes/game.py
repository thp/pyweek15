from ..engine.scene import Scene
import pygame


class Game(Scene):
    def process(self):
        return super(Game, self).process()

    def process_input(self, event):
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            self.next_state = ("GoodBye", None)

    def draw(self, screen):
        pass
