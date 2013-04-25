
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

        self.skipable = True
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
            "maybe a string of pearls would help?",

            [self.app.resman.get_creature("fishy_rainbow")],
            "the journey is long and hard",
            "food will sustain you",

            [self.app.resman.get_creature("diver")],
            "watch out!",
            "there are many dangers to be avoided",
        ]


class LostLife(Intermission):
    def _setup(self):
        self.next_scene = ("Game", None)

        self.background = self.app.resman.get_background("i_deepsea")[0]

        lives = int(self.app.player.health/3)

        self.title = "YOU LOST A LIFE"
        self.story = ["be careful! you have only %i left" % lives]
        self.creatures = [self.app.resman.get_creature("lost_life_whale")]


class GameOver(Intermission):
    def _setup(self):
        self.next_scene = ("Start", None)

        self.background = self.app.resman.get_background("i_deepsea")[0]

        self.title = "GAME OVER"
        self.story = ["it wasn't meant to be"]
        self.creatures = [self.app.resman.get_creature("game_over_whale")]


class NextLevelGroup_1_3(Intermission):
    def _setup(self):
        self.next_scene = ("Game", None)

        self.background = self.app.resman.get_background("i_beach")[0]

        self.title = "THE BEACH"
        self.story = iter(["the first hurdle is cleared...",
                           "...but beware of those hairless apes",
                           "ruining everything with their trash"])

        self.creatures = [self.app.resman.get_creature("jellyfish_a"),
                          self.app.resman.get_creature("jellyfish_b")]


class NextLevelGroup_2_3(Intermission):
    def _setup(self):
        self.next_scene = ("Game", None)

        self.background = self.app.resman.get_background("i_coralreef")[0]

        self.title = "THE CORAL REEF"
        self.story = iter(["everything is so colorful down here",
                           "you wish you could share it with someone"])

        self.creatures = [self.app.resman.get_creature("diver")]


class NextLevelGroup_3_1(Intermission):
    def _setup(self):
        self.next_scene = ("Game", None)

        self.background = self.app.resman.get_background("i_deepsea")[0]

        self.title = "THE DEEP SEA"
        self.story = iter(["it's getting dark and lonely",
                           "you wish you had someone to hold"])

        self.creatures = [self.app.resman.get_creature("lanternfish")]


class NextLevelGroup_4_1(Intermission):
    def _setup(self):
        self.next_scene = ("Game", None)

        self.background = self.app.resman.get_background("i_cliff")[0]

        self.title = "THE CLIFFS"
        self.story = iter(["closer, ever closer...",
                           "you can feel your destination approaching"])

        self.creatures = [self.app.resman.get_creature("rock_l")]


class NextLevelGroup_5_1(Intermission):
    def _setup(self):
        self.next_scene = ("Game", None)

        self.background = self.app.resman.get_background("i_surreal")[0]

        self.title = "WHAT A TRIP!"
        self.story = iter(["almost there"])

        self.creatures = [self.app.resman.get_creature("submarine")]


class Victory(Intermission):
    def _setup(self):
        self.next_scene = ("Outro", None)

        self.background = self.app.resman.get_background("i_surreal")[0]

        self.title = "VICTORY"
        self.story = ["a happy ending"]
        self.creatures = [
            self.app.resman.get_creature("whale_story_heart_mirror"),
            self.app.resman.get_creature("victory_submarine"),
         ]


class Outro(Intermission):
    def _setup(self):
        self.next_scene = ("GoodBye", None)

        self.background = self.app.resman.get_background("i_outro")[0]
        self.title = "GOOD BYE!"
        self.story = ["the team:",
                      "gfx: lobbbe",
                      "code: thp, styts, hop",
                      "sfx: styts, thp",]
