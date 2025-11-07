import pygame
import button
import math
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
font=pygame.font.Font(None, 40)
player_health=3
enemy_health=5
enemy_health1=5
score=0

now=pygame.time.get_ticks()
#create button instances
start_button = button.Button(SCREEN_WIDTH/2 +100, button_y, start_img)
exit_button = button.Button(SCREEN_HEIGHT/2 -100, button_y, exit_img)

main_character = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80, speed=20, margin=30)
main_character_bullet = Bullet(main_character.rect.centerx, main_character.rect.top, -10)
player_health = main_character.lives
main_character.rect = main_character.image.get_rect()

# EnemyA
enemyAImg = pygame.image.load ("enemy1.png")
enemyAImg = pygame.transform.scale(enemyAImg, (64, 64))
enemyA_health = 3
enemyA_X = 100
enemyA_Y = 100
enemyA_speed = 5
enemyA_direction = +1
#limited on the right side
enemy_right_max = SCREEN_WIDTH - 64  

#enemyB
enemyBImg = pygame.image.load ("enemy2.png")
enemyBImg = pygame.transform.scale(enemyBImg, (64, 64))
enemyB_health = 5
enemyB_X = SCREEN_WIDTH - 64
enemyB_Y = 100
enemyB_change = 0.8

#following main_character
enemyB_follow_speed = 2
    
#bullet 
bulletImg = pygame.image.load("bullet.png")
bullet = pygame.transform.scale(bulletImg, (10, 10))

enemy_bullets = []
enemy_fire_every_ms = 300
enemy_last_shot = 0
enemy_bullet_speed = 4

#bullet position
enemy_bullet_X = enemyA_X + 32
enemy_bullet_Y = enemyA_Y + 32

#at the main_character center(first shot)
dx0= (main_character.rect.x + 32) - enemy_bullet_X
dy0= (main_character.rect.y + 32) - enemy_bullet_Y
distance0 = math.hypot (dx0, dy0) or 1
#kontroll bullet's speed
enemy_bullet_dx = (dx0 / distance0) * enemy_bullet_speed
enemy_bullet_dy = (dy0 / distance0) * enemy_bullet_speed

#center to center collision
def iscollision (x1, y1, x2, y2, thresh = 30):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance < thresh



clock = pygame.time.Clock()

active = False

#load image
background = Infinite_Background(SCREEN_WIDTH, "backgrounds/boss_bg_img.png")

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
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				run = False
			elif active and event.key == pygame.K_SPACE:
				main_character.shoot()
	
	screen.fill((0,0,0))
	

    # Draw scrolling background
	background.draw_background(screen, scroll_speed=5)

	if not active:
		if start_button.draw(screen):
			start_button.remove()
			exit_button.remove()
			active = True

		if exit_button.draw(screen):
			run = False
	else:
		main_character.handle_keys(keys, SCREEN_WIDTH, SCREEN_HEIGHT)
		
		main_character.update()
		main_character_bullet.update()
		main_character.bullets.draw(screen)
		screen.blit(main_character.image, main_character.rect)
		text_score=font.render(f"Score:{score}",True, (255,255,255))
		text_player_helath=font.render(f"Health:{player_health}",True, (255,255,255))
		text_enemy_health=font.render(f"Enemy 1:{enemy_health}", True, (255,255,255))
		text_enemy_health1=font.render(f"Enemy 2:{enemy_health1}", True, (255,255,255))
		screen.blit(text_enemy_health,(SCREEN_WIDTH-100,0))
		screen.blit(text_enemy_health1, (SCREEN_WIDTH-100,50))
		screen.blit(text_player_helath, (0,50))
		screen.blit(text_score, (0,0))
		#pygame.display.flip()
		# player_health = main_character.check_enemy_hits(enemy_bullets)

		#enemyA movement
		if enemyA_health > 0:
			enemyA_X = enemyA_X + (enemyA_speed * enemyA_direction)
			if enemyA_X <= 0:
					enemyA_X = 0
					enemyA_direction = +1
					enemyA_Y += 64
			elif enemyA_X >= enemy_right_max:
					enemyA_X = enemy_right_max
					enemyA_direction = -1
					enemyA_Y += 64

		#enemyB movement
		if enemyB_health > 0:
			#always downward
			enemyB_Y += enemyB_change

			#closing in the main_character
			target_x = main_character.rect.x  
			center_x = enemyB_X + 32

			if center_x < target_x:
				enemyB_X += enemyB_follow_speed
			elif center_x > target_x:
				enemyB_X -= enemyB_follow_speed


			if enemyB_Y + 64 >= main_character.rect.y:
				game_over = True
		
			#enemyA bullet (always active)
		if enemyA_health > 0:
			
			if now - enemy_last_shot >= enemy_fire_every_ms:
				bx = enemyA_X + 32
				by = enemyA_Y + 32
				dx = (main_character.rect.x + 32) - bx
				dy = (main_character.rect.y + 32) - by
				dist = math.hypot(dx, dy) or 1
				vx = (dx / dist) * enemy_bullet_speed
				vy = (dy / dist) * enemy_bullet_speed
				enemy_bullets.append({"x": bx, "y": by, "dx": vx, "dy": vy})
				enemy_last_shot = now
			
			for b in enemy_bullets:
				b["x"] += b["dx"]
				b["y"] += b["dy"]

		


			#enemies's bullet hits the main_character's center
			p_cx, p_cy = main_character.rect.x + 32, main_character.rect.y + 32
			hit_any = False
			kept = []
			for b in enemy_bullets:
				if iscollision(p_cx, p_cy, b["x"], b["y"], thresh=30):
					hit_any = True
					player_health -= 1

				else:
					if 0 <= b["x"] <= SCREEN_WIDTH and 0 <= b["y"] <= SCREEN_HEIGHT:
						enemy_bullets.append(b)
				
			
			enemy_bullets = kept
			if hit_any:
				game_over = True

			#enemyA's bullet
			for b in enemy_bullets:
				screen.blit(bulletImg, (b["x"] - 5, b["y"] - 5))
			
			if enemyA_health > 0:
				screen.blit(enemyAImg, (enemyA_X, enemyA_Y))
			if enemyB_health > 0:
				screen.blit(enemyBImg, (enemyB_X, enemyB_Y))



	pygame.display.update()
		

pygame.quit()

