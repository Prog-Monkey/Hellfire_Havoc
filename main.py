import pygame
import random
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
    K_x,
    KEYUP,
    MOUSEBUTTONDOWN
)

# Initialize pygame
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("Music FromSoftware 2011.mp3")
pygame.mixer.music.play(loops=1001, start=10, fade_ms=100)
pygame.mixer.music.set_volume(2)

# Define constants for the screen width and height
info = pygame.display.Info()
screen_width = info.current_w
screen_height =info.current_h
screen_size = screen_width, screen_height

# Platform and character sizes
platform_width = 200
platform_height = 30
character_width = 50
character_height = 50

# Create the screen object
screen = pygame.display.set_mode(screen_size)

# Load the character image
ghost = pygame.image.load('images/ghost_final.png')
ghost = pygame.transform.scale(ghost, (character_width, character_height))
god = pygame.image.load("images/God.png")
god = pygame.transform.scale(god, (character_width, character_height))  # Resize god image
grave = pygame.image.load("images/grave_stone.png")
grave = pygame.transform.scale(grave, (character_width+50, character_height+50))  # Resize grave image
icon = god
icon = pygame.transform.scale(icon, (80, 50))
pygame.display.set_caption("Hellfire Havoc")
pygame.display.set_icon(icon)

# Hydra image
hydra = pygame.image.load("images/Hydra.png").convert_alpha()
hydra = pygame.transform.scale(hydra, (64, 64))

# Define gravity and initial velocities
gravity = 0.5
jump_velocity = -12

# Load the background image
background1 = pygame.image.load("images/background.png").convert()
background2 = pygame.image.load("images/background2.png").convert()
background3 = pygame.image.load("images/background3.png").convert()
background4 = pygame.image.load("images/background4.png").convert()
background = random.randint(0,5)
platform_image = pygame.image.load("images/Platform.png").convert()
backgroundGame = backgroundGame = pygame.transform.scale(background1, screen_size)
if background == 1:
    backgroundGame = pygame.transform.scale(background1, screen_size)
    platform_image = pygame.image.load("images/Platform.png").convert()
elif background==2:
    backgroundGame = pygame.transform.scale(background2, screen_size)
    platform_image = pygame.image.load("images/Platform.png").convert()
elif background==3:
    backgroundGame = pygame.transform.scale(background3, screen_size)
    platform_image = pygame.image.load("images/Platform.png").convert()
elif background==4:
    backgroundGame = pygame.transform.scale(background4, screen_size)
    platform_image = pygame.image.load("images/Platform1.png").convert_alpha()



# Define font and create a text surface
font1 = pygame.font.Font("fonts/Micro5-Regular.ttf", 70)
font2 = pygame.font.Font("fonts/Micro5-Regular.ttf", 50)
game_over_textE = font1.render("Hell Won", True, (255, 0, 0))
game_over_textG = font1.render("God Won", True, (255, 0, 0))
restart_text = font2.render("Press X to Restart", True, (0, 255, 20))

# Platform class
class Platform(pygame.sprite.Sprite):
    global platform_image
    def __init__(self, x, y, width, height, image):
        super().__init__()
        
        if image:
            self.image = platform_image
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = pygame.Surface([width, height])
            self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Function to generate random platforms
def generate_random_platforms():
    platforms = pygame.sprite.Group()

    # Add platform covering the entire ground
    ground_platform = Platform(0, screen_height - platform_height, screen_width, platform_height, platform_image)
    platforms.add(ground_platform)

    # Generate random platforms
    num_platforms = random.randint(5, 10)  # Random number of platforms
    for _ in range(num_platforms):
        x = random.randint(0, screen_width - platform_width)
        y = random.randint(100, screen_height - platform_height - 50)
        platform = Platform(x, y, platform_width, platform_height, "images/Platform.png")
        platforms.add(platform)

    return platforms

# Create initial platforms
platforms = generate_random_platforms()

# Custom Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

# Create sprite objects for ghost and hydra using the custom Player class
ghost_sprite = Player(ghost, screen_width // 2, screen_height // 2)
hydra_sprite = Player(hydra, screen_width // 7, screen_height // 2)

ghost_life = True
ghost_won = False
running = True


# Define menu variables
menu_font = pygame.font.Font("fonts/StalinistOne-Regular.ttf", 48)
font_copyright = pygame.font.Font("fonts/StalinistOne-Regular.ttf", 10)
font_owner = pygame.font.Font(None, 30)
play_text = menu_font.render("Play", True, (255, 255, 255))
play_rect = play_text.get_rect(center=(screen_width // 2, screen_height // 2))
title_text = menu_font.render("HELLFIRE HAVOC", True, (255, 0, 0))
title_rect = play_text.get_rect(center=(350, screen_height // 7))
menu_background = pygame.image.load("images/Hell_Menu.jpg")
menu_background = pygame.transform.scale(menu_background, (screen_width, screen_height))
menu_rect = menu_background.get_rect(center=(screen_width//2,screen_height//2))
copyright_text = font_copyright.render("Composer: Motoi Sakuraba Track #22 Japanese Collector's Edition of Dark Souls ©2011 FromSoftware", True, (255, 255, 255))
copyright_rect = copyright_text.get_rect(center=(500,630))
owner_text = font_owner.render("made by the champion", True, (255, 255, 255))
owner_rect = owner_text.get_rect(center=(screen_width/2,500))
# Menu loop

menu_running = True
while menu_running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.type == QUIT:
                menu_running = False
                running = False
            elif event.key == K_ESCAPE:
                menu_running = False
                running = False
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if play_rect.collidepoint(mouse_pos):
                menu_running = False
                clock = pygame.time.Clock()
                start_ticks = pygame.time.get_ticks()  # Get the current time in milliseconds
                countdown_seconds = 20
    
    screen.blit(menu_background,menu_rect)
    screen.blit(copyright_text, copyright_rect)
    screen.blit(owner_text, owner_rect)
    screen.blit(play_text, play_rect)
    screen.blit(title_text,title_rect)
   
    pygame.display.flip()

# Main game loop
while running and not menu_running:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == KEYDOWN and not ghost_won and ghost_life:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_LEFT:
                ghost_sprite.velocity_x = -9
            elif event.key == K_RIGHT:
                ghost_sprite.velocity_x = 9
            elif event.key == K_UP and not jumping_ghost:
                jumping_ghost = True
                ghost_sprite.velocity_y = jump_velocity

            elif event.key == K_a:
                hydra_sprite.velocity_x = -7
            elif event.key == K_d:
                hydra_sprite.velocity_x = 7
            elif event.key == K_w and not jumping_hydra:
                jumping_hydra = True
                hydra_sprite.velocity_y = jump_velocity
        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                ghost_sprite.velocity_x = 0
            if event.key == K_a or event.key == K_d:
                hydra_sprite.velocity_x = 0

        # Check for key press to restart the game
        if event.type == KEYDOWN and event.key == K_x and not ghost_life:
            # Reset the game
            ghost_sprite.rect.center = (screen_width // 2, screen_height // 2)
            hydra_sprite.rect.center = (screen_width // 7, hydra_sprite.rect.width // 2)
            ghost_life = True
            ghost_won = False
            jumping_ghost = False
            jumping_hydra = False
            ghost_sprite.image = ghost  # Change ghost back to ghost image
            hydra_sprite.image = hydra  # Change hydra back to hydra image
            background = random.randint(0,5)
            if background == 1:
                backgroundGame = pygame.transform.scale(background1, screen_size)
                platform_image = pygame.image.load("images/Platform.png").convert()
            elif background==2:
                backgroundGame = pygame.transform.scale(background2, screen_size)
                platform_image = pygame.image.load("images/Platform.png").convert()
            elif background==3:
                backgroundGame = pygame.transform.scale(background3, screen_size)
                platform_image = pygame.image.load("images/Platform.png").convert()
            elif background==4:
                backgroundGame = pygame.transform.scale(background4, screen_size)
                platform_image = pygame.image.load("images/Platform1.png").convert_alpha()
            platforms = generate_random_platforms()
            start_ticks = pygame.time.get_ticks()  # Reset the timer
        if event.type == KEYDOWN and event.key == K_x and ghost_won:
            # Reset the game
            ghost_sprite.rect.center = (screen_width // 2, screen_height // 2)
            hydra_sprite.rect.center = (screen_width // 7, hydra_sprite.rect.width // 2)
            ghost_life = True
            ghost_won = False
            jumping_ghost = False
            jumping_hydra = False
            ghost_sprite.image = ghost  # Change ghost back to ghost image
            hydra_sprite.image = hydra  # Change hydra back to hydra image
            background = random.randint(0,5)
            if background == 1:
                backgroundGame = pygame.transform.scale(background1, screen_size)
                platform_image = pygame.image.load("images/Platform.png").convert_alpha()
            elif background==2:
                backgroundGame = pygame.transform.scale(background2, screen_size)
                platform_image = pygame.image.load("images/Platform.png").convert_alpha()
            elif background==3:
                backgroundGame = pygame.transform.scale(background3, screen_size)
                platform_image = pygame.image.load("images/Platform.png").convert_alpha()
            elif background==4:
                backgroundGame = pygame.transform.scale(background4, screen_size)
                platform_image = pygame.image.load("images/Platform1.png").convert_alpha()
                platforms = generate_random_platforms()
            start_ticks = pygame.time.get_ticks()  # Reset the timer

    if not ghost_won and ghost_life:
        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000

        # Calculate remaining time
        remaining_seconds = countdown_seconds - elapsed_seconds

        if remaining_seconds <= 0:
            remaining_seconds = 0  # Stop the timer from going negative
            ghost_won = True  # Ghost wins after 30 seconds

    # Apply gravity to ghost and hydra
    ghost_sprite.velocity_y += gravity
    hydra_sprite.velocity_y += gravity

    # Update player positions
    ghost_sprite.update()
    hydra_sprite.update()

    # Check for collisions with platforms
    ghost_collided_platforms = pygame.sprite.spritecollide(ghost_sprite, platforms, False)
    for platform in ghost_collided_platforms:
        if ghost_sprite.velocity_y > 0:  # Check if ghost is moving downwards
            ghost_sprite.rect.bottom = platform.rect.top  # Set ghost's bottom to top of platform
            ghost_sprite.velocity_y = 0  # Stop ghost's vertical movement
            jumping_ghost = False  # Ghost is no longer jumping
        elif ghost_sprite.velocity_y < 0:  # Check if ghost is moving upwards
            ghost_sprite.rect.top = platform.rect.bottom  # Set ghost's top to bottom of platform
            ghost_sprite.velocity_y = 0  # Stop ghost's vertical movement

    hydra_collided_platforms = pygame.sprite.spritecollide(hydra_sprite, platforms, False)
    for platform in hydra_collided_platforms:
        if hydra_sprite.velocity_y > 0:  # Check if hydra is moving downwards
            hydra_sprite.rect.bottom = platform.rect.top  # Set hydra's bottom to top of platform
            hydra_sprite.velocity_y = 0  # Stop hydra's vertical movement
            jumping_hydra = False  # Hydra is no longer jumping
        elif hydra_sprite.velocity_y < 0:  # Check if hydra is moving upwards
            hydra_sprite.rect.top = platform.rect.bottom  # Set hydra's top to bottom of platform
            hydra_sprite.velocity_y = 0  # Stop hydra's vertical movement

    # Limit the ghost and hydra within the screen boundaries
    ghost_sprite.rect.x = max(0, min(ghost_sprite.rect.x, screen_width - ghost_sprite.rect.width))
    ghost_sprite.rect.y = max(0, min(ghost_sprite.rect.y, screen_height - ghost_sprite.rect.height))

    hydra_sprite.rect.x = max(0, min(hydra_sprite.rect.x, screen_width - hydra_sprite.rect.width))
    hydra_sprite.rect.y = max(0, min(hydra_sprite.rect.y, screen_height - hydra_sprite.rect.height))

    # Fill the screen with the background color
    screen.blit(backgroundGame, (0, 0))

    # Blit the platforms
    platforms.draw(screen)

    # Blit the characters
    screen.blit(ghost_sprite.image, ghost_sprite.rect)
    screen.blit(hydra_sprite.image, hydra_sprite.rect)

    if ghost_sprite.rect.colliderect(hydra_sprite.rect):
        ghost_life = False

    # Display "Game Over" text if ghost is dead
    if not ghost_life:
        screen.blit(grave, ghost_sprite.rect)  # Change ghost to grave image
        ghost_sprite.image = grave  # Blit grave image

        game_over_rect = game_over_textE.get_rect(center=(screen_width // 2, screen_height // 2 - 30))
        screen.blit(game_over_textE, game_over_rect)

        restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 30))
        screen.blit(restart_text, restart_rect)
        
    if ghost_won:
        ghost_sprite.image = god  # Change ghost image to god

        god_rect = god.get_rect(center=ghost_sprite.rect.center)
        screen.blit(god, god_rect)  # Blit god image

        game_over_rect = game_over_textG.get_rect(center=(screen_width // 2, screen_height // 2 - 30))
        screen.blit(game_over_textG, game_over_rect)

        restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 30))
        screen.blit(restart_text, restart_rect)
      
    timer_text = font2.render(f"Time: {remaining_seconds}", True, (255, 255, 255))
    screen.blit(timer_text, (10, 10))
    # Update the display
    pygame.display.update()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()