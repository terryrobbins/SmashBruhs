import pygame as pg

#game options
TITLE = "Smash Bruh"
screenWidth = 576
screenHeight = 288
FPS = 60

#Player Variables
p_acc = 0.5
p_fric = -(0.12)


# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0,50)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 69, 0)
BGCOLOR = (255,174,201)

#loads sprites
bg = pg.image.load('backgrounds/scene1.png')

