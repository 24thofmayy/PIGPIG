import pygame
# game setup
verical_tile_number = 120
TILESIZE = 32

WIDTH    = 640
HEIGTH   = 480
center = ((WIDTH/2),(HEIGTH/2))
FPS      = 60

PLAYER_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1 

PLAYER_SPEED = 2

RED = (255, 0, 0,)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

tilemap = [
    'BBBBBBBBBBBBBBBBBBBB',
    'B..................B',
    'B..................B',
    'B....BBB...........B',
    'B..................B',
    'B..................B',
    'B.........P........B',
    'B..................B',
    'B..................B',
    'B..........BBBB....B',
    'B.............B....B',
    'B.............B....B',
    'B..................B',
    'B..................B',
    'BBBBBBBBBBBBBBBBBBBB'



]
screen = pygame.display.set_mode((WIDTH,HEIGTH))
#weapon data
weapon_data = {
    'Gun'  : {'cooldown' : 100, 'damage' : 20}
}
