# Pygame
import pygame

# Initializing fonts.
pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 30)
large_font = pygame.font.SysFont("Comic Sans MS", 60)
medium_font = pygame.font.SysFont("Comic Sans MS", 40)


# Function for writing text to the screen easily.
def message(sentence, color, x, y, font_type, display):
    sentence = font_type.render(str.encode(sentence), True, color)
    display.blit(sentence, [x, y])