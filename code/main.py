import pygame, sys
from level import *
from sprites import *
from settings import *
  

class Game:
	def __init__(self):  
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		self.clock = pygame.time.Clock()
		self.running = True
		self.font = pygame.font.Font('../assets/Mario-Kart-DS.ttf', 32)

		self.character_spritesheet = Spritesheet('../assets/graphic/test/RedSamurai/redsamurai.png')
		self.terrain_spritesheet = Spritesheet("../assets/graphic/Backgrounds/Tilesets/TilesetFloor.png")
		self.object_spritesheet = Spritesheet("../assets/graphic/Backgrounds/Tilesets/TilesetNature.png")
		self.enemy_spritesheet = Spritesheet('../assets/graphic/test/Octopus2/SpriteSheet.png')
		self.intro_background = pygame.transform.scale(pygame.image.load('../assets/graphic/Backgrounds/menu.png'),(WIDTH,HEIGTH))

		pygame.display.set_caption('PIG KILLER')	
	
	def createTilemap(self):
		for i, row in enumerate(tilemap):
			for j, column in enumerate(row):
				Ground(self, j, i)
				if column == "B":
					Block(self, j, i)
				if column == "E":
					Enemy(self, j, i)
				if column == "P":
					Player(self, j, i)

	def new(self):
		# start new game
		self.playing = True

		# contain all sprites in game
		self.all_sprites = pygame.sprite.LayeredUpdates()
		self.blocks = pygame.sprite.LayeredUpdates()
		self.enemies = pygame.sprite.LayeredUpdates()
		self.attack = pygame.sprite.LayeredUpdates()

		self.createTilemap()

	def events(self):
		# game loop events
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.playing = False
					self.running = False

	def update(self):
		# game loop update
		# find the update method in every sprites in that group and run it
		self.all_sprites.update()
	
	def draw(self):
		self.screen.fill(BLACK)
		#draw all sprites in the group onto the screen
		self.all_sprites.draw(self.screen)
		# FPS = frames per sec (how many time to update the screen per sec )
		self.clock.tick(FPS)
		pygame.display.update()

	def main(self):
		# game loop
		while self.playing:
			self.events()
			self.update()
			self.draw()
		self.running = False

	def game_over(self):
		pass
	
	def intro_screen(self):
		intro = True

		title = self.font.render('SQUID KILLER !!', True, WHITE)
		title_rect = title.get_rect(x=190, y=180)

		play_button = Button(260, 280, 100, 30, WHITE,BLACK, 'PLAY', 26)
		while intro:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					intro = False
					self.running = False

			mouse_pos = pygame.mouse.get_pos()
			mouse_pressed = pygame.mouse.get_pressed()

			if play_button.is_pressed(mouse_pos,mouse_pressed):
				intro = False

			self.screen.blit(self.intro_background, (0,0))
			self.screen.blit(title, title_rect)
			self.screen.blit(play_button.image, play_button.rect)
			self.clock.tick(FPS)
			pygame.display.update()

g = Game()
g.intro_screen()
g.new()
while g.running:
	g.main()
	g.game_over()

pygame.quit()
sys.exit()