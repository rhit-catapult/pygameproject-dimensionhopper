import pygame
import sys
import random
import time


backgrounds = [
]

current_background_index = 0


def change_background():
    global current_background_index
    current_background_index = (current_background_index + 1) % len(backgrounds)


def main():
    # turn on pygame
    pygame.init()

    # create a screen
    pygame.display.set_caption("Dimension Hopper")
    # TODO: Change the size of the screen as you see fit!
    screen = pygame.display.set_mode((640, 480))

    # let's set the framerate
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # TODO: Add you events code
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:  # Change the background when 'C' is pressed
                    change_background()

        # TODO: Fill the screen with whatever background color you like!
        screen.fill((255, 255, 255))

        # TODO: Add your project code

        # don't forget the update, otherwise nothing will show up!
        pygame.display.update()


main()
