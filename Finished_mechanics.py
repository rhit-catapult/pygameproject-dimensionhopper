import pygame
import sys

# Constants
WIDTH, HEIGHT = 1400, 860
RADIUS = 20
GRAVITY = 0
JUMP_HEIGHT = 20
PLATFORM_WIDTH_RATIO = 0.14  # Platform width as a ratio of screen width
PLATFORM_HEIGHT_RATIO = 0.023  # Platform height as a ratio of screen height
BLOCK_SIZE = HEIGHT // 19  # Each block is a unit on the 25x19 grid

PLATFORM_WIDTH = int(WIDTH * PLATFORM_WIDTH_RATIO)
PLATFORM_HEIGHT = int(HEIGHT * PLATFORM_HEIGHT_RATIO)

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, left_character_file, right_character_file):
        super().__init__()
        self.screen = screen
        self.imageR = pygame.image.load(right_character_file)
        self.imageL = pygame.image.load(left_character_file)
        self.imageR = pygame.transform.scale(self.imageR, (BLOCK_SIZE, BLOCK_SIZE))
        self.imageL = pygame.transform.scale(self.imageL, (BLOCK_SIZE, BLOCK_SIZE))
        self.image = self.imageR
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_x = 0
        self.speed_y = 0
        self.is_jumping = False
        self.jump_counter = 0
        self.is_touching_ground = False
        self.facing_left = False

    def draw(self):
        if self.facing_left:
            self.image = self.imageL
        else:
            self.image = self.imageR
        self.screen.blit(self.image, self.rect.topleft)

    def update_player(self):
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

    def move_left(self):
        self.speed_x = -5
        self.facing_left = True

    def move_right(self):
        self.speed_x = 5
        self.facing_left = False

    def stop(self):
        self.speed_x = 0

    def jump(self):
        if self.jump_counter < 2:
            self.speed_y = -JUMP_HEIGHT
            self.jump_counter += 1

    def reset_position(self):
        self.rect.topleft = ((ord('o') - ord('a')) * BLOCK_SIZE, 8 * BLOCK_SIZE)
        self.speed_x = 0
        self.speed_y = 0
        self.jump_counter = 0

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
    platform1 = Platform(WIDTH / 2, HEIGHT - PLATFORM_HEIGHT - 20)
    platform2 = Platform(WIDTH / 4, HEIGHT / 2)
    platform3 = Platform(WIDTH - WIDTH / 4, HEIGHT / 2)
    platform4 = Platform(WIDTH / 2 - 300, HEIGHT - PLATFORM_HEIGHT - 100)

    initial_x = (ord('o') - ord('a')) * BLOCK_SIZE
    initial_y = 2 * BLOCK_SIZE
    player = Player(screen, initial_x, initial_y, "HeroKidL.png", "HeroKidR.png")

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

        player.update_player()

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