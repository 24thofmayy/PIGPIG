import pygame ,sys
from settings import *
import player

class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.image = pygame.Surface((50,10))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center + (pos_x,pos_y))
        self.bullet = pygame.sprite.group()

    def update(self):
        self.rect.x += 5
    def create_bullet(self):
        
        return Bullet(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])


   