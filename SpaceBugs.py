#!/usr/bin/env python

# Importing packages
import pygame
import sys

# Initializing Pygame
pygame.init()


# Importing images
healthBar = pygame.image.load("IMGS/HealthBar/15HP.png")
enemyHealthBar = pygame.image.load("IMGS/HealthBar/15HP.png")
spaceship = pygame.image.load("IMGS/SpaceshipResize.png")
bullet = pygame.image.load("IMGS/bullet.png")
enemyBullet = pygame.image.load("IMGS/smallBullet.png")
enemy = pygame.image.load("IMGS/Enemy.png")
BG = pygame.image.load("IMGS/BG.png")
logo = pygame.image.load("IMGS/rocket.png")

# Setting a display caption and icon
pygame.display.set_caption("Space Bugs")
pygame.display.set_icon(logo)

# Setting a display width and height and then creating it
display_width, display_height = 700, 500
game_display = pygame.display.set_mode((display_width, display_height))
intro_display = pygame.display.set_mode((display_width, display_height))

# Bullet
bulletX = 0
bulletY = 375
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Enemy Bullet
enemyBulletXChange = 0
enemyBulletYChange = 15
enemyBulletState = "ready"

# Create fonts and a way to add text to screen
pygame.font.init()
font = pygame.font.SysFont("consolas", 30)
large_font = pygame.font.SysFont("consolas", 60)
medium_font = pygame.font.SysFont("consolas", 40)
small_font = pygame.font.SysFont("consolas", 20)
impact = pygame.font.SysFont("impact", 30, True)
def message(sentence, color, x, y, font_type, display):
    sentence = font_type.render(str.encode(sentence), True, color)
    display.blit(sentence, [x, y])


# Create Explosion class
class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(f"IMGS/img/exp{num}.png")
			img = pygame.transform.scale(img, (100, 100))
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

	def update(self):
		explosion_speed = 4
		# Update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		# If the animation is complete, reset animation index
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()


# Firing bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    game_display.blit(bullet, (x + 51, y - 77))


def enemyShoot(x, y):
    global enemyBulletState
    enemyBulletState = "fire"
    game_display.blit(enemyBullet, (x+12, y+23))


# Main function
def main():
    global bulletY
    global bullet_state
    global bulletX
    global bulletRect
    global enemy
    global enemyHealthBar
    global enemyBullet
    global enemyBulletState
    global healthBar

    # Spaceship variables
    spaceship_x = 260
    spaceship_y = 330
    spaceship_x_change = 0
    spaceship_health = 15


    # Initializing pygame
    pygame.init()

    # Creating colors
    golden_yellow = (212, 175, 55)
    grey = (175, 175, 175)
    white = (255, 255, 255)

    # Enemy variables
    enemy_x = 10
    enemy_y = 30
    enemyXChange = 7
    enemyHP = 5
    enemy_border = 53
    enemyXwidth = 61
    enemyYwidth = 43
    EnemyStageCounter = 2
    EnemyMidPointX = 12
    EnemyMidPointY = 15
    enemyHPCounter = 5
    enemyBulletX = 0
    enemyBulletY = 30
    bulletWidth = 9
    bulletLength = 27
    enemyDamage = 1

    # Explosion animation
    explosion_group = pygame.sprite.Group()

    # Creating a loop to keep program running
    while True:

        # Setting a background
        game_display.blit(BG, (0, 0))

        # Add explosion to screen
        explosion_group.draw(game_display)
        explosion_group.update()

        # --- Event Processing and controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    spaceship_x_change = 3
                elif event.key == pygame.K_LEFT:
                    spaceship_x_change = -3
                elif event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = spaceship_x
                        fire_bullet(bulletX, bulletY)
                if event.key == pygame.K_q:
                    sys.exit()
            elif event.type == pygame.KEYUP:
                spaceship_x_change = 0
        
        # Bullet hitboxes
        bulletRect = pygame.Rect(bulletX + 52, bulletY - 70, 18, 55)
        enemyBulletRect = pygame.Rect(enemyBulletX+13, enemyBulletY+20, bulletWidth, bulletLength)

        # Bullet movement
        if bulletY <= 0:
            bulletY = 375
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        # Enemy Bullet
        for r in list(range(-1, 1)):
            if enemy_x+r == spaceship_x:
                if enemyBulletState == "ready":
                    enemyBulletX = enemy_x
                    enemyShoot(enemy_x, enemy_y)

        # Enemy bullet movement
        if enemyBulletY >= 700:
            enemyBulletY = 30
            enemyBulletState = "ready"
        
        if enemyBulletState == "fire":
            enemyShoot(enemyBulletX, enemyBulletY)
            enemyBulletY += enemyBulletYChange

        # Ship movement
        spaceship_x += spaceship_x_change
        # Preventing the ship from going off the screen
        if spaceship_x > display_width - 117:
            spaceship_x = display_width - 117
        if spaceship_x < 0:
            spaceship_x = 0

		# Displaying spaceship
        if spaceship_health > 0:
            game_display.blit(spaceship, (spaceship_x, spaceship_y))
            game_display.blit(healthBar, (5, 420))
            spaceshipRect = pygame.Rect(spaceship_x, spaceship_y+3, 120, 117)
        else:
            message("Game over, press Q to quit", grey, 25, 250, medium_font, game_display)
            enemyBulletState = "ready"
            bullet_state = "ready"

        # Enemy movement
        enemy_x += enemyXChange
        enemyRect = pygame.Rect(enemy_x-4, enemy_y+6, enemyXwidth, enemyYwidth)
       
        # Preventing the enemy from going off the screen
        if enemy_x > display_width-enemy_border:
            enemyXChange = -3
        if enemy_x < 1:
            enemyXChange = 3
        
        # How the enemy takes damage
        if bulletRect.colliderect(enemyRect):
            explosion = Explosion(enemy_x+EnemyMidPointX, enemy_y+EnemyMidPointY)
            explosion_group.add(explosion)
            enemyHP -= 1
            enemyHPCounter -= 1
            bulletY = 480
            bullet_state = "ready"            
        if EnemyStageCounter == 2:
            if enemyHPCounter == 4:
                enemyHealthBar = pygame.image.load("IMGS/HealthBar/12HP.png")
            if enemyHPCounter == 3:
                enemyHealthBar = pygame.image.load("IMGS/HealthBar/9HP.png")
            if enemyHPCounter == 2:
                enemyHealthBar = pygame.image.load("IMGS/HealthBar/6HP.png")
            if enemyHPCounter == 1:
                enemyHealthBar = pygame.image.load("IMGS/HealthBar/3HP.png")
            if enemyHPCounter == 0:
                enemyHealthBar = pygame.image.load("IMGS/HealthBar/0HP.png")
        if enemyHP == 0:
            EnemyStageCounter -= 1
            if EnemyStageCounter == 0:
                enemy = pygame.image.load("IMGS//S2Enemy.png")
                enemyBullet = pygame.image.load("IMGS/fatbullet.png")
                enemyDamage = 2
                bulletWidth = 30
                bulletLength = 60
                enemyHP = 15
                enemy_border=145
                enemyXwidth = 119
                enemyYwidth = 150
                EnemyMidPointX = 60
                EnemyMidPointY = 75
        if enemyHP == 10:
            enemy = pygame.image.load("IMGS/S2EnemyDamaged1.png")
        if enemyHP == 5:
            if EnemyStageCounter == 0:
                enemy = pygame.image.load("IMGS/S2EnemyDamaged2.png")
        if EnemyStageCounter == 0:
            enemyHealthBar = pygame.image.load("IMGS/HealthBar/{HP}HP.png".format(HP = str(enemyHP)))
        if enemyBulletRect.colliderect(spaceshipRect):
            enemyExplosion = Explosion(spaceship_x+60, spaceship_y)
            explosion_group.add(enemyExplosion)
            spaceship_health -= enemyDamage
            enemyBulletY = enemy_y
            enemyBulletState = "ready"
        if enemyHP > 0:
            game_display.blit(enemy, (enemy_x, enemy_y))
            game_display.blit(enemyHealthBar, (5, -30))
        if enemyHP <= 0:
            if EnemyStageCounter < -20:
                spaceship_health = 15 
                message("PLAYER WINS!!!", golden_yellow, 150, 220, large_font, game_display)
                message("Press Q to exit.", white, 200, 300, font, game_display)
                enemyBulletState = "ready"

        # Player health bar
        healthBar = pygame.image.load("IMGS/HealthBar/{a}HP.png".format(a = spaceship_health*1))


        # Updating Screen so changes take places
        pygame.display.flip()

        # Setting FPS
        FPS = pygame.time.Clock()
        FPS.tick(60)


# More colors
black = (0, 0, 0)
white = (255, 255, 255)
grey = (100, 100, 100)

# Creating Introduction screen
while True:
    intro_display.fill(black)
    pygame.event.poll()
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    message("Space Bugs", white, 180, 150, large_font, intro_display)
    if 250 > mouse[0] > 150 and 400 > mouse[1] > 350:
        pygame.draw.rect(intro_display, grey, [150, 350, 100, 50])
        if click[0] == 1:
            main()
    else:
        pygame.draw.rect(intro_display, white, [150, 350, 100, 50])

    if 550 > mouse[0] > 450 and 400 > mouse[1] > 350:
        pygame.draw.rect(intro_display, grey, [450, 350, 100, 50])
        if click[0] == 1:
            pygame.quit()
            sys.exit()
    else:
        pygame.draw.rect(intro_display, white, [450, 350, 100, 50])

    message("Start", black, 155, 360, font, intro_display)
    message("Quit", black, 465, 360, font, intro_display)

    # Updating screen so changes take place
    pygame.display.update()

    # Limit to 60 frames per second
    clock = pygame.time.Clock()
    clock.tick(60)


