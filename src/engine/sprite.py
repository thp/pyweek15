def make_sequence(frames):
    """
    >>> make_sequence(3)
    [1, 2, 3, 2]
    """
    return range(1, frames+1) + range(frames-1, 1, -1)

class Sprite(object):
    def init(self, format_str, frames, duration=.2):
        self.duration = duration
        if self.app.resman.get_sprite(format_str) is not None:
            self.sprites = [format_str]
        else:
            self.sprites = [format_str % x for x in make_sequence(frames)]
        self.frames_per_sprite = int(duration * self.app.fps)
        self.current_sprite = 0
        self.current_frame = 0

    def process(self):
        self.current_frame += 1
        if self.current_frame == self.frames_per_sprite:
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.current_frame = 0

    def current_sprite_name(self):
        return self.sprites[self.current_sprite]

    def lookup_sprite(self, name):
        return self.app.resman.get_sprite(name)
