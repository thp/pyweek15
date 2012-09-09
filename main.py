import pygame

pygame.display.set_mode((1024, 768))
screen = pygame.display.get_surface()

clock = pygame.time.Clock()

running = True

while running:
    clock.tick(30)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            running = False

    pygame.display.flip()

pygame.quit()
