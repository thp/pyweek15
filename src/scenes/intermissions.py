from engine.scene import Intermission


class Start(Intermission):
    def _setup(self):
        self.next_scene = ("Intro", None)

        self.background = self.app.resman.get_background("i_normal")[0]

        self.title = "ONE WHALE TRIP"
        self.story = ["a love story"]
        self.creatures = [self.app.resman.get_creature("whale_story")]


class Intro(Intermission):
    def _setup(self):
        self.next_scene = ("Game", None)

        self.background = self.app.resman.get_background("i_normal")[0]

        self.title = "A LOVE STORY"
        self.story = [
            [self.app.resman.get_creature("whale_story")],
            "hi there! what a nice whale you are!",

            [self.app.resman.get_creature("submarine")],
            "the moment you saw that lovely creature...",
            "... you knew it was love on first sight",

            [self.app.resman.get_creature("whale_story_heart")],
            "at first your advances were met with...",
            "cold disinterest...",
            "cold disinterest... and distance",
            "a whole ocean of distance, in fact",
            "but that made your resolve only stronger",
            "across the ocean you would follow!",

            [self.app.resman.get_creature("oyster_1_pearl")],
            "maybe a string of pearls would open doors?",

            [self.app.resman.get_creature("fishy_rainbow")],
            "the journey is long and hard",
            "food will sustain you",

            [self.app.resman.get_creature("diver")],
            "watch out!",
            "there are many dangers to be avoided",
        ]


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
