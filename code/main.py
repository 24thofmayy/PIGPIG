import pygame, sys
from level import *
from player import *
from settings import *
blue = 18, 78, 137  

class Game:
	def __init__(self):  
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		self.clock = pygame.time.Clock()
		#self.font = pygame.font.Font('Arial',32)
		self.running = True
		pygame.display.set_caption('PIG KILLER')	
	
	def new(self):
		# start new game
		self.playing = True

		# contain all sprites in game
		self.all_sprites = pygame.sprite.LayeredUpdates()
		self.blocks = pygame.sprite.LayeredUpdates()
		self.enemie = pygame.sprite.LayeredUpdates()
		self.attack = pygame.sprite.LayeredUpdates()

		self.player = Player(self, 1, 2)
	def events(self):
		# game loop events
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.playing = False
					self.running = False
			# 		pygame.quit()
			# 		sys.exit()	
			# self.screen.fill(blue)
			# pygame.display.update()
			# self.clock.tick(FPS)
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
# if __name__ == '__main__':
# 	game = Game()
# 	game.run()