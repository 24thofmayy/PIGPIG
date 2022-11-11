import pygame
from settings import *
import math 
import random

# by pasting 'game' here we'll be able to access all the variable in 'Game'
# 'x' 'y' to set where the player appear on the screen
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

		self.image = pygame.Surface([self.width,self.height])
		self.image.fill(RED)

		# rect is where the image im sprites positioned and sized 
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

	def update(self):
		self.movement()

		self.rect.x += self.x_change
		self.rect.y += self.y_change

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
		
		
