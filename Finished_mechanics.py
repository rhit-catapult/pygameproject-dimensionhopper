import pygame
import sys

# Constants
WIDTH, HEIGHT = 1400, 860
RADIUS = 20
GRAVITY = .9
JUMP_HEIGHT = 20
PLATFORM_WIDTH = 200
PLATFORM_HEIGHT = 20

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('HeroKidR.png')
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.is_jumping = False
        self.is_touching_ground = False
        self.moving_left = False
        self.moving_right = False
        self.speed_x = 0
        self.speed_y = 0
        self.jump_counter = 0
        self.dash_timer = 0

    def update(self):
        self.speed_y += GRAVITY
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed_y = 0
            self.is_touching_ground = True
            self.jump_counter = 0
        if self.dash_timer > 0:
            self.dash_timer -= 1
            if self.dash_timer == 0:
                self.stop()

    def move_left(self):
        self.speed_x = -5
        self.image = pygame.image.load('HeroKidL.png')

    def move_right(self):
        self.speed_x = 5
        self.image = pygame.image.load('HeroKidR.png')

    def dash(self):
        if self.jump_counter < 2:
            if self.moving_left:
                self.speed_x = -40
            elif self.moving_right:
                self.speed_x = 40
            self.dash_timer = 10

    def stop(self):
        self.speed_x = 0

    def jump(self):
        if self.jump_counter < 2:
            self.speed_y = -JUMP_HEIGHT
            self.jump_counter += 1


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    player = Player()
    platform1 = Platform(WIDTH / 2, HEIGHT - PLATFORM_HEIGHT - 20)
    platform2 = Platform(WIDTH / 4, HEIGHT / 2)
    platform3 = Platform(WIDTH - WIDTH / 4, HEIGHT / 2)
    platform4 = Platform(WIDTH / 2 - 300, HEIGHT - PLATFORM_HEIGHT - 100)

    all_sprites = pygame.sprite.Group(player, platform1, platform2, platform3, platform4)
    platforms = pygame.sprite.Group(platform1, platform2, platform3, platform4)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_a:
                    player.move_left()
                    player.moving_left = True
                if event.key == pygame.K_d:
                    player.move_right()
                    player.moving_right = True
                if event.key == pygame.K_w:
                    player.jump()
                if event.key == pygame.K_LSHIFT:
                    player.stop()
                    player.dash()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player.stop()
                    player.moving_left = False
                    player.moving_right = False

        player.update()

        for platform in platforms:
            if player.rect.colliderect(platform.rect):
                if player.speed_y > 0:
                    player.rect.bottom = platform.rect.top
                    player.speed_y = 0
                    player.is_touching_ground = True
                    player.jump_counter = 0
                elif player.speed_y < 0:
                    player.rect.top = platform.rect.bottom
                    player.speed_y = 0

        screen.fill(WHITE)
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(120)


if __name__ == "__main__":
    main()