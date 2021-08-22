import settings
import pygame
from pygame.locals import *

from projects import integrals

slide_index = 1
clock = pygame.time.Clock()
while True:
    clock.tick(100)
    settings.screen.fill((0, 0, 0))
    mouse_state = [
        (pygame.mouse.get_pos()[0] / (settings.CONFIG['screen_width']/2) - 1) * settings.CONFIG['x_max'],
        (1 - pygame.mouse.get_pos()[1] / (settings.CONFIG['screen_height']/2)) * settings.CONFIG['y_max']
    ]

    slides = integrals.Scene(mouse_state)
    slides[0]()
    slides[slide_index]()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if slide_index > 1:
                    slide_index -= 1
            if event.key == pygame.K_RIGHT:
                if slide_index < len(slides) - 1:
                    slide_index += 1

    settings.time += 0.01
    pygame.display.update()