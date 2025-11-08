import pygame
import button
from boss import Boss, Beam, Asteroid, Infinite_Background 
from main_character import Player, Bullet
from enemies import EnemyA, EnemyB 

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

#create button instances
start_button = button.Button(SCREEN_WIDTH/2 +100, button_y, start_img)
exit_button = button.Button(SCREEN_HEIGHT/2 -100, button_y, exit_img)

main_character = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80, speed=20, margin=30)
enemy_a = EnemyA(SCREEN_WIDTH, SCREEN_HEIGHT, start_x=100, start_y=120, speed=5, health=3, fire_every_ms=300, bullet_speed=6)
enemy_b = EnemyB(SCREEN_WIDTH, SCREEN_HEIGHT, start_x=SCREEN_WIDTH-200, start_y=120, health=5, fall_speed=1.2, follow_speed=3)
main_character_bullet = Bullet(main_character.rect.centerx, main_character.rect.top, -10)
player_health = main_character.lives





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

        #enemis update
        enemy_a.update(main_character.rect)
        enemy_b.update(main_character.rect)

        #collision(player's bullet to enemies)
        enemy_a.check_player_hits(main_character)
        enemy_b.check_player_hits(main_character)

        #collision(enemyA's bullet to player)
        for bullet in list(enemy_a.enemy_bullets):
            if main_character.rect.colliderect(bullet.rect):
                bullet.kill()
                main_character.lives = max(0,main_character.lives - 1)

        main_character.bullets.draw(screen)
        screen.blit(main_character.image, main_character.rect)

        enemy_a.draw(screen)
        enemy_b.draw(screen)

        player_health = main_character.lives
        enemy_health = max(0, enemy_a.health)
        enemy_health = max(0, enemy_b.health)


        text_score=font.render(f"Score:{score}",True, (255,255,255))
        text_player_helath=font.render(f"Health:{player_health}",True, (255,255,255))
        text_enemy_health=font.render(f"Enemy 1:{enemy_health}", True, (255,255,255))
        text_enemy_health1=font.render(f"Enemy 2:{enemy_health1}", True, (255,255,255))
        screen.blit(text_enemy_health,(SCREEN_WIDTH-100,0))
        screen.blit(text_enemy_health1, (SCREEN_WIDTH-100,50))
        screen.blit(text_player_helath, (0,50))
        screen.blit(text_score, (0,0))
        pygame.display.flip()
        # player_health = main_character.check_enemy_hits(enemy_bullets)

    pygame.display.update()
    

pygame.quit()


