import pygame
import sys


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

def main():
    pygame.init()
    screen = pygame.display.set_mode((1400, 860))


    block = Block(screen, 100, 100, 50, 50, (0, 255, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((255, 255, 255))

        block.draw()

        pygame.display.update()

main()