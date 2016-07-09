class Scene(object):
    def __init__(self, app, name):
        self.app = app
        self.name = name

class Intermission(Scene):
    def __init__(self, app, name):
        super(Intermission, self).__init__(app, name)
        self.resume()

    def resume(self):
        self.creatures = None
        self.skipable = False
        self._setup()
        self.update()

    def process(self):
        pass

    def update(self):
        line = self.story.pop(0)
        if line.startswith('(') and line.endswith(')'):
            key, value = line[1:-1].split('=', 1)
            if key == 'creatures':
                self.creatures = [self.app.resman.creatures[c] for c in value.split()]
            self.line = self.story.pop(0)
        else:
            self.line = line

    def process_input(self, pressed, key):
        if pressed and ((self.skipable and key == 's') or not self.story):
            self.app.go_to_scene(self.next_scene)
        elif pressed:
            self.update()

    def draw(self):
        self.app.screen.draw_card(self.title, self.line,
                                  self.background, self.creatures)
        if self.skipable:
            self.app.screen.draw_skip()

    def _setup(self):
        is_header = True
        fmt_args = {'player_lives': int(self.app.player.health/3)}

        self.story = []
        for line in filter(None, self.app.resman.intermissions[self.name]):
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
