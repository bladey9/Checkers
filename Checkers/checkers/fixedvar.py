import pygame


surface = pygame.Surface((100,100))
surface.set_alpha(100)

width = 800
height = 800
rows = 8
columns = 8

# King Image
king = pygame.transform.scale(pygame.image.load("assets/king.png"), (35, 25))
white_winner = pygame.transform.scale(pygame.image.load("assets/whitehaswon.png"),(800,500))
black_winner = pygame.transform.scale(pygame.image.load("assets/blackhaswon.png"),(800,500))

# Colour codes for UI
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
brown = (222, 188, 153)
light_brown = (200, 208, 168)
dark_brown = (101, 67, 33)
grey = (128, 128, 128)

surface.fill(white)
space = int(width / columns)