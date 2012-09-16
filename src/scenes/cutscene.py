from engine.scene import Scene
from pygame.locals import *


class CutScene(Scene):
    def __init__(self, app):
        super(CutScene, self).__init__(app)
        self.i_subtitle = 0

    def process_input(self, event):
        if event.type == QUIT:
            self._advance()
        elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
            self._advance()

    def process(self):
        return super(CutScene, self).process()

    def resume(self, args):
        super(CutScene, self).resume(self)
        self.score = args['score'] if args and 'score' in args.keys() else None
        self.health = args['health'] if args and 'health' in args.keys() else None
        self.story = args['story'] if args and 'story' in args.keys() else None
        self.restart = args['restart'] if args and 'restart' in args.keys() else False
        self.i_subtitle = 0

    def _advance(self):
        # show the next text (loop through texts)
        if self.i_subtitle < self.story.__len__() - 1:
            self.i_subtitle += 1
        else:
            # when all text have been shown
            #    continue to next Game
            next_level = self.app.next_level()
            if next_level != None or self.restart:
                if not self.restart:
                    self.app.level_nr = int(self.app.level_nr) + 1
                else:
                    next_level = self.app.level_nr
                self.next_state = ("Game", {"next_level": next_level,
                 'health': self.health,
                 'score': self.score,
                 })
            else:
                # or if all levels are complete, show Victory
                self.next_state = ("Victory", {"score": self.score})

    def draw(self):
        if self.i_subtitle < len(self.story):
            story = self.story[self.i_subtitle]
        else:
            story = None

        self.app.screen.draw_card('Cut Scene', story)
