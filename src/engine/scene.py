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
        if ((event.type == KEYDOWN and event.key == K_ESCAPE)
                or event.type == QUIT):
            self.next_state = ("GoodBye", None)

    def draw(self):
        pass


class Intermission(Scene):
    def __init__(self, app):
        super(Intermission, self).__init__(app)

        self.creatures = None

        # Set to True in _setup to allow skipping of story
        self.skipable = False

        self._setup()
        self.story = iter(self.story)
        self.update()

    def _setup(self):
        """Define the details of this cut scene."""
        self.next_scene = ("Start", None)

        self.background = self.app.resman.get_background("i_normal")[0]

        self.title = "ONE-WAY ALE-WHAY IP-TRAY"
        self.story = [
            [self.app.resman.get_creature("whale_story")],
            "a-way ove-lay ory-stay",
        ]

    def resume(self, arg):
        super(Intermission, self).resume(arg)
        self.__init__(self.app)

    def update(self):
        item = next(self.story)
        if type(item) is str:
            self.line = item
        else:
            self.creatures = item
            self.line = next(self.story)

    def process_input(self, event):
        if self.skipable and event.type == KEYDOWN and event.key == K_s:
            self.next_state = self.next_scene
        elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
            try:
                self.update()
            except StopIteration:
                self.next_state = self.next_scene

        super(Intermission, self).process_input(event)


    def draw(self):
        self.app.screen.draw_card(self.title, self.line,
                                  self.background, self.creatures)
        if self.skipable:
            self.app.screen.draw_skip()

