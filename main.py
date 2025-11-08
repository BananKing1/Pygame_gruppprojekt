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

enemies_active = None
player_health = 3
enemy_health = 5
enemy_health1 = 3

score=0

#create button instances
start_button = button.Button(SCREEN_WIDTH/2 +100, button_y, start_img)
exit_button = button.Button(SCREEN_HEIGHT/2 -100, button_y, exit_img)

main_character = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80, speed=20, margin=30)
enemy_a = EnemyA(SCREEN_WIDTH, SCREEN_HEIGHT, start_x=100, start_y=120, speed=5, health=3, fire_every_ms=300, bullet_speed=6)
enemy_b = EnemyB(SCREEN_WIDTH, SCREEN_HEIGHT, start_x=SCREEN_WIDTH-200, start_y=120, health=5, fall_speed=1.2, follow_speed=3)
main_character_bullet = Bullet(main_character.rect.centerx, main_character.rect.top, -10)
player_health = main_character.lives
player_health_boss = 5

# Make Boss & Asteroid objects (Natalie's part)
boss_active = False
boss_health = 10
boss_enemy = Boss(SCREEN_WIDTH, SCREEN_HEIGHT, boss_health)
boss_beam = Beam(5, 2, boss_enemy)
asteroid = Asteroid(SCREEN_WIDTH, SCREEN_HEIGHT, 2, 2)
small_asteroid = Asteroid(SCREEN_WIDTH, SCREEN_HEIGHT, 1, 1)
small_asteroid_2 = Asteroid(SCREEN_WIDTH, SCREEN_HEIGHT, 1, 1)
# Asteroid speed, because asteroids have different speeds
asteroid_speed = 9


clock = pygame.time.Clock()
tick_speed = 60

active = False
paused = False

#load image
background = Infinite_Background(SCREEN_WIDTH, "backgrounds/boss_bg_img.png")

#game loop
run = True
while run:
    clock.tick(tick_speed) #tick speed
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
    background.draw_background(screen, 5)

    if not active:
        if start_button.draw(screen):
            start_button.remove()
            exit_button.remove()
            active = True

        if exit_button.draw(screen):
            run = False
    else:
        # player score and health (Nasra's part)
        text_score=font.render(f"Score: {score}",True, (255,255,255))
        text_player_helath=font.render(f"Health: {player_health}",True, (255,255,255))
        screen.blit(text_player_helath, (0,50))
        screen.blit(text_score, (0,0))
        
        # player mechanics (Sara's part)
        main_character.handle_keys(keys, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        main_character.update()
        main_character_bullet.update()

        main_character.bullets.draw(screen)
        screen.blit(main_character.image, main_character.rect)

        # spawn enemies
        enemies_active = True



        """ Enemies FIGHT!!! """
        if enemies_active == True and boss_active == False:
            # enemies health (Nasra's part)
            text_enemy_health=font.render(f"Enemy 1: {enemy_health}", True, (255,255,255))
            text_enemy_health1=font.render(f"Enemy 2: {enemy_health1}", True, (255,255,255))
            screen.blit(text_enemy_health,(SCREEN_WIDTH-100,0))
            screen.blit(text_enemy_health1, (SCREEN_WIDTH-100,50))
            
            #enemies update (Zahra's part)
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

            # draw enemies
            enemy_a.draw(screen)
            enemy_b.draw(screen)

            player_health = main_character.lives
            enemy_health = max(0, enemy_a.health)
            enemy_health1 = max(0, enemy_b.health)

            # stops the game when player dies
            if player_health == 0:
                print("You lose :(")
                active = False

            # handle player score, add 25 per enemy per frame
            if enemy_health == 0:
                score += 25
            if enemy_health1 == 0:
                score += 25


            # spawn boss when both enemies are dead
            if enemy_health == 0 and enemy_health1 == 0:
                enemies_active = False
                boss_active = True
        


        """ Boss FIGHT!!! """
        if boss_active == True:
            # increase score per frame
            score += 50

            # Show boss health (Nasra's part)
            text_boss_health=font.render(f"Boss: {boss_health}", True, (255,255,255))
            screen.blit(text_boss_health,(SCREEN_WIDTH-100,0))

            # Draw objects (Natalie's part)
            screen.blit(boss_enemy.image, boss_enemy.rect)
            screen.blit(asteroid.image, asteroid.rect)
            screen.blit(small_asteroid.image, small_asteroid.rect)
            screen.blit(small_asteroid_2.image, small_asteroid_2.rect)

            boss_beam.shoot_beam(main_character)
            boss_beam.beam_reset(SCREEN_WIDTH, SCREEN_HEIGHT, boss_enemy)
            asteroid.throw_asteroid(asteroid_speed, SCREEN_WIDTH)
            small_asteroid.throw_asteroid(asteroid_speed + 1, SCREEN_WIDTH)
            small_asteroid_2.throw_asteroid(asteroid_speed + 2, SCREEN_WIDTH)


            # stops the game when player dies
            if player_health == 0:
                print("You lose :(")
                active = False


            # Move boss, beam, asteroids
            if boss_health > 0:
                boss_enemy.shake()
                screen.blit(boss_beam.image, boss_beam.rect) # will "remove" beam when boss dies

                # Handle boss, player health and collision
                boss_health = boss_enemy.take_damage(main_character.bullets)
                main_character.lives = boss_beam.beam_hit_player(main_character, main_character.lives, boss_enemy)
                main_character.lives = asteroid.collided_asteroid(main_character, main_character.lives, SCREEN_WIDTH)
                main_character.lives = small_asteroid.collided_asteroid(main_character, main_character.lives, SCREEN_WIDTH)
                main_character.lives = small_asteroid_2.collided_asteroid(main_character, main_character.lives, SCREEN_WIDTH)
                player_health = main_character.lives

            # boss is dead
            else: 
                boss_beam.remove()
                paused = boss_enemy.boss_dies()



        """ Player WINS!!! """
        # edited Zahra's code
        while paused:
            # display message and score
            font = pygame.font.SysFont(None, 48)
            msg = font.render("You win, yippie!!!", True, (255, 255, 0))
            display_score = font.render(f"Score: {score}", True, (255, 255, 0))
            screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, SCREEN_HEIGHT//2 - msg.get_height()//2-25))
            screen.blit(display_score, (SCREEN_WIDTH//2 - display_score.get_width()//2, SCREEN_HEIGHT//2 - display_score.get_height()//2+25))
            
            # update screen before freezing
            pygame.display.flip()

            # freeze the game until player press esc
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        paused = False        
                

        pygame.display.flip()
    pygame.display.update()
pygame.quit()


