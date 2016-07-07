from engine.scene import Intermission

class IntermissionFromFile(Intermission):
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
        for line in self.app.resman.intermissions[self.__class__.__name__]:
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

            print 'Got line:', repr(line)


class Start(IntermissionFromFile):
    pass

class Intro(IntermissionFromFile):
    pass

class LostLife(IntermissionFromFile):
    pass

class GameOver(IntermissionFromFile):
    pass

class NextLevelGroup_1_3(IntermissionFromFile):
    pass

class NextLevelGroup_2_3(IntermissionFromFile):
    pass

class NextLevelGroup_3_1(IntermissionFromFile):
    pass

class NextLevelGroup_4_1(IntermissionFromFile):
    pass

class NextLevelGroup_5_1(IntermissionFromFile):
    pass

class Victory(IntermissionFromFile):
    pass

class Outro(IntermissionFromFile):
    pass
