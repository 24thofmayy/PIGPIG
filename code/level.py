import pygame
from support import *
from settings import *
from tile import Tile
from player import Player,Bullet
from debug import debug
map_wide = 1920
map_high = 1920
class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()
		self.bullets_sprites = pygame.sprite.Group()

		# sprite setup
		self.create_map()

	def create_map(self):
		layouts = {
			'boundary': import_csv_layout("C:\\Users\\Acer\\OneDrive\\Desktop\\patt\\uni\\y1\\profun\\Game project\\map\\final_border.csv"),
			'object': import_csv_layout("C:\\Users\\Acer\\OneDrive\\Desktop\\patt\\uni\\y1\\profun\\Game project\\map\\final_forest rocrk.csv"),			
		}
		
		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						#if style == 'boundary':
						Tile((x,y),[ self.obstacle_sprites],'invisible')
						
		self.player = Player((850,850),[self.visible_sprites],self.obstacle_sprites)
	def run(self):
		# update and draw the game
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		self.obstacle_sprites.update()
		
		debug(self.player.status)

class YSortCameraGroup(pygame.sprite.Group):

	def __init__(self):

		# general setup 
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()
		
		#creating the floor
		
		self.floor_surface = pygame.transform.scale(pygame.image.load('C:\\Users\\Acer\\OneDrive\\Desktop\\patt\\uni\\y1\\profun\\Game project\\map\\final.png').convert(), (map_wide,map_high))
		self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))
	def center_target_camera(self,target):
		self.offset.x = target.rect.centerx - self.half_w
		self.offset.y = target.rect.centery - self.half_h


	def custom_draw(self,player):

		# getting the offset 
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		#drawing the floor
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surface,floor_offset_pos)

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)

		#pygame.draw.rect(self.display_surface,'yellow',self.camera_rect,5)
	