from engine.scene import Intermission


class Start(Intermission):
    def _setup(self):
        self.next_scene = ("Intro", None)

        self.title = "ONE WHALE TRIP"
        self.story = ["a love story", "in umpteen parts"]

        self.background = self.app.resman.get_background("beach")[0]
        self.creatures = [self.app.resman.get_sprite("whale_2-1")]
