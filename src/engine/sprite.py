class Sprite(object):
    def init(self, sprite_dict):
        """
        Convers seconds from sprite_dict to frames.
        e.g. {"player1": .2, "player2": .3}

        sprite_dict[key] => value:
            key ... name of image
            value ... seconds to hold frame"""
        self.frame_dict = {}
        for name in sprite_dict.keys():
            seconds = sprite_dict[name]
            frames = int(seconds * self.app.fps)
            self.frame_dict[name] = frames

        self.current_frame = 0
        self.n_frames = self.frame_dict.keys().__len__()
        self.frames_left = self.frame_dict[self.frame_dict.keys()[0]]

    def process(self):
        """Gets called every frame.
        Updats current sprite image"""
        if self.frames_left > 0:
            self.frames_left -= 1
        else:
            if self.current_frame < self.n_frames - 1:
                self.current_frame += 1
            else:
                self.current_frame = 0
            self.frames_left = self.frame_dict.values()[self.current_frame]

    def _current_sprite(self):
        name = self.frame_dict.keys()[self.current_frame]
        return self.app.resman.get_sprite(name)
