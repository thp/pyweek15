from engine.scene import Intermission


class Start(Intermission):
    def _setup(self):
        self.next_scene = ("Intro", None)

        self.title = "ONE WHALE TRIP"
        self.story = ["a love story"]

        self.background = self.app.resman.get_background("beach")[0]
        self.creatures = [self.app.resman.get_sprite("whale_2-1")]


class Intro(Intermission):
    def _setup(self):
        super(Intro, self)._setup()

        self.next_scene = ("Game", None)
        self.title = "INTRO"


class GameOver(Intermission):
    def _setup(self):
        super(GameOver, self)._setup()

        self.next_scene = ("Start", None)
        self.title = "GAME OVER"


class Victory(Intermission):
    def _setup(self):
        super(Victory, self)._setup()

        self.next_scene = ("Outro", None)
        self.title = "VICTORY"


class Outro(Intermission):
    def _setup(self):
        super(Outro, self)._setup()

        self.next_scene = ("GoodBye", None)
        self.title = "OUTRO"
