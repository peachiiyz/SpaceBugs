#!/usr/bin/env python

# Imports and global variables -----------------------------------------------
import pygame
from modules.images import *
from modules.explosion import *
from modules.message import *

# Display width and height.
display_width, display_height = 800, 600
# Bullet variables.
bullet_x, bullet_y = 0, 500
bullet_y_change = 15
bullet_state = False
# Enemy Bullet variables.
enemy_bullet_y_change = 17.5
enemy_bullet_state = False
# Colors.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLDEN_YELLOW = (212, 175, 55)
GREY = (175, 175, 175)
# Fonts.
pygame.font.init()
small_font = pygame.font.SysFont("Comic Sans MS", 30)
medium_font = pygame.font.SysFont("Comic Sans MS", 40)
large_font = pygame.font.SysFont("Comic Sans MS", 60)


# Functions ------------------------------------------------------------------
# Firing bullet.
def fire_bullet(x, y, canvas):
    """
    
    """
    global bullet_state
    bullet_state = True
    canvas.blit(bullet, (x + 51, y - 77))


# Enemy firing bullet.
def enemy_shoot(x, y, canvas):
    """
    
    """
    global enemy_bullet_state
    enemy_bullet_state = True
    canvas.blit(enemy_bullet, (x+12, y+23))


# Main function.
def main():
    global bullet_x, bullet_y, bullet_state, enemy, \
           enemy_health_bar, enemy_bullet, enemy_bullet_state, health_bar
    # Setting the game display.
    game_display = pygame.display.set_mode((display_width, display_height))
    # Spaceship variables.
    spaceship_x, spaceship_y = display_width-440, display_height-170
    spaceship_x_change = 0
    spaceship_health = 15
    # Enemy variables.
    enemy_x, enemy_y = 10, 30
    enemy_x_change = 5
    enemy_hp = 5
    enemy_border = 53
    enemy_x_width, enemy_y_width = 61, 43
    enemy_stage_counter = 2
    enemy_mid_point_x, enemy_mid_point_y = 12, 15
    enemy_hp_counter = 5
    enemy_bullet_x, enemy_bullet_y = 0, 30
    bullet_width, bullet_length = 9, 27
    enemy_damage = 1
    # Explosion animation.
    explosion_group = pygame.sprite.Group()

    # Creating a loop to keep program running.
    while True:
        # Setting a background.
        game_display.blit(background, (0, 0))
        # Add explosion to screen.
        explosion_group.draw(game_display)
        explosion_group.update()
        # Event Processing and controls.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    spaceship_x_change = 3
                elif event.key == pygame.K_a:
                    spaceship_x_change = -3
                elif event.key == pygame.K_SPACE:
                    if not bullet_state:
                        bullet_x = spaceship_x
                        fire_bullet(bullet_x, bullet_y, game_display)
                if event.key == pygame.K_q:
                    quit()
            elif event.type == pygame.KEYUP:
                spaceship_x_change = 0
        
        # Bullet hitboxes.
        bullet_rect = pygame.Rect(bullet_x + 52, bullet_y - 70, 18, 55)
        enemy_bullet_rect = pygame.Rect(enemy_bullet_x+13, enemy_bullet_y+20,
                                        bullet_width, bullet_length)

        # Bullet movement.
        if bullet_y <= 0:
            bullet_y = 375
            bullet_state = False  # Resets bullet once gone past screen.

        if bullet_state:
            fire_bullet(bullet_x, bullet_y, game_display)
            bullet_y -= bullet_y_change  # Firing the bullet.

        # Enemy Bullet.
        for r in list(range(-1, 1)):
            if enemy_x+r == spaceship_x:
                if not enemy_bullet_state:
                    enemy_bullet_x = enemy_x  # Fire when bullet in range.
                    enemy_shoot(enemy_x, enemy_y, game_display)

        # Enemy bullet movement.
        if enemy_bullet_y >= display_height:
            enemy_bullet_y = 30
            enemy_bullet_state = False  # Resets enemy's bullet.

        if enemy_bullet_state:
            enemy_shoot(enemy_bullet_x, enemy_bullet_y, game_display)
            enemy_bullet_y += enemy_bullet_y_change

        # Ship movement.
        spaceship_x += spaceship_x_change
        # Preventing the ship from going off the screen
        if spaceship_x > display_width - 117:
            spaceship_x = display_width - 117
        if spaceship_x < 0:
            spaceship_x = 0

        # Displaying spaceship
        if spaceship_health > 0:
            game_display.blit(spaceship, (spaceship_x, spaceship_y))
            game_display.blit(health_bar, (5, display_height-80))
            spaceship_rect = pygame.Rect(spaceship_x, spaceship_y+3, 120, 117)
        else:
            message("Game over, press Q to quit", GREY, 165, 250,
                    medium_font, game_display)
            enemy_bullet_state = False
            bullet_state = False
        
        # Enemy moving left to right.
        enemy_x += enemy_x_change
        enemy_rect = pygame.Rect(enemy_x-4, enemy_y+6,
                                 enemy_x_width, enemy_y_width)

        # Preventing the enemy from going off the screen.
        if enemy_x > display_width-enemy_border:
            enemy_x_change = -3
        if enemy_x < 1:
            enemy_x_change = 3

        # How the enemy takes damage.
        if bullet_rect.colliderect(enemy_rect):
            explosion = Explosion(enemy_x+enemy_mid_point_x,
                                  enemy_y+enemy_mid_point_y)
            explosion_group.add(explosion)
            enemy_hp -= 1
            enemy_hp_counter -= 1
            bullet_y = 480
            bullet_state = False
        if enemy_stage_counter == 2:
            enemy_health_bar = pygame.image.load("assets/health_bar/" +
                                                 f"{enemy_hp_counter*3}HP.png")
        if enemy_hp == 0:
            enemy_stage_counter -= 1
            if enemy_stage_counter == 0:
                enemy = pygame.image.load("assets/enemies/S2Enemy.png")
                enemy_bullet = pygame.image.load("assets/bullets/enemy_bullet2.png")
                enemy_damage = 2
                bullet_width, bullet_length = 30, 60
                enemy_hp = 15
                enemy_border = 145
                enemy_x_width, enemy_y_width = 119, 150
                enemy_mid_point_x, enemy_mid_point_y = 60, 75
        if enemy_hp == 10:
            enemy = pygame.image.load("assets/enemies/S2EnemyDamaged1.png")
        if enemy_hp == 5:
            if enemy_stage_counter == 0:
                enemy = pygame.image.load("assets/enemies/S2EnemyDamaged2.png")
        if enemy_stage_counter == 0:
            enemy_health_bar = pygame.image.load("assets/health_bar/" +
                                                 f"{enemy_hp}HP.png")
        if enemy_bullet_rect.colliderect(spaceship_rect):
            enemy_explosion = Explosion(spaceship_x+60, spaceship_y)
            explosion_group.add(enemy_explosion)
            spaceship_health -= enemy_damage
            enemy_bullet_y = enemy_y
            enemy_bullet_state = False
        if enemy_hp > 0:
            game_display.blit(enemy, (enemy_x, enemy_y))
            game_display.blit(enemy_health_bar, (5, -30))
        if enemy_hp <= 0:
           if enemy_stage_counter < 0:
                spaceship_health = 15
                message("PLAYER WINS!!!", GOLDEN_YELLOW, 150, 220,
                        large_font, game_display)
                message("Press Q to exit.", WHITE, 200, 300,
                        small_font, game_display)
                enemy_bullet_state = False

        # Player health bar
        if spaceship_health >= 0:
            health_bar = pygame.image.load("assets/health_bar/" +
                                           f"{spaceship_health}HP.png")
        # Updating Screen so changes take places
        pygame.display.update()
        # Setting FPS
        FPS = pygame.time.Clock()
        FPS.tick(120)


# Main -----------------------------------------------------------------------
# Initializing Pygame
pygame.init()
# Setting a display caption and icon
pygame.display.set_caption("Space Bugs")
pygame.display.set_icon(logo)
intro_display = pygame.display.set_mode((display_width, display_height))

# Creating Introduction screen
while True:
    intro_display.fill(BLACK)
    pygame.event.poll()
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    message("Space Bugs", WHITE, display_width-570, 150,
            large_font, intro_display)
    if 250 > mouse[0] > 150 and display_height-100 > mouse[1] \
       > display_height-150:
        pygame.draw.rect(intro_display, GREY,
                         [150, display_height-150, 100, 50])
        if click[0] == 1:
            main()
    else:
        pygame.draw.rect(intro_display, WHITE,
                         [150, display_height-150, 100, 50])

    if display_width-150 > mouse[0] > display_width-250 and \
       display_height-100 > mouse[1] > display_height-150:
        pygame.draw.rect(intro_display, GREY,
                         [display_width-250, display_height-150, 100, 50])
        if click[0] == 1:
            pygame.quit()
            quit()
    else:
        pygame.draw.rect(intro_display, WHITE,
                         [display_width-250, display_height-150, 100, 50])

    # Writing Start and Quit on the buttons on screen.
    message("Start", BLACK, 160, display_height-150, small_font, intro_display)
    message("Quit", BLACK, display_width-235, display_height-150,
            small_font, intro_display)
    # Updating screen so changes take place.
    pygame.display.update()
