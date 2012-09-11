
def make_sequence(frames):
    """
    Make a loopable sequence of frames

    >>> make_sequence(3)
    [0, 1, 2, 1]
    """
    return range(1, frames+1) + range(frames-1, 1, -1)


class Sprite(object):
    def init(self, format_str, frames, duration=.2):
        """
        >>> s = Sprite()
        >>> s.init('whale_a_%d', 3)
        """
        self.duration = duration
        self.sprites = [format_str % x for x in make_sequence(frames)]
        self.frames_per_sprite = int(duration * self.app.fps)
        self.current_sprite = 0
        self.current_frame = 0

    def process(self):
        """Gets called every frame.
        Updats current sprite image"""
        self.current_frame += 1
        if self.current_frame == self.frames_per_sprite:
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.current_frame = 0

    def current_sprite_name(self):
        return self.sprites[self.current_sprite]

    def lookup_sprite(self, name):
        return self.app.resman.get_sprite(name)

