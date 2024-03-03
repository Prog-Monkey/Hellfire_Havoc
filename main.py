import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_UP,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_a,
    K_d,
    KEYUP,
    K_x
)

# Initialize pygame
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("Music.mp3")
pygame.mixer.music.play(loops=1001, start=10, fade_ms=100)
pygame.mixer.music.set_volume(2)

# Define constants for the screen width and height
screen_width = 1200
screen_height = 650
screen_size = screen_width, screen_height
CYAN = (0, 255, 255)
background_color = CYAN

# Platform and character sizes
platform_width = 200
platform_height = 30
character_width = 50
character_height = 50

# Create the screen object
screen = pygame.display.set_mode(screen_size)

# Load the character image
ghost = pygame.image.load('ghost_final.png')
ghost = pygame.transform.scale(ghost, (character_width, character_height))
god = pygame.image.load("God.png")
god = pygame.transform.scale(god, (character_width, character_height))  # Resize god image
grave = pygame.image.load("grave_stone.png")
grave = pygame.transform.scale(grave, (character_width, character_height))  # Resize grave image
icon = god
icon = pygame.transform.scale(icon, (80, 50))
pygame.display.set_caption("The Capture")
pygame.display.set_icon(icon)

# Hydra image
hydra = pygame.image.load("Hydra.png").convert_alpha()
hydra = pygame.transform.scale(hydra, (64, 64))

# Define gravity and initial velocities
gravity = 0.5
ghost_velocity_y = 0  # Set initial vertical velocity to 0
hydra_velocity_y = 0  # Set initial vertical velocity for hydra to 0
jumping_ghost = False
jumping_hydra = False
jump_velocity = -12

# Define player movement variables
ghost_vel_x = 0
hydra_vel_x = 0
acceleration = 5
friction = 0

# Load the background image
background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, screen_size)

# Define font and create a text surface
font1 = pygame.font.Font("Micro5-Regular.ttf", 70)
font2 = pygame.font.Font("Micro5-Regular.ttf", 50)
game_over_textE = font1.render("Hell Won", True, (255, 0, 0))
game_over_textG = font1.render("God Won", True, (255, 0, 0))
restart_text = font2.render("Press X to Restart", True, (0, 255, 20))

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image=None):
        super().__init__()
        if image:
            self.image = pygame.image.load(image).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = pygame.Surface([width, height])
            self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create platforms
platforms = pygame.sprite.Group()
platform1 = Platform(0, screen_height -1, screen_width, platform_height, "Platform.png")
platform2 = Platform(0, screen_height - 100, platform_width, platform_height, "Platform.png")
platform3 = Platform(0, screen_height - 200, 20, 50, "Platform.png")
platforms.add(platform1, platform2)

# Create sprite objects for ghost and hydra
ghost_sprite = pygame.sprite.Sprite()
ghost_sprite.image = ghost
ghost_sprite.rect = ghost_sprite.image.get_rect()
ghost_sprite.rect.center = (screen_width // 2, screen_height // 2)

hydra_sprite = pygame.sprite.Sprite()
hydra_sprite.image = hydra
hydra_sprite.rect = hydra_sprite.image.get_rect()
hydra_sprite.rect.center = (screen_width // 7, hydra_sprite.rect.width // 2)

ghost_life = True
ghost_won = False
running = True
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()  # Get the current time in milliseconds
countdown_seconds = 30
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == KEYDOWN and ghost_life:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_LEFT:
                ghost_vel_x = -9
            elif event.key == K_RIGHT:
                ghost_vel_x = 9
            elif event.key == K_UP and not jumping_ghost:
                jumping_ghost = True
                ghost_velocity_y = jump_velocity

            elif event.key == K_a:
                hydra_vel_x = -7
            elif event.key == K_d:
                hydra_vel_x = 7
            elif event.key == K_w and not jumping_hydra:
                jumping_hydra = True
                hydra_velocity_y = jump_velocity
        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                ghost_vel_x = 0
            if event.key == K_a or event.key == K_d:
                hydra_vel_x = 0

        # Check for key press to restart the game
        elif event.type == KEYDOWN and event.key == K_x and not ghost_life:
            # Reset the game
            ghost_sprite.rect.center = (screen_width // 2, screen_height // 2)
            hydra_sprite.rect.center = (screen_width // 7, hydra_sprite.rect.width // 2)
            ghost_life = True
            ghost_won = False
            jumping_ghost = False
            jumping_hydra = False
            ghost_sprite.image = ghost  # Change ghost back to ghost image
            hydra_sprite.image = hydra  # Change hydra back to hydra image
            start_ticks = pygame.time.get_ticks()  # Reset the timer
        elif event.type == KEYDOWN and event.key == K_x and ghost_won:
            # Reset the game
            ghost_sprite.rect.center = (screen_width // 2, screen_height // 2)
            hydra_sprite.rect.center = (screen_width // 7, hydra_sprite.rect.width // 2)
            ghost_life = True
            ghost_won = False
            jumping_ghost = False
            jumping_hydra = False
            ghost_sprite.image = ghost  # Change ghost back to ghost image
            hydra_sprite.image = hydra  # Change hydra back to hydra image
            start_ticks = pygame.time.get_ticks()  # Reset the timer
    if not ghost_won and ghost_life:
        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000

        # Calculate remaining time
        remaining_seconds = countdown_seconds - elapsed_seconds

        if remaining_seconds <= 0:
            remaining_seconds = 0  # Stop the timer from going negative
            ghost_won = True  # Ghost wins after 30 seconds

    # Apply gravity to ghost and hydra
    ghost_velocity_y += gravity
    hydra_velocity_y += gravity

    # Apply horizontal movement for ghost and hydra
    ghost_sprite.rect.x += ghost_vel_x
    hydra_sprite.rect.x += hydra_vel_x

    # Apply friction to slow down ghost and hydra
    if ghost_vel_x != 0:
        if ghost_vel_x > 0:
            ghost_vel_x = max(0, ghost_vel_x - friction)
        else:
            ghost_vel_x = min(0, ghost_vel_x + friction)

    if hydra_vel_x != 0:
        if hydra_vel_x > 0:
            hydra_vel_x = max(0, hydra_vel_x - friction)
        else:
            hydra_vel_x = min(0, hydra_vel_x + friction)

    # Apply vertical movement for ghost and hydra
    ghost_sprite.rect.y += ghost_velocity_y
    hydra_sprite.rect.y += hydra_velocity_y

    # Check for collisions with platforms
 # Check for collisions with platforms
    ghost_collided_platforms = pygame.sprite.spritecollide(ghost_sprite, platforms, False)
    for platform in ghost_collided_platforms:
        if ghost_velocity_y > 0:  # Check if ghost is moving downwards
            ghost_sprite.rect.bottom = platform.rect.top  # Set ghost's bottom to top of platform
            ghost_velocity_y = 0  # Stop ghost's vertical movement
            jumping_ghost = False  # Ghost is no longer jumping
        elif ghost_velocity_y < 0:  # Check if ghost is moving upwards
            ghost_sprite.rect.top = platform.rect.bottom  # Set ghost's top to bottom of platform
            ghost_velocity_y = 0  # Stop ghost's vertical movement

    hydra_collided_platforms = pygame.sprite.spritecollide(hydra_sprite, platforms, False)
    for platform in hydra_collided_platforms:
        if hydra_velocity_y > 0:  # Check if hydra is moving downwards
            hydra_sprite.rect.bottom = platform.rect.top  # Set hydra's bottom to top of platform
            hydra_velocity_y = 0  # Stop hydra's vertical movement
            jumping_hydra = False  # Hydra is no longer jumping
        elif hydra_velocity_y < 0:  # Check if hydra is moving upwards
            hydra_sprite.rect.top = platform.rect.bottom  # Set hydra's top to bottom of platform
            hydra_velocity_y = 0  # Stop hydra's vertical movement

    # Check for collision between ghost and hydra
    if ghost_sprite.rect.colliderect(hydra_sprite.rect):
        ghost_life = False

    # Limit the ghost and hydra within the screen boundaries
    ghost_sprite.rect.x = max(0, min(ghost_sprite.rect.x, screen_width - ghost_sprite.rect.width))
    ghost_sprite.rect.y = max(0, min(ghost_sprite.rect.y, screen_height - ghost_sprite.rect.height))

    hydra_sprite.rect.x = max(0, min(hydra_sprite.rect.x, screen_width - hydra_sprite.rect.width))
    hydra_sprite.rect.y = max(0, min(hydra_sprite.rect.y, screen_height - hydra_sprite.rect.height))

    # Fill the screen with the background color
    screen.blit(background, (0, 0))

    # Blit the platforms
    platforms.draw(screen)

    # Blit the characters
    screen.blit(ghost_sprite.image, ghost_sprite.rect)
    screen.blit(hydra_sprite.image, hydra_sprite.rect)

    # Display "Game Over" text if ghost is dead
    if not ghost_life:
        game_over_rect = game_over_textE.get_rect(center=(screen_width // 2, screen_height // 2 - 30))
        screen.blit(game_over_textE, game_over_rect)
        restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 30))
        screen.blit(restart_text, restart_rect)
        screen.blit(grave, ghost_sprite.rect)  # Change ghost to grave image
        ghost_sprite.image = grave  # Change ghost image to grave
        ghost_vel_x = 0  # Stop ghost movement
        hydra_vel_x = 0  # Stop hydra movement
    else:
        ghost_sprite.image = ghost
        hydra_sprite.image = hydra

    if ghost_won:
        game_over_rect = game_over_textG.get_rect(center=(screen_width // 2, screen_height // 2 - 30))
        screen.blit(game_over_textG, game_over_rect)
        restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 30))
        screen.blit(restart_text, restart_rect)
        screen.blit(god, ghost_sprite.rect)  # Change ghost to god image
        ghost_sprite.image = god  # Change ghost image to god
        ghost_vel_x = 0  # Stop ghost movement
        hydra_vel_x = 0  # Stop hydra movement
    else:
        ghost_sprite.image = ghost
        hydra_sprite.image = hydra

    # Display the remaining time
    timer_text = font2.render(f"Time: {remaining_seconds}", True, (255, 255, 255))
    screen.blit(timer_text, (10, 10))

    # Update the display
    pygame.display.update()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
