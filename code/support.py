import pygame
from settings import *
from csv import reader
# from os import walk

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        layout = reader(map,delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((TILESIZE,TILESIZE))):
		super().__init__(groups)
		self.sprites_type = sprite_type
		self.image = pygame.transform.scale(surface,(16,16)).convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,0)

        
# def import_folder(path):
#     surface_list = []

#     for _,__,img_files in walk(path):
#         for image in img_files:
#             full_path = path + '/' + image
#             image_surf = pygame.image.load(full_path).convert_alpha()
#             surface_list.append(image_surf)
            
    # return surface_list
#print(import_csv_layout("../map/final2_player.csv"))