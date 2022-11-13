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
		self.attack = False

		self.facing = 'down'
		self.animation_loop = 1

		self.image = pygame.transform.scale((self.game.character_spritesheet.get_sprite(0, 0, 16, 16)),(32,32))
		

		# rect is where the image in sprites positioned and sized 
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

	def update(self):
		self.movement()
		self.animate()
		self.collide_enemy()

		self.rect.x += self.x_change
		self.collide_blocks('x')
		self.rect.y += self.y_change
		self.collide_blocks('y')

		self.x_change = 0
		self.y_change = 0
		self.attack = False

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
		if keys[pygame.K_SPACE]:
			self.attack = True

	def collide_enemy(self):
		hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
		if hits:
			self.kill()
			self.game.playing = False

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

	def animate(self):
		down_animations = [pygame.transform.scale((self.game.character_spritesheet.get_sprite(0, 0, 16, 16)),(32,32)),
                           pygame.transform.scale((self.game.character_spritesheet.get_sprite(0, 16, 16, 16)),(32,32)),
                           pygame.transform.scale((self.game.character_spritesheet.get_sprite(0, 32, 16, 16)),(32,32)),
						   pygame.transform.scale((self.game.character_spritesheet.get_sprite(0, 48, 16, 16)),(32,32))]

		up_animations = [pygame.transform.scale((self.game.character_spritesheet.get_sprite(16, 0, 16, 16)),(32,32)),
                           pygame.transform.scale((self.game.character_spritesheet.get_sprite(16, 16, 16, 16)),(32,32)),
                           pygame.transform.scale((self.game.character_spritesheet.get_sprite(16, 32, 16, 16)),(32,32)),
						   pygame.transform.scale((self.game.character_spritesheet.get_sprite(16, 48, 16, 16)),(32,32))]

		left_animations = [pygame.transform.scale((self.game.character_spritesheet.get_sprite(32, 0, 16, 16)),(32,32)),
                           pygame.transform.scale((self.game.character_spritesheet.get_sprite(32, 16, 16, 16)),(32,32)),
                           pygame.transform.scale((self.game.character_spritesheet.get_sprite(32, 32, 16, 16)),(32,32)),
						   pygame.transform.scale((self.game.character_spritesheet.get_sprite(32, 48, 16, 16)),(32,32))]

		right_animations = [pygame.transform.scale((self.game.character_spritesheet.get_sprite(48, 0, 16, 16)),(32,32)),
                           pygame.transform.scale((self.game.character_spritesheet.get_sprite(48, 16, 16, 16)),(32,32)),
                           pygame.transform.scale((self.game.character_spritesheet.get_sprite(48, 32, 16, 16)),(32,32)),
						   pygame.transform.scale((self.game.character_spritesheet.get_sprite(48, 48, 16, 16)),(32,32))]

		down_attack = pygame.transform.scale((self.game.attack_spritesheet.get_sprite(0, 0, 16, 16)),(32,32))

		up_attack = pygame.transform.scale((self.game.attack_spritesheet.get_sprite(16, 0, 16, 16)),(32,32))

		left_attack = pygame.transform.scale((self.game.attack_spritesheet.get_sprite(32, 0, 16, 16)),(32,32))

		right_attack = pygame.transform.scale((self.game.attack_spritesheet.get_sprite(48, 0, 16, 16)),(32,32))
		
		
		if self.facing == "down":
			if self.y_change == 0 and self.attack == False:
				self.image = pygame.transform.scale((self.game.character_spritesheet.get_sprite(0, 0, 16, 16)),(32,32))
			elif self.attack == True:
				self.image = down_attack
			else:
				self.image = down_animations[math.floor(self.animation_loop)]
				# change animation every 10 frames
				self.animation_loop += 0.1
				if self.animation_loop >= 4:
					self.animation_loop = 1

		if self.facing == "up":
			if self.y_change == 0 and self.attack == False:
				self.image = pygame.transform.scale((self.game.character_spritesheet.get_sprite(16, 0, 16, 16)),(32,32))
			elif self.attack == True:
				self.image = up_attack
			else:
				self.image = up_animations[math.floor(self.animation_loop)]
				# change animation every 10 frames
				self.animation_loop += 0.1
				if self.animation_loop >= 4:
					self.animation_loop = 1	

		if self.facing == "left":
			if self.x_change == 0 and self.attack == False:
				self.image = pygame.transform.scale((self.game.character_spritesheet.get_sprite(32, 0, 16, 16)),(32,32))
			elif self.attack == True:
				self.image = left_attack
			else:
				self.image = left_animations[math.floor(self.animation_loop)]
				# change animation every 10 frames
				self.animation_loop += 0.1
				if self.animation_loop >= 4:
					self.animation_loop = 1

		if self.facing == "right":
			if self.x_change == 0 and self.attack == False:
				self.image = pygame.transform.scale((self.game.character_spritesheet.get_sprite(48, 0, 16, 16)),(32,32))
			elif self.attack == True:
				self.image = right_attack
			else:
				self.image = right_animations[math.floor(self.animation_loop)]
				# change animation every 10 frames
				self.animation_loop += 0.1
				if self.animation_loop >= 4:
					self.animation_loop = 1	
class Enemy(pygame.sprite.Sprite):
	def __init__(self, game, x, y):

		self.game = game
		self._layer = ENEMY_LAYER
		self.groups = self.game.all_sprites, self.game.enemies
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.x = x * TILESIZE
		self.y = y * TILESIZE
		self.width = TILESIZE
		self.height = TILESIZE

		self.x_change = 0
		self.y_change = 0
		self.facing = random.choice(['left','right'])
		self.animation_loop = 1
		self.movement_loop = 0
		self.max_travel = random.randint(7, 30)

		self.image = pygame.transform.scale((self.game.enemy_spritesheet.get_sprite(0, 0, 16, 16)),(32,32))
		self.image.set_colorkey(BLACK)

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

	def update(self):
		self.movement()
		self.animate()

		self.rect.x += self.x_change
		self.rect.y += self.y_change

		self.x_change = 0
		self.y_change = 0

	def movement(self):
		if self.facing == 'left': 
			self.x_change -= ENEMY_SPEED
			self.movement_loop -= 1
			if self.movement_loop <= -self.max_travel:
				self.facing = 'right'
		
		if self.facing == 'right':
			self.x_change += ENEMY_SPEED
			self.movement_loop += 1
			if self.movement_loop >= self.max_travel:
				self.facing = 'left'
	
	def animate(self):
		down_animations = [pygame.transform.scale((self.game.enemy_spritesheet.get_sprite(0, 0, 16, 16)),(32,32)),
                           pygame.transform.scale((self.game.enemy_spritesheet.get_sprite(0, 16, 16, 16)),(32,32)),
                           pygame.transform.scale((self.game.enemy_spritesheet.get_sprite(0, 32, 16, 16)),(32,32)),
						   pygame.transform.scale((self.game.enemy_spritesheet.get_sprite(0, 48, 16, 16)),(32,32))]

		up_animations = [pygame.transform.scale((self.game.enemy_spritesheet.get_sprite(16, 0, 16, 16)),(32,32)),
                           pygame.transform.scale((self.game.enemy_spritesheet.get_sprite(16, 16, 16, 16)),(32,32)),
                           pygame.transform.scale((self.game.enemy_spritesheet.get_sprite(16, 32, 16, 16)),(32,32)),
						   pygame.transform.scale((self.game.enemy_spritesheet.get_sprite(16, 48, 16, 16)),(32,32))]

		left_animations = [pygame.transform.scale((self.game.enemy_spritesheet.get_sprite(32, 0, 16, 16)),(32,32)),
                           pygame.transform.scale((self.game.enemy_spritesheet.get_sprite(32, 16, 16, 16)),(32,32)),
                           pygame.transform.scale((self.game.enemy_spritesheet.get_sprite(32, 32, 16, 16)),(32,32)),
						   pygame.transform.scale((self.game.enemy_spritesheet.get_sprite(32, 48, 16, 16)),(32,32))]

		right_animations = [pygame.transform.scale((self.game.enemy_spritesheet.get_sprite(48, 0, 16, 16)),(32,32)),
                           pygame.transform.scale((self.game.enemy_spritesheet.get_sprite(48, 16, 16, 16)),(32,32)),
                           pygame.transform.scale((self.game.enemy_spritesheet.get_sprite(48, 32, 16, 16)),(32,32)),
						   pygame.transform.scale((self.game.enemy_spritesheet.get_sprite(48, 48, 16, 16)),(32,32))]

		if self.facing == "down":
			if self.y_change == 0:
				self.image = pygame.transform.scale((self.game.enemy_spritesheet.get_sprite(0, 0, 16, 16)),(32,32))
			else:
				self.image = down_animations[math.floor(self.animation_loop)]
				# change animation every 10 frames
				self.animation_loop += 0.1
				if self.animation_loop >= 4:
					self.animation_loop = 1

		if self.facing == "up":
			if self.y_change == 0:
				self.image = pygame.transform.scale((self.game.enemy_spritesheet.get_sprite(16, 0, 16, 16)),(32,32))
			else:
				self.image = up_animations[math.floor(self.animation_loop)]
				# change animation every 10 frames
				self.animation_loop += 0.1
				if self.animation_loop >= 4:
					self.animation_loop = 1	

		if self.facing == "left":
			if self.x_change == 0:
				self.image = pygame.transform.scale((self.game.enemy_spritesheet.get_sprite(32, 0, 16, 16)),(32,32))
			else:
				self.image = left_animations[math.floor(self.animation_loop)]
				# change animation every 10 frames
				self.animation_loop += 0.1
				if self.animation_loop >= 4:
					self.animation_loop = 1

		if self.facing == "right":
			if self.x_change == 0:
				self.image = pygame.transform.scale((self.game.enemy_spritesheet.get_sprite(48, 0, 16, 16)),(32,32))
			else:
				self.image = right_animations[math.floor(self.animation_loop)]
				# change animation every 10 frames
				self.animation_loop += 0.1
				if self.animation_loop >= 4:
					self.animation_loop = 1	

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

class Button:
	def __init__(self, x, y, width, height, fg, bg, content, fontsize):
		self.font = pygame.font.Font('../assets/NormalFont.ttf', fontsize)
		self.content = content

		self.x = x
		self.y =y
		self.width = width
		self.height = height

		self.fg = fg
		self.bg = bg

		self.image = pygame.Surface((self.width, self.height))
		self.image.fill(self.bg)
		self.rect = self.image.get_rect()

		self.rect.x = self.x
		self.rect.y = self.y

		self.text = self.font.render(self.content, True, self.fg)
		self.text_rect = self.text.get_rect(center = (self.width/2, self.height/2))
		self.image.blit(self.text, self.text_rect)
	
	def is_pressed(self, pos, pressed):
		if self.rect.collidepoint(pos):
			if pressed[0]:
				return True
			return False
		return False

class Attack(pygame.sprite.Sprite):

	def __init__(self, game, x, y):

		self.game = game
		self._layer = PLAYER_LAYER
		self.groups = self.game.all_sprites, self.game.spark
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.x = x
		self.y = y
		self.width = 48
		self.height = 48

		self.animation_loop =  0

		self.image = pygame.transform.scale((self.game.spark_spritesheet.get_sprite(0, 0, 32, 32)),(self.width,self.height))

		self.rect = self.image.get_rect()
		self.rect.x =self.x
		self.rect.y = self.y

	def update(self):
		self.animate()
		self.collide()

	def collide(self):
		hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

	def animate(self):
		#direction = self.game.player.facing
		spark_animations = [pygame.transform.scale((self.game.spark_spritesheet.get_sprite(0, 0, 32, 32)),(self.width,self.height)),
                           pygame.transform.scale((self.game.spark_spritesheet.get_sprite(32, 0, 32, 32)),(self.width,self.height)),
                           pygame.transform.scale((self.game.spark_spritesheet.get_sprite(64, 0, 32, 32)),(self.width,self.height)),
						   pygame.transform.scale((self.game.spark_spritesheet.get_sprite(96, 0, 32, 32)),(self.width,self.height))]

		self.image = spark_animations[math.floor(self.animation_loop)]
		self.animation_loop += 0.25
		if self.animation_loop >= 4:
			self.kill()
