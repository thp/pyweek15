from engine.scene import Scene
from pygame.locals import *


class CutScene(Scene):

    def process_input(self, event):
        if event.type == QUIT:
            self._advance()
        elif event.type == KEYDOWN:
            self._advance()

    def resume(self, args):
        super(CutScene, self).resume(self)
        self.score = args['score'] if args and 'score' in args.keys() else None
        self.health = args['health'] if args and 'health' in args.keys() else None

    def _advance(self):
        # TODO:
        # show the next text (loop through texts)
        # when all text have been shown
        next_level = self.app.next_level()
        if next_level != None:
            self.app.level_nr = int(self.app.level_nr) + 1
            self.next_state = ("Game", {"next_level": next_level,
             'health': self.health,
             'score': self.score,
             })
        else:
            self.next_state = ("Victory", {"score": self.score})
        #    continue to next Game
        # or if all levels are complete, show Victory

        #self.next_state = ("MainMenu", None)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.app.font.render("CutScene", False, (255, 255, 255)),
            (100, 100))
