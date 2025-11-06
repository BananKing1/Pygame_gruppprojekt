import pygame
import button
from boss import Boss, Beam, Asteroid, Infinite_Background 
from main_character import Player, Bullet

pygame.init()
#create display window
info=pygame.display.Info()
SCREEN_HEIGHT = info.current_h
SCREEN_WIDTH = info.current_w

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Our game')

#load button images
start_img = pygame.image.load('sprites/start_btn.png').convert_alpha()
exit_img = pygame.image.load('sprites/exit_btn.png').convert_alpha()

button_y= SCREEN_HEIGHT/2

#create button instances
start_button = button.Button(SCREEN_WIDTH/2 +100, button_y, start_img)
exit_button = button.Button(SCREEN_HEIGHT/2 -100, button_y, exit_img)

main_character = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80, speed=20, margin=30)
main_character_bullet = Bullet(main_character.rect.centerx, main_character.rect.top, -10)
player_health = main_character.lives

clock = pygame.time.Clock()

active = False

#load image
background = Infinite_Background(SCREEN_WIDTH, SCREEN_HEIGHT, "backgrounds/boss_bg_img.png")

#game loop
run = True
while run:
	clock.tick(60) #tick speed
	keys = pygame.key.get_pressed()

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False
	
	screen.fill((0,0,0))

    # Draw scrolling background
	background.draw_background(screen, scroll_speed=5)

	if not active:
		if start_button.draw(screen):
			start_button.remove()
			exit_button.remove()
			print('START')
			
			active = True

		if exit_button.draw(screen):
			print('EXIT')
			run = False
	else:
		if pygame.key.get_pressed()[pygame.K_ESCAPE]:
			run =False
		
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				run = False
			elif e.type == pygame.KEYDOWN:
			# Tryck ESC för att avsluta spelet
				if e.key == pygame.K_ESCAPE:
					run = False
				elif e.key == pygame.K_SPACE:
					main_character.shoot()

		screen.blit(main_character.image, main_character.rect)
		main_character.handle_keys(keys, SCREEN_WIDTH, SCREEN_HEIGHT)
		
		main_character.update()
		main_character_bullet.update()
		main_character.bullets.draw(screen)
		screen.blit(main_character.image, main_character.rect)
		# player_health = main_character.check_enemy_hits(enemy_bullets)

	pygame.display.update()

pygame.quit()

