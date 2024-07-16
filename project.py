import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 860
BLOCK_SIZE = SCREEN_HEIGHT // 19  # Each block is a unit on the 25x19 grid

# Colors
WHITE = (255, 255, 255)
BLOCK_COLOR = (0, 0, 0)

# Backgrounds list
backgrounds = []

# Current background index
current_background_index = 0

def change_background():
    global current_background_index
    current_background_index = (current_background_index + 1) % len(backgrounds)

class Spike:
    def __init__(self, screen, x, y, image_filename):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_filename)
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))


    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

class Block:
    def __init__(self, screen, x, y, width, height, color):
        self.screen = screen
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

def create_map1(screen):
    blocks = [
        # Outer walls
        *[(col, 'a') for col in range(1, 26)],
        *[(col, 's') for col in range(1, 26)],
        *[(1, row) for row in 'abcdefghijklmnopqrs'],
        *[(25, row) for row in 'abcdefghijklmnopqrs'],
        # Inner blocks
        (2, 'k'), (3, 'k'), (3, 'o'), (3, 'p'), (4, 'm'), (4, 'n'), (4, 'o'), (4, 'p'),
        (5, 'k'), (5, 'l'), (5, 'm'), (5, 'n'), (5, 'o'), (5, 'p'),
        (6, 'k'), (6, 'l'), (6, 'm'), (6, 'n'), (6, 'o'), (7, 'b'), (7, 'c'), (7, 'l'), (7, 'm'), (7, 'n'),
        (8, 'c'), (8, 'm'), (8, 'n'), (9, 'i'), (9, 'l'), (9, 'm'), (9, 'n'), (10, 'i'), (10, 'j'), (10, 'k'),
        (10, 'l'), (10, 'n'), (10, 'o'), (10, 'r'), (11, 'j'), (11, 'o'), (11, 'r'), (12, 'j'), (12, 'm'),
        (12, 'o'), (12, 'p'), (12, 'q'), (12, 'r'), (13, 'h'), (13, 'i'), (13, 'j'), (13, 'm'), (13, 'o'),
        (14, 'f'), (14, 'g'), (14, 'h'), (14, 'i'), (14, 'j'), (14, 'm'), (14, 'r'), (15, 'h'), (15, 'i'),
        (15, 'j'), (15, 'm'), (15, 'n'), (15, 'o'), (15, 'r'), (16, 'j'), (16, 'o'), (16, 'q'), (16, 'r'),
        (17, 'j'), (17, 'k'), (17, 'o'), (18, 'i'), (18, 'j'), (18, 'k'), (18, 'l'), (18, 'n'), (18, 'o'),
        (19, 'h'), (19, 'i'), (19, 'j'), (19, 'k'), (19, 'l'), (19, 'n'), (19, 'o'), (20, 'h'), (20, 'j'),
        (20, 'l'), (20, 'n'), (20, 'o'), (21, 'j'), (21, 'm'), (21, 'n'), (21, 'o'), (22, 'j'), (22, 'm'),
        (22, 'n'), (22, 'o'), (22, 'p'), (22, 'q'), (23, 'o'), (23, 'q')
    ]

    spikes = [
        (2, 'j'), (2, 'l'), (2, 'm'), (4, 'r'), (5, 'j'), (5, 'r'), (6, 'j'), (7, 'r'),
        (8, 'k'), (8, 'l'), (9, 'h'), (9, 'q'), (9, 'r'), (10, 'h'), (11, 'i'), (12, 'i'),
        (12, 'l'), (13, 'p'), (14, 'k'), (14, 'q'), (15, 'g'), (15, 'k'), (16, 'i'), (16, 'm'),
        (16, 'n'), (17, 'i'), (17, 'n'), (17, 'q'), (17, 'r'), (18, 'h'), (18, 'r'), (19, 'g'),
        (19, 'q'), (19, 'r'), (20, 'g'), (20, 'r'), (21, 'g'), (22, 'g')
    ]

    # Draw blocks
    for col, row in blocks:
        x = (col - 1) * BLOCK_SIZE
        y = (ord(row) - ord('a')) * BLOCK_SIZE
        block = Block(screen, x, y, BLOCK_SIZE, BLOCK_SIZE, BLOCK_COLOR)
        block.draw()

    # Draw spikes
    for col, row in spikes:
        x = (col - 1) * BLOCK_SIZE
        y = (ord(row) - ord('a')) * BLOCK_SIZE
        spike = Spike(screen, x, y, "spike1.png")  # Assuming you have a "spike1.png" image file
        spike.draw()

def create_backgrounds(screen):
    global backgrounds
    background1 = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background1.fill(WHITE)
    create_map1(background1)
    backgrounds.append(background1)

def draw_background(screen):
    screen.blit(backgrounds[current_background_index], (0, 0))

def main():
    # turn on pygame
    pygame.init()

    # create a screen
    pygame.display.set_caption("Dimension Hopper")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create the backgrounds
    create_backgrounds(screen)

    # let's set the framerate
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:  # Change the background when 'C' is pressed
                    change_background()

        # Draw the current background
        draw_background(screen)

        # don't forget the update, otherwise nothing will show up!
        pygame.display.update()
        clock.tick(60)

main()
