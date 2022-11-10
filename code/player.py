import pygame 
from settings import *
from support import import_folder

class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.image = pygame.Surface((50,10))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center = (pos_x,pos_y))
        self.bullet = pygame.sprite.Group()

    def update(self):
        self.rect.x += 5

	
class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups,obstacle_sprites):
		super().__init__(groups)
		self.image = pygame.transform.scale(pygame.image.load('C:\\Users\\Acer\\OneDrive\\Desktop\\patt\\uni\\y1\\profun\\Game project\\01 - level\\1 - level\\graphics\\test\\player.png').convert_alpha(),(32,32))
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,0)

		#graphic setup
		self.import_player_assets()
		self.status = 'r'
		self.frame_index = 0
		self.animation_speed = 0.15

		# movement
		self.direction = pygame.math.Vector2()
		self.speed = 5
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = None
		self.obstacle_sprites = obstacle_sprites
	
	def create_bullet(self):
		return Bullet(self.hitbox.x,self.hitbox.y)

	def import_player_assets(self):
		character_path = 'C:\\Users\\Acer\\OneDrive\\Desktop\\patt\\uni\\y1\\profun\\Game project\\assets\\graphic\\player\\'
		self.animations = {'l':[],'l_attack':[],'l_idle':[],'r':[],'r_attack':[],'r_idle':[],'u':[],'u_attack':[],'u_idle':[],'d':[],'d_attack':[],'d_idle':[]}
		for animation in self.animations.keys():
			full_path = character_path + animation
			# animation = pygame.transform.scale(animation,(32,32))
			self.animations[animation] = import_folder(full_path) 

	def input(self):
		
		keys = pygame.key.get_pressed()
		mouse = pygame.mouse.get_pressed()
		#movement input
		if keys[pygame.K_w]:
			self.direction.y = -1
			self.status = 'u'
		elif keys[pygame.K_s]:
			self.direction.y = 1
			self.status = 'd'
		else:
			self.direction.y = 0

		if keys[pygame.K_d]:
			self.direction.x = 1
			self.status = 'r'
		elif keys[pygame.K_a]:
			self.direction.x = -1
			self.status = 'l'
		else:
			self.direction.x = 0

		#attack1 input
		if keys[pygame.K_SPACE] and not self.attacking:
			self.attacking = True
			self.attack_time = pygame.time.get_ticks()
			print('attack')
			# magic input 
		if mouse[0] and not self.attacking:
			self.attacking = True
			self.attack_time = pygame.time.get_ticks()
			print('magic')

	def get_status(self):

		# idle status
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'

		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle','_attack')
				else:
					self.status = self.status + '_attack'
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack','')

	def move(self,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center
		
	def collision(self,direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0: # moving right
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0: # moving left
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom
	def cooldowns(self):
		current_time = pygame.time.get_ticks()

		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.attacking = False

	def animate(self):
		animation = self.animations[self.status]

		# loop over the frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		# set the image
		self.image = pygame.transform.scale(animation[int(self.frame_index)],(150,150))
		self.rect = self.image.get_rect(center = self.hitbox.center)


	def update(self):
		self.rect.center = pygame.mouse.get_pos()
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move(self.speed)




