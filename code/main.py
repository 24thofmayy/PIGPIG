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
							num += 1
							print('Pig = ' + str(num))
						elif stlye == 'monster':
							Monster(self, j-6, i-7)
							num2 += 1
							print('Mon = ' + str(num2))
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

		text_box = pygame.Rect((WIDTH/2 - 350/2, HEIGTH/2 - 20), (350, 50))
		text_surface = self.title_font.render(user_ip, True, (0, 0, 0))

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
			if self.hp <= 0:
				self.screen.blit(score, score_rect)
				self.screen.blit(text, text_rect)
				pygame.mixer.Sound.play(self.gameoversound)

			if self.pig >= 30:
				self.screen.blit(win, win_rect)
				self.screen.blit(score, score_rect)
				pygame.mixer.Sound.play(self.winsound)
			
			username = self.title_font.render(user_ip, True, WHITE)
			user_rect = username.get_rect(center=(WIDTH/2,HEIGTH/2+50))
			self.screen.blit(username, user_rect)
			self.screen.blit(back_button.image, back_button.rect)
			self.screen.blit(name, name_rect)
			
			self.screen.blit(restart_button.image, restart_button.rect)
			self.clock.tick(FPS)
			pygame.display.update()
		
	def intro_screen(self):
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
		text = self.title_font.render('HIGH SCORE', True, WHITE)
		text_rect = text.get_rect(center=(WIDTH/2,HEIGTH/2))

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
			
			self.screen.blit(self.gameover_bg, (0,0))
			self.screen.blit(text, text_rect)
			self.screen.blit(back_button.image, back_button.rect)
			#self.run()
			self.clock.tick(FPS)
			pygame.display.update()
	
	# def draw_name(self):
	# 	self.drawname = True
		
	# 	back_button = Button(10, HEIGTH-60, 120, 50 , WHITE, BLACK, 'GO BACK', 26)

	# 	while self.drawname:
	# 		for event in pygame.event.get():
	# 			if event.type == pygame.QUIT:
	# 				self.drawname = False
	# 				self.running = False
	# 			if event.type == pygame.KEYDOWN:
	# 				if event.key == pygame.K_BACKSPACE:
	# 					self.player_name = self.player_name[:-1]
	# 				elif len(self.player_name) <= 20 and event.key != pygame.K_RETURN:
	# 					self.player_name += event.unicode
	# 				elif event.key == pygame.K_RETURN and len(self.player_name) >= 1:
	# 					self.intro = False
	# 					self.drawname = False
	# 					self.new()
	
	# 		mouse_pos = pygame.mouse.get_pos()
	# 		mouse_pressed = pygame.mouse.get_pressed()

	# 		if back_button.is_pressed(mouse_pos, mouse_pressed):
	# 			self.drawname = False
	# 			self.intro_screen()
			
			
			
	# 		self.clock.tick(FPS)
	# 		pygame.display.update()
		
		# text_surface = self.title_font.render(self.player_name, True, (0, 0, 0))
		# pygame.draw.rect(self.screen, 'WHITE', pygame.Rect(WIDTH//2 - text_surface.get_width()//2-5, HEIGTH//2 - text_surface.get_height()//2-5, text_surface.get_width()+10, text_surface.get_height()+5),  2)
		# screen.blit(text_surface,(WIDTH//2 - text_surface.get_width()//2, HEIGTH//2 - text_surface.get_height()//2))

	# def read_score (self):

	# 	for x in self.scin:
	# 		self.scindex +=1
	# 		self.scorex += x
	# 		if x =='\n' or self.scindex == len(self.scin)-1:
	# 			self.scorelist.append(self.scorex)
	# 			self.scorex= ""

	# 	for x in self.plin:
	# 		self.plindex +=1
	# 		self.playerx += x
	# 		if x =='\n' or self.plindex == len(self.plin)-1:
	# 			self.playerlist.append(self.playerx)
	# 			self.playerx= ""

	# 	self.playername_first = ScoreInput(self.screen,"1. "+self.playerlist[0],(0,0,0),20,150,3)
	# 	self.playername_second = ScoreInput(self.screen,"2. "+self.playerlist[1],(0,0,0),20,250,3)
	# 	self.playername_third = ScoreInput(self.screen,"3. "+self.playerlist[2],(0,0,0),20,350,3)
	# 	self.playername_fourth = ScoreInput(self.screen,"4. "+self.playerlist[3],(0,0,0),20,450,3)
	# 	self.playername_fifth = ScoreInput(self.screen,"5. "+self.playerlist[4],(0,0,0),20,550,3)
        
	# 	self.score_first = ScoreInput(self.screen,self.scorelist[0],(0,0,0),500,150,3)
	# 	self.score_second = ScoreInput(self.screen,self.scorelist[1],(0,0,0),500,250,3)
	# 	self.score_third = ScoreInput(self.screen,self.scorelist[2],(0,0,0),500,350,3)
	# 	self.score_fourth = ScoreInput(self.screen,self.scorelist[3],(0,0,0),500,450,3)
	# 	self.score_fifth = ScoreInput(self.screen,self.scorelist[4],(0,0,0),500,550,3)

	# 	self.sctxt.close()
	# 	self.pltxt.close()
    
	# def display_score(self):
	# 	self.read_score()
	# 	self.playername_first.draw()
	# 	self.playername_second.draw()
	# 	self.playername_third.draw()
	# 	self.playername_fourth.draw()
	# 	self.playername_fifth.draw()
	# 	self.score_first.draw()
	# 	self.score_second.draw()
	# 	self.score_third.draw()
	# 	self.score_fourth.draw()
	# 	self.score_fifth.draw()
    
	# def run(self):
	# 	self.screen.fill('WHITE')
	# 	self.display_score()


g = Game()  
g.intro_screen()
#g.draw_name()
g.new()
while g.running:
	g.main()
	g.game_over()

pygame.quit()
sys.exit()