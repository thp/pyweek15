import pygame


class App(object):
    def __init__(self, title, resolution, scenes):
        pygame.display.set_mode(resolution)
        self.screen = pygame.display.get_surface()
        pygame.display.set_caption(title)

        self._clock = pygame.time.Clock()

        self._scenes = []
        for asc in scenes:
            s = asc(self)
            self._scenes.append(s)
        self.scene = self._scenes[0]

    def _get_scene(self, s):
        for astate in self._scenes:
            if astate.__class__.__name__ == s:
                return astate

    def run(self):
        running = True

        while running:
            self._clock.tick(30)

            p = self.scene.process()
            if p:
                next_scene, scene_arg = p
                if next_scene:
                    if next_scene == "GoodBye":
                        running = False
                    else:
                        # scene wants to change!
                        self.scene = self._get_scene(next_scene)
                        self.scene.resume(scene_arg)

            events = pygame.event.get()
            for event in events:
                self.scene.process_input(event)

            self.scene.draw(self.screen)

            pygame.display.flip()

        pygame.quit()
