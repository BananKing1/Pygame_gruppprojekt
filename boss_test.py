import pygame
import button
from boss import Boss, Beam, Asteroid, Infinite_Background 
from main_character import Player, Bullet

pygame.init()

# Create display window
info = pygame.display.Info()
SCREEN_HEIGHT = info.current_h
SCREEN_WIDTH = info.current_w

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Our game')

# Load button images
start_img = pygame.image.load('sprites/start_btn.png').convert_alpha()
exit_img = pygame.image.load('sprites/exit_btn.png').convert_alpha()

button_y = SCREEN_HEIGHT / 2

# Create button instances
start_button = button.Button(SCREEN_WIDTH / 2 + 100, button_y, start_img)
exit_button = button.Button(SCREEN_HEIGHT / 2 - 100, button_y, exit_img)

main_character = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80, speed=20, margin=30)
player_health = main_character.lives

main_character_bullet = Bullet(main_character.rect.centerx, main_character.rect.top, -10)

# Make Boss & Asteroid objects
boss_active = True
boss_health = 10
boss_enemy = Boss(SCREEN_WIDTH, SCREEN_HEIGHT, boss_health)
boss_beam = Beam(5, 2, boss_enemy)
asteroid = Asteroid(SCREEN_WIDTH, SCREEN_HEIGHT, 2, 2)
small_asteroid = Asteroid(SCREEN_WIDTH, SCREEN_HEIGHT, 1, 1)
small_asteroid_2 = Asteroid(SCREEN_WIDTH, SCREEN_HEIGHT, 1, 1)

# Asteroid stats
asteroid_speed = 9

clock = pygame.time.Clock()
active = False

# Load background image
background = Infinite_Background(SCREEN_WIDTH, "backgrounds/boss_bg_img.png")

# Game loop
run = True
while run:
    clock.tick(60)  # tick speed
    keys = pygame.key.get_pressed()

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif active and event.key == pygame.K_SPACE:
                main_character.shoot()

    screen.fill((0, 0, 0))

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
        main_character_bullet.update()
        main_character.bullets.draw(screen)
        main_character.update()
        screen.blit(main_character.image, main_character.rect)

        """Boss FIGHT!!!"""
        if boss_active == True:
            # Draw objects
            screen.blit(boss_enemy.image, boss_enemy.rect)
            screen.blit(asteroid.image, asteroid.rect)
            screen.blit(small_asteroid.image, small_asteroid.rect)
            screen.blit(small_asteroid_2.image, small_asteroid_2.rect)

            boss_beam.shoot_beam(main_character)
            boss_beam.beam_reset(SCREEN_WIDTH, SCREEN_HEIGHT, boss_enemy)
            asteroid.throw_asteroid(asteroid_speed, SCREEN_WIDTH)
            small_asteroid.throw_asteroid(asteroid_speed + 1, SCREEN_WIDTH)
            small_asteroid_2.throw_asteroid(asteroid_speed + 2, SCREEN_WIDTH)

            # Move boss, beam, asteroids
            if boss_health > 0:
                boss_enemy.shake()
                screen.blit(boss_beam.image, boss_beam.rect) # will "remove" beam when boss dies

                # Handle boss, player health and collision
                boss_health = boss_enemy.take_damage(main_character.bullets)
                player_health = boss_beam.beam_hit_player(main_character, player_health, boss_enemy)
                player_health = asteroid.collided_asteroid(main_character, player_health, SCREEN_WIDTH)
                player_health = small_asteroid.collided_asteroid(main_character, player_health, SCREEN_WIDTH)
                player_health = small_asteroid_2.collided_asteroid(main_character, player_health, SCREEN_WIDTH)
            else: # boss is dead
                boss_beam.remove()
                boss_enemy.boss_dies()

    pygame.display.update()

pygame.quit()
