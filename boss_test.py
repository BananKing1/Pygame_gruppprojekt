import pygame
from boss import Boss, Beam, Asteroid, Infinite_Background


pygame.init()

# Screen
info = pygame.display.Info()
SCREEN_WIDTH  = info.current_w
SCREEN_HEIGHT = info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Boss Test")

clock = pygame.time.Clock()
running = True

#load image
background = Infinite_Background(SCREEN_WIDTH, SCREEN_HEIGHT, "backgrounds/boss_bg_img.png")

# Player (stats)
player = pygame.Rect(200, 200, 50, 50)
player_health = 20
boss_health = 10

# Make Boss & Asteroid objects
boss_enemy = Boss(SCREEN_WIDTH, SCREEN_HEIGHT, 10)
boss_beam = Beam(10, 2, boss_enemy)
asteroid = Asteroid(SCREEN_WIDTH, SCREEN_HEIGHT, 2, 2) # create boss and pos for boss
small_asteroid = Asteroid(SCREEN_WIDTH, SCREEN_HEIGHT, 1, 1) # create boss and pos for boss
small_asteroid_2 = Asteroid(SCREEN_WIDTH, SCREEN_HEIGHT, 1, 1) # create boss and pos for boss

# Asteroid stats
asteroid_speed = 10
asteroid_size = 50


while running:
    clock.tick(60) #tick speed

    # Handle quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0,0,0)) 

    # Draw scrolling background
    background.draw_background(screen, scroll_speed=5)

    # ESC quits
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        running = False


    # Move boss, beam, asteroids
    boss_enemy.shake()
    boss_beam.shoot_beam(player, boss_enemy)
    boss_beam.beam_reset(SCREEN_WIDTH, SCREEN_HEIGHT, boss_enemy)
   
    asteroid.throw_asteroid(asteroid_speed, SCREEN_WIDTH)
    small_asteroid.throw_asteroid(asteroid_speed + 5, SCREEN_WIDTH)   
    small_asteroid_2.throw_asteroid(asteroid_speed + 5, SCREEN_WIDTH)   
    

    # Health
    player_health = boss_beam.beam_hit_player(player, player_health, boss_enemy)
    player_health = asteroid.collided_asteroid(player, asteroid.rect, player_health, SCREEN_WIDTH)
    player_health = small_asteroid.collided_asteroid(player, small_asteroid.rect, player_health, SCREEN_WIDTH)
    player_health = small_asteroid_2.collided_asteroid(player, small_asteroid_2.rect, player_health, SCREEN_WIDTH)
    
    # Draw objects
    pygame.draw.rect(screen, (0, 0, 255), player)
    screen.blit(boss_enemy.image, boss_enemy.rect)
    screen.blit(boss_beam.image, boss_beam.rect)
    screen.blit(asteroid.image, asteroid.rect)
    screen.blit(small_asteroid.image, small_asteroid.rect)
    screen.blit(small_asteroid_2.image, small_asteroid_2.rect)

    pygame.display.update()
pygame.quit()