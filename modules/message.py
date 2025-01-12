# Pygame
import pygame


def message(sentence, color, x, y, font_type, canvas):
    """
    Display text to a canvas in pygame.

    Args:
        sentence (str): text that needs to be displayed
        color (tuple): tuple containing RGB color values for the text
        x (int): X-coordinate of text's position
        y (int): Y-coordinate of text's position
        font_type (pygame.font.SysFont): System font object
        canvas ()
    """

    sentence = font_type.render(str.encode(sentence), True, color)
    canvas.blit(sentence, [x, y])
