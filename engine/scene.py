from core import random

class Scene(object):
    def __init__(self, app, name):
        self.app = app
        self.name = name

class Particle(object):
    def __init__(self, sprite, x, y, sx, sy):
        self.spawn = (x + random.randint(-sx, sx), y + random.randint(-sy, sy))
        self.x, self.y = self.spawn
        self.dy = -random.uniform(0.5, 3.0)
        self.sprite = sprite
        self.opacity = 1.0

    def step(self):
        self.y += self.dy
        self.x += random.randint(-2, +2) / 10.0
        self.opacity *= 0.97
        if self.y < -self.sprite.h:
            self.x, self.y = self.spawn
            self.opacity = 1.0

class Intermission(Scene):
    def __init__(self, app, name, filedata):
        super(Intermission, self).__init__(app, name)
        self.filedata = filter(None, filedata)
        self.resume()

    def resume(self):
        self.creatures = []
        self.particles = []
        self.skipable = False
        self._setup()
        self.update()

    def process(self):
        for particle in self.particles:
            particle.step()

    def update(self):
        while self.story:
            line = self.story.pop(0)
            if line.startswith('(') and line.endswith(')'):
                key, value = line[1:-1].split('=', 1)
                if key == 'creatures':
                    self.creatures = [self.app.resman.creatures[c] for c in value.split()]
                elif key == 'particles':
                    values = value.split(':')
                    sprite = values.pop(0)
                    count = int(values.pop(-1))
                    self.particles.extend(Particle(self.app.resman.creatures[sprite],
                                                   *map(int, values)) for i in range(count))
            else:
                self.line = line
                break

    def process_input(self, pressed, key):
        if pressed and ((self.skipable and key == 's') or not self.story):
            self.app.go_to_scene(self.next_scene)
        elif pressed:
            self.update()

    def draw(self):
        self.app.screen.draw_card(self.title, self.line, self.background, self.creatures, self.skipable)
        self.app.renderer.postprocess()
        for particle in self.particles:
            self.app.renderer.draw(particle.sprite, (particle.x, particle.y), particle.opacity, particle.opacity)

    def _setup(self):
        is_header = True
        fmt_args = {'player_lives': int(self.app.player.health/3)}

        self.story = []
        for line in self.filedata:
            if is_header and line == '---':
                is_header = False
            elif is_header:
                key, value = line.split('=', 1)
                if key == 'next_scene':
                    self.next_scene = value
                elif key == 'background':
                    self.background = self.app.resman.backgrounds[value][0]
                elif key == 'skipable':
                    self.skipable = (value == 'true')
                elif key == 'title':
                    self.title = value
            else:
                self.story.append(line.format(**fmt_args))
