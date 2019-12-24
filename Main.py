import pygame

pygame.init()
SIZE = [600, 400]
screen = pygame.display.set_mode(SIZE)
BLACK = pygame.Color('black')


screen.fill(BLACK)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    pygame.display.flip()

