import pygame
import math

pygame.init()

#screen

screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("enemies")
width, height = screen.get_size()
clock =pygame.time.Clock()


#player
player_w = player_h = 64
#players center
player_X = 900 
player_Y = 900

# EnemyA
enemyAImg = pygame.image.load ("enemy1.png")
enemyAImg = pygame.transform.scale(enemyAImg, (64, 64))
enemyA_health = 3
enemyA_X = 100
enemyA_Y = 100
enemyA_speed = 5
enemyA_direction = +1
#limited on the right side
enemy_right_max = width - 64  

#enemyB
enemyBImg = pygame.image.load ("enemy2.png")
enemyBImg = pygame.transform.scale(enemyBImg, (64, 64))
enemyB_health = 5
enemyB_X = width - 64
enemyB_Y = 100
enemyB_change = 0.8

#following player
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

#at the player center(first shot)
dx0= (player_X + 32) - enemy_bullet_X
dy0= (player_Y + 32) - enemy_bullet_Y
distance0 = math.hypot (dx0, dy0) or 1
enemy_bullet_dx = (dx0 / distance0) * enemy_bullet_speed
enemy_bullet_dy = (dy0 / distance0) * enemy_bullet_speed


#player bullet
player_bullet_X = player_X 
player_bullet_Y = player_Y
player_bullet_speed = -10
#ready or fire
player_bullet_state = "ready" 



#center to center collision
def iscollision (x1, y1, x2, y2, thresh = 30):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance < thresh



running = True
game_over = False


while running:
    clock.tick(60)
    now = pygame.time.get_ticks()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #player's bullet to enemies (space)    
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if player_bullet_state == "ready":
                player_bullet_state = "fire"
                player_bullet_X = player_X 
                player_bullet_Y = player_Y


            
    if game_over:
        screen.fill((25, 25, 25))
        font = pygame.font.SysFont(None, 48)
        msg = font.render("Game Over", True, (255, 80, 80))
        screen.blit(msg, (1000//2 - msg.get_width()//2, height//2 - msg.get_height()//2))
        pygame.display.update()
        continue
       


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

        #closing in the player
        target_x = player_X  
        center_x = enemyB_X + 32

        if center_x < target_x:
            enemyB_X += enemyB_follow_speed
        elif center_x > target_x:
            enemyB_X -= enemyB_follow_speed


        if enemyB_Y + 64 >= player_Y:
            game_over = True


    #bullet movment
    if player_bullet_state == "fire":
        player_bullet_Y += player_bullet_speed
        if player_bullet_Y < 0:
            player_bullet_state = "ready"
            player_bullet_Y = player_Y


    #player's bullet hits the enemyA
    if player_bullet_state == "fire" and enemyA_health > 0:
        eA_cx, eA_cy = enemyA_X + 32, enemyA_Y + 32
        if iscollision(eA_cx, eA_cy, player_bullet_X, player_bullet_Y, thresh=36):
            enemyA_health -= 1
            player_bullet_state = "ready"
            player_bullet_Y = player_Y


    #player's bullet hits the enemyB
    if player_bullet_state == "fire" and enemyB_health > 0:
        eB_cx, eB_cy = enemyB_X + 32, enemyB_Y + 32
        if iscollision(eB_cx, eB_cy, player_bullet_X, player_bullet_Y, thresh=36):
            enemyB_health -= 1
            player_bullet_state = "ready"
            player_bullet_Y = player_Y

    #enemyA bullet (always active)
    if enemyA_health > 0:

        if now - enemy_last_shot >= enemy_fire_every_ms:
            bx = enemyA_X + 32
            by = enemyA_Y + 32
            dx = (player_X + 32) - bx
            dy = (player_Y + 32) - by
            dist = math.hypot(dx, dy) or 1
            vx = (dx / dist) * enemy_bullet_speed
            vy = (dy / dist) * enemy_bullet_speed
            enemy_bullets.append({"x": bx, "y": by, "dx": vx, "dy": vy})
            enemy_last_shot = now

        for b in enemy_bullets:
            b["x"] += b["dx"]
            b["y"] += b["dy"]

       


        #enemies's bullet hits the player's center
        p_cx, p_cy = player_X + 32, player_Y + 32
        hit_any = False
        kept = []
        for b in enemy_bullets:
            if iscollision(p_cx, p_cy, enemy_bullet_X, enemy_bullet_Y, thresh=30):
                hit_any = True

            else:
                if 0 <= b["x"] <= width and 0 <= b["y"] <= height:
                    kept.append(b)
        enemy_bullets = kept
        if hit_any:
            game_over = True


    #draw
    screen.fill((0,128,128))

    #player model
    pygame.draw.rect(screen, (200,200,200), (player_X - player_w//2,player_Y - player_h//2, player_w, player_h))

    if enemyA_health > 0:
        screen.blit(enemyAImg, (enemyA_X, enemyA_Y))
    if enemyB_health > 0:
        screen.blit(enemyBImg, (enemyB_X, enemyB_Y))


    #player's bullet
    if player_bullet_state == "fire":
        screen.blit(bulletImg, (player_bullet_X - 8, player_bullet_Y - 8))

    #enemyA's bullet
    for b in enemy_bullets:
        screen.blit(bulletImg, (b["x"] - 8, b["y"] - 8))
                        
    pygame.display.update()


    
     