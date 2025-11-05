import pygame
import math

pygame.init()

#screen
screen = pygame.display.set_mode((1000,1000))

#player
player_w = player_h = 64
player_X = 900
player_Y = 900

# EnemyA
enemyAImg = pygame.image.load ("enemy1.png")
enemyAImg = pygame.transform.scale(enemyAImg, (64, 64))
enemyA_health = 3
enemyA_X = 100
enemyA_Y = 100
enemyA_speed = 0.4
enemyA_direction = +1
enemy_right_max = 1000 - 64

#enemyB
enemyBImg = pygame.image.load ("enemy2.png")
enemyBImg = pygame.transform.scale(enemyBImg, (64, 64))
enemyB_health = 5
enemyB_X = 936
enemyB_Y = 100
enemyB_change = 0.1
    
#bullet 
bulletImg = pygame.image.load("bullet.webp")

#player bullet
player_bullet_X = player_X + player_w // 2
player_bullet_Y = player_Y
player_bullet_speed = -10
player_bullet_state = "ready" 

#bullet for enemyA
enemy_bullet_X = enemyA_X + 32
enemy_bullet_Y = enemyA_Y + 32
enemy_bullet_dx = 0
enemy_bullet_dy = 0
enemy_bullet_speed = 4


    

dx0= (player_X + 32) - enemy_bullet_X
dy0= (player_Y + 32) - enemy_bullet_Y
distance = math.hypot (dx0/dy0) or 1
bullet_dx = (dx0 / distance) * enemy_bullet_speed
bullet_dy = (dy0 / distance) * enemy_bullet_speed


running = True
game_over = False
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if player_bullet_state == "ready":
                player_bullet_state = "fire"
                player_bullet_X = player_X + player_w // 2
                player_bullet_Y = player_Y


            
    if game_over:

        screen.fill((25, 25, 25))
        font = pygame.font.SysFont(None, 48)
        msg = font.render("Game Over", True, (255, 80, 80))
        screen.blit(msg, (1000//2 - msg.get_width()//2, 1000//2 - msg.get_height()//2))
        pygame.display.update()
        continue
       


    #enemyA movement
    if enemyA_health > 0:
        enemyA_X = enemyA_X + (enemyA_speed * enemyA_direction)
        if enemyA_X <= 0:
                enemyA_X = 0
                enemyA_direction = +1
                enemyA_Y += 64
        elif enemyA_X >= 936:
                enemyA_X = 936
                enemyA_direction = -1
                enemyA_Y += 64


    if enemyB_health > 0:
        enemyB_Y += enemyB_change
        if enemyB_Y + 64 >= player_Y:
            game_over = True









    #bullet movment
    if player_bullet_state == "fire":
        player_bullet_Y += player_bullet_speed
        if player_bullet_Y < 0:
            player_bullet_state = "ready"
            player_bullet_Y = player_Y

    if player_bullet_state == "fire" and enemyA_health > 0:
        eA_cx, eA_cy = enemyA_X + 32, enemyA_Y + 32
        if iscollision(eA_cx, eA_cy, player_bullet_X, player_bullet_Y, thresh=36):
            enemyA_health -= 1
            player_bullet_state = "ready"
            player_bullet_Y = player_Y

    if player_bullet_state == "fire" and enemyB_health > 0:
        eB_cx, eB_cy = enemyB_X + 32, enemyB_Y + 32
        if iscollision(eB_cx, eB_cy, player_bullet_X, player_bullet_Y, thresh=36):
            enemyB_health -= 1
            player_bullet_state = "ready"
            player_bullet_Y = player_Y

    enemy_bullet_X += enemy_bullet_dx
    enemy_bullet_Y += enemy_bullet_dy

    p_cx, p_cy = player_X + 32, player_Y + 32
    if iscollision(p_cx, p_cy, enemy_bullet_X, enemy_bullet_Y, thresh=30):
        game_over = True









                    

        if enemy_bullet_X < 0 or enemy_bullet_X > 1000 or enemy_bullet_Y < 0 or enemy_bullet_Y > 1000 :
            enemy_bullet_X = enemyA_X + 32
            enemy_bullet_Y = enemyA_Y + 32
            dx = (player_X + 32) - enemy_bullet_X
            dy = (player_Y + 32) - enemy_bullet_Y
            distance = math.hypot (dx0/dy0) or 1
            bullet_dx = (dx0 / distance) * enemy_bullet_speed
            bullet_dy = (dy0 / distance) * enemy_bullet_speed


        screen.fill((0,128,128))

        pygame.draw.rect(screen, (200,200,200), (player_X, player_Y, player_w, player_h))

        if enemyA_health > 0:
            screen.blit(enemyAImg, enemyA_X, enemyA_Y)
        if enemyB_health > 0:
            screen.blit(enemyBImg, enemyB_X, enemyB_Y)

        if player_bullet_state == "fire":
            screen.blit(bulletImg, (player_bullet_X - 8, player_bullet_Y - 8))

        screen.blit(bulletImg, (enemy_bullet_X - 8, enemy_bullet_Y - 8))
        
                        

        
    pygame.display.update()


    
     