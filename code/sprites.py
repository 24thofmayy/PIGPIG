import pygame
from settings import *
import math 
import random

# by pasting 'game' here we'll be able to access all the variable in 'Game'
# 'x' 'y' to set where the player appear on the screen
class Spritesheet:
	def __init__(self, file):
		self.sheet = pygame.image.load(file).convert()
		
	# cut the sprite sheet
	def get_sprite(self, x, y, width, height):
		sprite = pygame.Surface([width, height])
		sprite.blit(self.sheet, (0,0), (x, y, width, height))
		sprite.set_colorkey(BLACK)
		return sprite

class Player(pygame.sprite.Sprite):
	def __init__(self, game, x, y):

		self.game = game
		self._layer = PLAYER_LAYER

		# adding the player into all_sprites group 
		self.groups = self.game.all_sprites
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.x = x * TILESIZE
		self.y = y * TILESIZE
		self.width = TILESIZE
		self.height = TILESIZE

		self.x_change = 0
		self.y_change = 0

		self.facing = 'down'

		self.image = self.game.character_spritesheet.get_sprite(0, 0, 16, 16)
		self.image = pygame.transform.scale((self.image),(32,32))

		# rect is where the image in sprites positioned and sized 
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

	def update(self):
		self.movement()

		self.rect.x += self.x_change
		self.collide_blocks('x')
		self.rect.y += self.y_change
		self.collide_blocks('y')

		self.x_change = 0
		self.y_change = 0

	def movement(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a]:
			self.x_change -= PLAYER_SPEED
			self.facing = 'left'
		if keys[pygame.K_d]:
			self.x_change += PLAYER_SPEED
			self.facing = 'right'
		if keys[pygame.K_w]:
			self.y_change -= PLAYER_SPEED
			self.facing = 'up'
		if keys[pygame.K_s]:
			self.y_change += PLAYER_SPEED
			self.facing = 'down'	

	def collide_blocks(self, direction):
		if direction == "x":
			# check if the sprite ซ้อนกัน
			hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
			if hits:
				if self.x_change > 0:
					self.rect.x = hits[0].rect.left - self.rect.width
				if self.x_change < 0:
					self.rect.x = hits[0].rect.right 

		if direction == "y":
			hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
			if hits:
				if self.y_change > 0:
					self.rect.y = hits[0].rect.top - self.rect.height
				
				if self.y_change < 0:
					self.rect.y = hits[0].rect.bottom

class Block(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		
		self.game = game
		self._layer = BLOCK_LAYER
		self.groups = self.game.all_sprites, self.game.blocks
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.x = x * TILESIZE
		self.y = y * TILESIZE
		self.width = TILESIZE
		self.height = TILESIZE

		self.image = self.game.object_spritesheet.get_sprite(32, 0, 32, 32)
		self.image = pygame.transform.scale((self.image),(32,32))

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		self.game = game
		self._layer = GROUND_LAYER
		self.groups = self.game.all_sprites
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.x = x * TILESIZE
		self.y = y * TILESIZE
		self.width = TILESIZE
		self.height = TILESIZE

		self.image = self.game.terrain_spritesheet.get_sprite(32, 176, self.width, self.height)
		self.image = pygame.transform.scale((self.image),(32,32))

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

