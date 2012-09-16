from engine.scene import Intermission


class Start(Intermission):
    def _setup(self):
        self.next_scene = ("IntroWhale", None)

        self.title = "ONE WHALE TRIP"
        self.story = ["a love story"]

        self.background = self.app.resman.get_background("i_normal")[0]
        self.creatures = [self.app.resman.get_creature("whale_story")]


class IntroWhale(Intermission):
    def _setup(self):
        self.next_scene = ("IntroSub", None)

        self.title = "A LOVE STORY"
        self.story = ["hi there! what a nice whale you are!"]

        self.background = self.app.resman.get_background("i_normal")[0]
        self.creatures = [self.app.resman.get_creature("whale_story")]


class IntroSub(Intermission):
    def _setup(self):
        self.next_scene = ("IntroStory", None)

        self.title = "A LOVE STORY"
        self.story = ["the moment you saw that lovely creature...",
                      "... you knew it was love on first sight"]

        self.background = self.app.resman.get_background("i_normal")[0]
        self.creatures = [self.app.resman.get_creature("submarine")]


class IntroStory(Intermission):
    def _setup(self):
        self.next_scene = ("IntroPearls", None)

        self.title = "A LOVE STORY"
        self.story = ["at first your advances were met with...",
                      "cold disinterest...",
                      "cold disinterest... and distance",
                      "a whole ocean of distance, in fact",
                      "but that made your resolve only stronger",
                      "across the ocean you would follow!"]

        self.background = self.app.resman.get_background("i_normal")[0]
        self.creatures = [self.app.resman.get_creature("whale_story_heart")]


class IntroPearls(Intermission):
    def _setup(self):
        self.next_scene = ("IntroFishy", None)

        self.title = "A LOVE STORY"
        self.story = ["maybe a string of pearls would open doors?"]

        self.background = self.app.resman.get_background("i_normal")[0]
        self.creatures = [self.app.resman.get_creature("oyster_1_pearl")]


class IntroFishy(Intermission):
    def _setup(self):
        self.next_scene = ("IntroEnemies", None)

        self.title = "A LOVE STORY"
        self.story = ["the journey is long and hard",
                      "food will sustain you"]

        self.background = self.app.resman.get_background("i_normal")[0]
        self.creatures = [self.app.resman.get_creature("fishy_rainbow")]


class IntroEnemies(Intermission):
    def _setup(self):
        self.next_scene = ("Game", None)

        self.title = "A LOVE STORY"
        self.story = ["watch out!",
                      "there are many dangers to be avoided"]

        self.background = self.app.resman.get_background("i_normal")[0]
        self.creatures = [self.app.resman.get_creature("diver")]


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
