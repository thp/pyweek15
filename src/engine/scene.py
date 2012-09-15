from pygame.locals import *


class Scene(object):
    def __init__(self, app):
        self.app = app
        self.next_state = None  # holds None or a string with classname of the place to go

    def process(self):
        return self.next_state

    def resume(self, arg):
        """Called form App when being switched to"""
        self.next_state = None

    def process_input(self, event):
        pass

    def draw(self):
        pass


class Intermission(Scene):
    def __init__(self, app):
        super(Intermission, self).__init__(app)

        self._setup()
        self.story = iter(self.story)
        self.line = next(self.story)

    def _setup(self):
        """Define the details of this cut scene."""
        self.next_scene = ("Start", None)

        self.title = "ONE-WAY ALE-WHAY IP-TRAY"
        self.story = ["a-way ove-lay ory-stay"]

        self.background = self.app.resman.get_background("beach")[0]
        self.creatures = [self.app.resman.get_sprite("whale_2-1")]


    def process_input(self, event):
        if event.type == KEYDOWN:
            try:
                self.line = next(self.story)
            except StopIteration:
                self.next_state = self.next_scene


    def draw(self):
        self.app.screen.draw_card(self.title, self.line,
                                  self.background, self.creatures)
