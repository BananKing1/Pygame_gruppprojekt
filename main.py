import pygame
import button
from boss import Boss, Beam, Asteroid, Infinite_Background 

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

clock = pygame.time.Clock()

#load image
background = Infinite_Background(SCREEN_WIDTH, SCREEN_HEIGHT, "backgrounds/boss_bg_img.png")

#game loop
run = True
while run:
	clock.tick(60) #tick speed

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	
	screen.fill((0,0,0))

    # Draw scrolling background
	background.draw(screen, scroll_speed=5)

	if start_button.draw(screen):
		print('START')

	if exit_button.draw(screen):
		print('EXIT')
		run = False

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False

	if pygame.key.get_pressed()[pygame.K_ESCAPE]:
		run =False

	pygame.display.update()

pygame.quit()

