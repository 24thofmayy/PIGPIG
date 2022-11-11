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
		#self.font = pygame.font.Font('Arial',32)
		self.running = True
		self.character_spritesheet = Spritesheet('../assets/graphic/test/RedSamurai/redsamurai.png')
		self.terrain_spritesheet = Spritesheet("../assets/graphic/Backgrounds/Tilesets/TilesetFloor.png")
		self.object_spritesheet = Spritesheet("../assets/graphic/Backgrounds/Tilesets/TilesetNature.png")

		pygame.display.set_caption('PIG KILLER')	
	
	def createTilemap(self):
		for i, row in enumerate(tilemap):
			for j, column in enumerate(row):
				Ground(self, j, i)
				if column == "B":
					Block(self, j, i)
				if column == "P":
					Player(self, j, i)

	def new(self):
		# start new game
		self.playing = True

		# contain all sprites in game
		self.all_sprites = pygame.sprite.LayeredUpdates()
		self.blocks = pygame.sprite.LayeredUpdates()
		self.enemie = pygame.sprite.LayeredUpdates()
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
		pass

g = Game()
g.intro_screen()
g.new()
while g.running:
	g.main()
	g.game_over()

pygame.quit()
sys.exit()