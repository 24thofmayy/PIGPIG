import pygame, sys
from level import *
from sprites import *
from settings import *
from support import *
from score import ScoreInput

class Game:
	def __init__(self):  
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH)) 
		self.clock = pygame.time.Clock()
		self.running = True
		self.title_font = pygame.font.Font('../assets/NormalFont.ttf', 32)
		self.small_font = pygame.font.Font('../assets/NormalFont.ttf', 18)

		self.character_spritesheet = Spritesheet('../assets/graphic/test/RedSamurai/redsamurai.png')
		self.attack_spritesheet = Spritesheet('../assets/graphic/test/RedSamurai/Attack.png')
		self.spark_spritesheet = Spritesheet('../assets/graphic/particles/spark.png')
		self.terrain_spritesheet = Spritesheet("../assets/graphic/Backgrounds/Tilesets/TilesetFloor.png")
		self.object_spritesheet = Spritesheet("../assets/graphic/Backgrounds/Tilesets/TilesetNature.png")
		self.enemy_spritesheet = Spritesheet('../assets/graphic/test/Octopus2/SpriteSheet.png')
		
		self.intro_background = pygame.transform.scale(pygame.image.load('../assets/graphic/Backgrounds/menu.png'),(WIDTH,HEIGTH))
		self.gameover_bg = pygame.transform.scale(pygame.image.load('../assets/graphic/Backgrounds/gameover.png'),(WIDTH,HEIGTH))
		self.heart_pic = pygame.image.load('../assets/graphic/particles/fruit_01a.png')
		
		self.gameoversound = pygame.mixer.Sound("../assets/sound/lose.mp3")
		self.gameoversound.set_volume(1)
		self.winsound = pygame.mixer.Sound("../assets/sound/win.mp3")
		self.winsound.set_volume(1)
		self.bgsound = pygame.mixer.Sound("../assets/sound/backgroung.mp3")
		self.bgsound.set_volume(1)

		self.scores = []
		self.rankscores = []

		pygame.display.set_caption('SQUID GAME')	
	
	def createTilemap(self):
		Ground(self, -6, -7)
		num = 0
		num2 = 0
		#self.player = Player(self, 10, 7)

		layouts = {
			'object' : import_csv_layout('../map/final2_object.csv'),
			'Player' : import_csv_layout('../map/final2_player.csv'),
			'Pig' : import_csv_layout('../map/final2_pig.csv'),
			'border' :import_csv_layout('../map/final2_border.csv'),
			'monster' :import_csv_layout('../map/final2_monster.csv'),
			'item' :import_csv_layout('../map/final2_item.csv')
		}
		for stlye,layout in layouts.items(): 
			for i, row in enumerate(layout):
				for j, column in enumerate(row):
					if column != "-1":
						if stlye == "Pig":
							Enemy(self, j-6, i-7)
						elif stlye == 'monster':
							Monster(self, j-6, i-7)
						elif stlye == 'item':
							Item(self, j-6, i-7)	
						elif stlye == "Player":
							self.player = Player(self, j-6, i-7)
						elif stlye == "border" or  stlye == "object":
							Block(self, j-6, i-7)

	def new(self):
		# start new game
		self.playing = True
		self.score = 0
		self.hp = 1000
		self.pig = 0

		# contain all sprites in game
		self.all_sprites = pygame.sprite.LayeredUpdates()
		self.blocks = pygame.sprite.LayeredUpdates()
		self.enemies = pygame.sprite.LayeredUpdates()
		self.monster = pygame.sprite.LayeredUpdates()
		self.spark = pygame.sprite.LayeredUpdates()
		self.item = pygame.sprite.LayeredUpdates() 
		self.createTilemap()

	def events(self):
		# game loop events
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.playing = False
					self.running = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						if self.player.facing == 'up':
							Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
						if self.player.facing == 'down':
							Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
						if self.player.facing == 'left':
							Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
						if self.player.facing == 'right':
							Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)
					if event.key == pygame.K_ESCAPE:
						#self.kill()
						self.playing = False
						self.game_over()


	def update(self):
		# game loop update
		# find the update method in every sprites in that group and run it
		self.all_sprites.update()
		
	def draw(self):
		self.screen.fill(BLUE)
		#draw all sprites in the group onto the screen
		self.all_sprites.draw(self.screen)
		score = self.small_font.render('SCORE : '+ str(self.score), True, BLACK)
		score_rect = score.get_rect(x=5, y=40)
		
		hp = self.small_font.render('HP : '+ str(int(self.hp/10)), True, BLACK)
		hp_rect = hp.get_rect(x=5, y=20)

		squid = self.small_font.render('SQUID     KILLED : ' + str(self.pig)+ '/30', True, RED )
		squid_rect = squid.get_rect(x=5, y=0)

		self.screen.blit(score, score_rect)
		self.screen.blit(hp, hp_rect)
		self.screen.blit(squid, squid_rect)


		# FPS = frames per sec (how many time to update the screen per sec )
		self.clock.tick(FPS)
		pygame.display.update()

	def main(self):
		# game loop
		while self.playing:
			self.events()
			self.update()
			self.draw()

	def game_over(self):
		self.gameover = True
		user_ip = ''

		back_button = Button(WIDTH/2+100,HEIGTH/2+150, 150, 50 , WHITE, BLACK, 'CONFIRM', 26)

		text = self.title_font.render('GAME OVER', True, WHITE)
		text_rect = text.get_rect(center=(WIDTH/2,HEIGTH/2-100))

		name = self.title_font.render('ENTER YOUR NAME: ', True, WHITE)
		name_rect = name.get_rect(center=(WIDTH/2,HEIGTH/2))

		score = self.title_font.render('YOUR SCORE    IS    '+ str(self.score) , True, RED)
		score_rect = score.get_rect(center=(WIDTH/2,HEIGTH/2-50))

		win = self.title_font.render('! YOU WIN !', True, WHITE)
		win_rect = win.get_rect(center=(WIDTH/2,HEIGTH/2-100))

		restart_button = Button(10, HEIGTH-60, 120, 50 , WHITE, BLACK, 'RESTART', 16)
		

		for sprite in self.all_sprites:
			sprite.kill()

		while self.gameover:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					self.gameover = False
				
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_BACKSPACE:
						user_ip = user_ip[:-1]
					else:
						user_ip += event.unicode
				
				mouse_pos = pygame.mouse.get_pos()
				mouse_pressed = pygame.mouse.get_pressed()
				
				if back_button.is_pressed(mouse_pos,mouse_pressed):
					self.gameover = False
					file = open('score.txt', 'a')
					file.write(f'{user_ip}, {self.score}\n')
					file.flush()
					file.close()
					self.intro_screen()
				
				if restart_button.is_pressed(mouse_pos, mouse_pressed):
					self.gameover = False
					self.new()
					self.main()

			self.screen.fill((0,0,0))
			
			if self.pig >= 30:
				self.screen.blit(win, win_rect)
				self.screen.blit(score, score_rect)
				pygame.mixer.Sound.play(self.winsound)

			else:
				self.screen.blit(score, score_rect)
				self.screen.blit(text, text_rect)
				pygame.mixer.Sound.play(self.gameoversound)

			
			username = self.title_font.render(user_ip, True, WHITE)
			user_rect = username.get_rect(center=(WIDTH/2,HEIGTH/2+50))
			self.screen.blit(username, user_rect)
			self.screen.blit(back_button.image, back_button.rect)
			self.screen.blit(name, name_rect)
			
			self.screen.blit(restart_button.image, restart_button.rect)
			self.clock.tick(FPS)
			pygame.display.update()
		
	def intro_screen(self):
		self.show = 0
		self.intro = True

		title = self.title_font.render('SQUID    GAME', True, WHITE)
		title_rect = title.get_rect(x=195, y=80)

		name = self.small_font.render('65010727  patthanan     chualam', True, WHITE)
		name_rect = name.get_rect(x=180, y=440)

		play_button = Button(260, 230, 100, 30, WHITE,BLACK, 'PLAY', 26)
		high_score_button = Button(210, 290, 200, 30 , WHITE, BLACK, 'HIGH SCORE', 26)

		while self.intro:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.intro = False
					self.running = False

			mouse_pos = pygame.mouse.get_pos()
			mouse_pressed = pygame.mouse.get_pressed()

			if play_button.is_pressed(mouse_pos,mouse_pressed):
				self.intro = False
				self.new()
				self.main()
				
			if high_score_button.is_pressed(mouse_pos,mouse_pressed):
				self.intro = False
				self.high_score()


			self.screen.blit(self.intro_background, (0,0))
			self.screen.blit(title, title_rect)
			self.screen.blit(name, name_rect)
			self.screen.blit(play_button.image, play_button.rect)
			self.screen.blit(high_score_button.image, high_score_button.rect)
			
			self.clock.tick(FPS)
			pygame.display.update()

	def high_score(self):
		self.highscore = True
		text = self.title_font.render('HIGH SCORE', True, RED)
		text_rect = text.get_rect(center=(WIDTH/2,HEIGTH/2-150))

		back_button = Button(10, HEIGTH-60, 120, 50 , WHITE, BLACK, 'GO BACK', 26)

		while self.highscore:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.highscore = False
					self.running = False

			mouse_pos = pygame.mouse.get_pos()
			mouse_pressed = pygame.mouse.get_pressed()

			if back_button.is_pressed(mouse_pos, mouse_pressed):
				self.highscore = False
				self.intro_screen()
		
			#self.screen.fill(WHITE)
			self.display_rank()
			self.screen.blit(text, text_rect)
			self.screen.blit(back_button.image, back_button.rect)
			
			self.clock.tick(FPS)
			pygame.display.update()

	def draw_text_rank(self,text, color, size, screen, pos):
		font = pygame.font.Font('../assets/NormalFont.ttf', size)
		textobj = font.render(text, False, color)
		textrect = textobj.get_rect(midleft = pos)
		screen.blit(textobj, textrect)

	def ranking(self):
		if self.show != 1:
			self.rankscores = []
			self.scores = []
			with open('score.txt') as file:
				for line in file:
					name, score = line.split(',')
					score = int(score)
					self.scores.append((name, score))
				self.scores.sort(key=lambda s: s[1])
				self.scores.reverse()
				for num in range(0, 5):
					self.rankscores.insert(num,self.scores[num])
				file.flush()
				print(self.scores)
				self.show = 1
			

	def display_rank(self):
		self.ranking()
		screen = pygame.display.set_mode((WIDTH,HEIGTH)) 
		space = 0
		for i in range(0, 5):
			self.draw_text_rank(f'{self.rankscores[i][0]}', WHITE, 20, screen, (WIDTH / 2 - 200, 180 + space))
			space += 50

		space = 0
		for i in range(0, 5):
			self.draw_text_rank(f'{self.rankscores[i][1]}', WHITE, 20, screen, (WIDTH / 2 + 100, 180 + space))
			space += 50
		
g = Game()  
g.intro_screen()
#g.draw_name()
g.new()
while g.running:
	g.main()
	g.game_over()

pygame.quit()
sys.exit()