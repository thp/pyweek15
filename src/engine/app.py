import pygame


class App(object):
    def __init__(self, title="PyWeek 15", resolution=(1024, 768)):
        pygame.display.set_mode(resolution)
        self.screen = pygame.display.get_surface()
        pygame.display.set_caption(title)

        self.clock = pygame.time.Clock()

    def run(self):
        running = True

        while running:
            self.clock.tick(30)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    running = False

            pygame.display.flip()

        pygame.quit()
