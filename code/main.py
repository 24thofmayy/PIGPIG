import pygame, sys
from settings import *
from level import Level
blue = 18, 78, 137  

class Game:
	def __init__(self):
		  
		# general setup
		pygame.init()
		
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('PIG KILLER')
		self.clock = pygame.time.Clock()
		self.level = Level()
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()	
			self.screen.fill(blue)
			self.level.run()
			#self.player.update()
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()