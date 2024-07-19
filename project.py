import pygame
import sys

# Constants
WIDTH, HEIGHT = 1120, 860
GRAVITY = 0.2
JUMP_HEIGHT = 9
DASH_VELOCITY = 12  # Dash velocity, similar to horizontal jump speed
DASH_DURATION = 9  # Duration of the dash in frames
BLOCK_SIZE = HEIGHT // 19  # Each block is a unit on the 25x19 grid
PLAYER_SIZE = int(BLOCK_SIZE * 0.7)  # Player size is 0.7 of a block unit
MOVE_SPEED = 4  # Horizontal move speed
dev_mode = False
start_time = 0
record = 0
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLOCK_COLOR = (0, 0, 0)

# Backgrounds list
backgrounds = []

# Current background index
current_background_index = 0

def change_background():
    global current_background_index
    current_background_index = (current_background_index + 1) % len(backgrounds)

def reset_to_map1():
    global current_background_index
    current_background_index = 0

class Player(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, left_character_file, right_character_file):
        super().__init__()
        self.screen = screen
        self.imageR = pygame.image.load(right_character_file)
        self.imageL = pygame.image.load(left_character_file)
        self.imageR = pygame.transform.scale(self.imageR, (PLAYER_SIZE, PLAYER_SIZE))
        self.imageL = pygame.transform.scale(self.imageL, (PLAYER_SIZE, PLAYER_SIZE))
        self.image = self.imageR
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_x = 0
        self.speed_y = 0
        self.is_jumping = False
        self.jump_start_y = 0  # Track the starting Y position of the jump
        self.jump_height_limit = 2 * BLOCK_SIZE  # Maximum jump height
        self.is_touching_ground = False
        self.is_dashing = False
        self.dash_timer = 0
        self.dash_counter = 0  # Dash counter to limit mid-air dashes
        self.facing_left = False

    def draw(self):
        if self.facing_left:
            self.image = self.imageL
        else:
            self.image = self.imageR
        self.screen.blit(self.image, self.rect.topleft)

    def update_player(self, blocks):
        if not self.is_dashing:
            self.speed_y += GRAVITY
        else:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.speed_x = 0

        self.rect.x += self.speed_x

        # Horizontal collision handling
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if self.speed_x > 0:
                    self.rect.right = block.rect.left
                elif self.speed_x < 0:
                    self.rect.left = block.rect.right

        self.rect.y += self.speed_y

        # Vertical collision handling
        self.is_touching_ground = False
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if self.speed_y > 0:
                    self.rect.bottom = block.rect.top
                    self.speed_y = 0
                    self.is_touching_ground = True
                    self.jump_counter = 0
                    self.dash_counter = 0  # Reset dash counter when touching the ground
                elif self.speed_y < 0:
                    self.rect.top = block.rect.bottom
                    self.speed_y = 0

        # Cap the jump height
        if self.is_jumping:
            if self.rect.y <= self.jump_start_y - self.jump_height_limit:
                self.speed_y = 0  # Stop the jump
                self.is_jumping = False

        # Screen bounds collision
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
            self.dash_counter = 0

    def move_left(self):
        self.speed_x = -MOVE_SPEED
        self.facing_left = True

    def move_right(self):
        self.speed_x = MOVE_SPEED
        self.facing_left = False

    def stop(self):
        if not self.is_dashing:
            self.speed_x = 0

    def jump(self):
        if self.jump_counter < 2:
            self.speed_y = -JUMP_HEIGHT
            self.jump_start_y = self.rect.y  # Record the starting Y position of the jump
            self.is_jumping = True
            self.jump_counter += 1

    def dash_left(self):
        if not self.is_dashing and self.dash_counter < 1:
            self.speed_x = -DASH_VELOCITY
            self.dash_timer = DASH_DURATION
            self.is_dashing = True
            self.dash_counter += 1

    def dash_right(self):
        if not self.is_dashing and self.dash_counter < 1:
            self.speed_x = DASH_VELOCITY
            self.dash_timer = DASH_DURATION
            self.is_dashing = True
            self.dash_counter += 1

    def reset_position(self):
        self.rect.topleft = (8 - 1) * BLOCK_SIZE, ((ord('o') - ord('a')) * BLOCK_SIZE)
        self.speed_x = 0
        self.speed_y = 0
        self.jump_counter = 0
        self.dash_counter = 0

class Spike(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, image_filename):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_filename)
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = pygame.Rect(self.rect.x + BLOCK_SIZE // 4, self.rect.y + BLOCK_SIZE // 4,
                                  BLOCK_SIZE // 2, BLOCK_SIZE // 2)

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

class Block(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, width, height, color):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class Diamond(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, image_filename):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load(image_filename)
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self):
        self.screen.blit(self.image, self.rect.topleft)

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

    block_sprites = pygame.sprite.Group()
    spike_sprites = pygame.sprite.Group()

    # Draw blocks
    for col, row in blocks:
        x = (col - 1) * BLOCK_SIZE
        y = (ord(row) - ord('a')) * BLOCK_SIZE
        block = Block(screen, x, y, BLOCK_SIZE, BLOCK_SIZE, BLOCK_COLOR)
        block.draw()
        block_sprites.add(block)

    # Draw spikes
    for col, row in spikes:
        x = (col - 1) * BLOCK_SIZE
        y = (ord(row) - ord('a')) * BLOCK_SIZE
        spike = Spike(screen, x, y, "spike1.png")  # Assuming you have a "spike1.png" image file
        spike.draw()
        spike_sprites.add(spike)

    return block_sprites, spike_sprites

def create_map2(screen):
    blocks = [
        # Outer walls
        *[(col, 'a') for col in range(1, 26)],
        *[(col, 's') for col in range(1, 26)],
        *[(1, row) for row in 'abcdefghijklmnopqrs'],
        *[(25, row) for row in 'abcdefghijklmnopqrs'],
        # Inner blocks
        (4, 'g'), (5, 'f'), (5, 'g'), (5, 'h'), (5, 'i'), (7, 'j'), (9, 'h'), (9, 'i'),
        (17, 'c'), (18, 'c'), (19, 'c'), (20, 'c'), (21, 'c'), (22, 'c'), (18, 'd'),
        (18, 'e'), (19, 'd')
    ]

    spikes = [(col, 'r') for col in range(2, 25)]
    spikes.append((20, 'm'))  # Add spike at the diamond's location in map 2
    spikes.append((19, 'm'))
    spikes.append((18, 'm'))
    spikes.append((12, 'p'))
    spikes.append((12, 'o'))
    spikes.append((11, 'o'))
    spikes.append((10, 'o'))

    block_sprites = pygame.sprite.Group()
    spike_sprites = pygame.sprite.Group()

    # Draw blocks
    for col, row in blocks:
        x = (col - 1) * BLOCK_SIZE
        y = (ord(row) - ord('a')) * BLOCK_SIZE
        block = Block(screen, x, y, BLOCK_SIZE, BLOCK_SIZE, BLOCK_COLOR)
        block.draw()
        block_sprites.add(block)

    # Draw spikes
    for col, row in spikes:
        x = (col - 1) * BLOCK_SIZE
        y = (ord(row) - ord('a')) * BLOCK_SIZE
        spike = Spike(screen, x, y, "spike1.png")
        spike.draw()
        spike_sprites.add(spike)

    return block_sprites, spike_sprites

def create_backgrounds(screen):
    global backgrounds
    background1 = pygame.Surface((WIDTH, HEIGHT))
    background1.fill(WHITE)
    block_sprites1, spike_sprites1 = create_map1(background1)
    diamond1 = Diamond(screen, (20 - 1) * BLOCK_SIZE, (ord('m') - ord('a')) * BLOCK_SIZE, "diamond.png")
    backgrounds.append((background1, block_sprites1, spike_sprites1, diamond1))

    background2 = pygame.Surface((WIDTH, HEIGHT))
    background2.fill(WHITE)
    block_sprites2, spike_sprites2 = create_map2(background2)
    backgrounds.append((background2, block_sprites2, spike_sprites2, None))

def draw_background(screen):
    background, _, _, diamond = backgrounds[current_background_index]
    screen.blit(background, (0, 0))
    if diamond:
        diamond.draw()

def display_win(screen):
    global record,start_time
    if record == 0:
        record = pygame.time.get_ticks()-start_time
        record /= 1000
    font = pygame.font.SysFont(None, 75)
    text_surface = font.render("YOU WIN"+str((record)), True, BLACK)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text_surface, text_rect)

    font_small = pygame.font.SysFont(None, 50)
    text_surface_small = font_small.render("Press SPACE BAR to play again", True, BLACK)
    text_rect_small = text_surface_small.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(text_surface_small, text_rect_small)

def reset_game(player, block_sprites, spike_sprites, diamond):
    global  start_time,record
    player.reset_position()
    player.speed_x = 0
    player.speed_y = 0
    player.jump_counter = 0
    player.dash_counter = 0
    start_time = pygame.time.get_ticks()
    record=0
def main():
    global  dev_mode,start_time,record
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    #pygame.display.set_caption("Dimension Hopper")
    clock = pygame.time.Clock()

    initial_x = (8 - 1) * BLOCK_SIZE
    initial_y = (ord('o') - ord('a')) * BLOCK_SIZE
    player = Player(screen, initial_x, initial_y, "HeroKidL.png", "HeroKidR.png")

    all_sprites = pygame.sprite.Group(player)

    # Create the backgrounds
    create_backgrounds(screen)

    game_won = False
    running = True
    font = pygame.font.Font(None, 74)
    while running:

        pygame.display.set_caption("Dimension Hopper")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    dev_mode = not dev_mode
                if event.key == pygame.K_ESCAPE:
                    running = False
                if not game_won:
                    if event.key == pygame.K_a:
                        player.move_left()
                    if event.key == pygame.K_d:
                        player.move_right()
                    if event.key == pygame.K_w:
                        player.jump()
                    if event.key == pygame.K_COMMA:
                        player.dash_left()
                    if event.key == pygame.K_PERIOD:
                        player.dash_right()
                    if event.key == pygame.K_SLASH:  # Change the background when '/' is pressed
                        change_background()
                if game_won and event.key == pygame.K_SPACE:
                    game_won = False
                    background, block_sprites, spike_sprites, diamond = backgrounds[current_background_index]
                    reset_game(player, block_sprites, spike_sprites, diamond)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player.stop()

        if not game_won:
            background, block_sprites, spike_sprites, diamond = backgrounds[current_background_index]
            player.update_player(block_sprites)

            # Collision with spikes
            if spike_sprites and not dev_mode:

                for spike in spike_sprites:
                    if player.rect.colliderect(spike.hitbox):
                        reset_to_map1()
                        record = 0
                        start_time = pygame.time.get_ticks()
                        player.reset_position()

            # Collision with diamond
            if diamond and player.rect.colliderect(diamond.rect):
                game_won = True

            screen.fill(WHITE)
            draw_background(screen)
            all_sprites.draw(screen)
            player.draw()
        else:
            screen.fill(WHITE)
            display_win(screen)
        screen.blit(font.render(str((pygame.time.get_ticks()-start_time)/1000), True, "WHITE"), (0, 0))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
