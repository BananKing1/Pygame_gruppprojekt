import pygame
import button

pygame.init()
#create display window
info=pygame.display.Info()
SCREEN_HEIGHT = info.current_h
SCREEN_WIDTH = info.current_w

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Button Demo')

#load button images
start_img = pygame.image.load('sprites/start_btn.png').convert_alpha()
exit_img = pygame.image.load('sprites/exit_btn.png').convert_alpha()

#create button instances
start_button = button.Button(100, 200, start_img, 0.8)
exit_button = button.Button(450, 200, exit_img, 0.8)

#game loop
run = True
while run:

	screen.fill((0,0,0))

	if start_button.draw(screen):
		print('START')
	if exit_button.draw(screen):
		print('EXIT')

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False

	if pygame.key.get_pressed()[pygame.K_ESCAPE]:
		run =False

	pygame.display.update()

pygame.quit()

