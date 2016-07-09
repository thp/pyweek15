from pygame.locals import KEYDOWN, MOUSEBUTTONDOWN, K_s


class Scene(object):
    def __init__(self, app, name):
        self.app = app
        self.name = name

    def process(self):
        pass

    def resume(self):
        pass

    def process_input(self, event):
        pass

    def draw(self):
        pass


class Intermission(Scene):
    def __init__(self, app, name):
        super(Intermission, self).__init__(app, name)
        self.resume()

    def resume(self):
        super(Intermission, self).resume()

        self.creatures = None

        # Set to True in _setup to allow skipping of story
        self.skipable = False

        self._setup()
        self.story = iter(self.story)
        self.update()

    def update(self):
        item = next(self.story)
        if type(item) is str:
            self.line = item
        else:
            self.creatures = item
            self.line = next(self.story)

    def process_input(self, event):
        if self.skipable and event.type == KEYDOWN and event.key == K_s:
            self.app.go_to_scene(self.next_scene)
        elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
            try:
                self.update()
            except StopIteration:
                self.app.go_to_scene(self.next_scene)

    def draw(self):
        self.app.screen.draw_card(self.title, self.line,
                                  self.background, self.creatures)
        if self.skipable:
            self.app.screen.draw_skip()

    def _parse_key_value(self, line):
        key, value = line.split(':', 1)
        value = value.strip()
        return key, value

    def _setup(self):
        is_header = True

        fmt_args = {
            'player_lives': int(self.app.player.health/3),
        }

        self.story = []
        for line in self.app.resman.intermissions[self.name]:
            if not line:
                continue

            if is_header and line == '---':
                is_header = False
                continue

            if is_header:
                key, value = self._parse_key_value(line)
                if key == 'next_scene':
                    self.next_scene = value
                elif key == 'background':
                    self.background = self.app.resman.get_background(value)[0]
                elif key == 'skipable':
                    self.skipable = (value == 'true')
                elif key == 'title':
                    self.title = value
                else:
                    raise ValueError(line)
            else:
                if line.startswith('(') and line.endswith(')'):
                    # Story meta definition
                    key, value = self._parse_key_value(line[1:-1])
                    if key == 'creatures':
                        self.story.append([self.app.resman.get_creature(c) for c in value.split()])
                    else:
                        raise ValueError(line)
                else:
                    # Story text
                    self.story.append(line.format(**fmt_args))

