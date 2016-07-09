def make_sequence(frames):
    return range(1, frames+1) + range(frames-1, 1, -1)

class Sprite(object):
    def init(self, basename, frames, duration=.2):
        self.duration = duration

        if frames == 0:
            self.sprites = [basename]
        else:
            self.sprites = ['%s-%d' % (basename, x) for x in make_sequence(frames)]

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

    def _draw(self, sprite_name, points, max_scale, opacity, tint, align_bottom):
        sprite = self.app.resman.get_sprite(sprite_name)
        w, h = sprite.get_size()
        left = min(point[0] for point in points)
        right = max(point[0] for point in points)
        bottom = max(point[1] for point in points)
        factor = min(max_scale, float(right-left) / float(w))

        x = (right+left)/2 - (w*factor)/2
        if align_bottom:
            y = bottom - h*factor
        else:
            center = tuple(float(x) / len(points) for x in map(sum, zip(*points)))
            y = center[1] - h / 2

        self.app.renderer.draw(sprite, (x, y), factor, opacity, tint)
