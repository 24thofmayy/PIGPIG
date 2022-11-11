import pygame
from support import *
from settings import *
from tile import Tile

class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprite group
		self.obstacle_sprites = pygame.sprite.Group()

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
						Tile((x,y),[ self.obstacle_sprites],'invisible')
	