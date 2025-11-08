
import pygame
import math


enemy_size = (64, 64)  
             
        
#enemyA Bullet
class EnemyBullet(pygame.sprite.Sprite):
    
    #bullet removes after leaving the screen
    def __init__(self, x, y, vx, vy, screen_w, screen_h):
        super().__init__()
        img = pygame.image.load("bullet.png").convert_alpha()
        self.image = pygame.transform.scale(img, (12, 12))
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = float(vx)
        self.vy = float(vy)
        self.screen_w = int(screen_w)
        self.screen_h = int(screen_h)

    def update (self):
        # bullet movment
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)
        # delet if goes out
        if (self.rect.right < 0 or self.rect.left > self.screen_w or
            self.rect.bottom < 0 or self.rect.top > self.screen_h):
            self.kill()


#enemyA
class EnemyA(pygame.sprite.Sprite):
    
    #enemyA movment + shoot at the player
    def __init__(self, screen_w, screen_h,
                 start_x=100, start_y=100,
                 speed=5, health=3,
                 fire_every_ms=300, bullet_speed=4):
        super().__init__()
        img = pygame.image.load("enemy1.png").convert_alpha()
        self.image = pygame.transform.scale(img, enemy_size)
        self.rect = self.image.get_rect(topleft=(start_x, start_y))

        self.screen_w = int(screen_w)
        self.screen_h = int(screen_h)

        # enemyA stats
        self.health = int(health)
        self.speed = int(speed)
        #to the right
        self.direction = +1                
        self.right_max = self.screen_w - enemy_size[0]

        # shooting
        self.enemy_bullets = pygame.sprite.Group()
        self.fire_every_ms = int(fire_every_ms)
        self.last_shot_ms = 0
        self.bullet_speed = float(bullet_speed)

    def draw(self, surface):
        if self.health > 0:
            surface.blit(self.image, self.rect)
        self.enemy_bullets.draw(surface)        

    def update(self, player_rect=None):
        #bullet before enemy dies
        if self.health <= 0:
            self.enemy_bullets.update()
            self.kill()
            return

        # movement in x_led
        self.rect.x += self.speed * self.direction


        #move down ond row 
        if self.rect.x <= 0:
            self.rect.x = 0
            self.direction = +1
            self.rect.y += enemy_size[1]
        elif self.rect.x >= self.right_max:
            self.rect.x = self.right_max
            self.direction = -1
            self.rect.y += enemy_size[1]

        if self.rect.bottom >= self.screen_h:
            self.rect.y = -enemy_size[1]    

        # shooting the player
        if player_rect is not None:
            now = pygame.time.get_ticks()
            if now - self.last_shot_ms >= self.fire_every_ms:
                sx, sy = self.rect.center
                tx, ty = player_rect.center
                dx, dy = tx - sx, ty - sy
                dist = math.hypot(dx, dy) or 1.0
                vx = (dx / dist) * self.bullet_speed
                vy = (dy / dist) * self.bullet_speed
                self.enemy_bullets.add(EnemyBullet(sx, sy, vx, vy, self.screen_w, self.screen_h))
                #shoot new bullet                                   
                self.last_shot_ms = now

        self.enemy_bullets.update()

    def check_player_hits(self, player_sprite):
        if self.health <= 0:
            return 0
        hits = pygame.sprite.spritecollide(self, player_sprite.bullets, dokill=True)
        attack = len(hits)
        if attack > 0:
            self.health -= attack
            if self.health <= 0:  
                self.enemy_bullets.empty() 
                self.kill()
        return attack


#enemyB
class EnemyB(pygame.sprite.Sprite):
   
   #enemyB movment
    def __init__(self, screen_w, screen_h,
                 start_x, start_y,
                 health=5, fall_speed=0.8, follow_speed=2):
        super().__init__()
        img = pygame.image.load("enemy2.png").convert_alpha()
        self.image = pygame.transform.scale(img, enemy_size)
        self.rect = self.image.get_rect(topleft=(start_x, start_y))

        self.screen_w = int(screen_w)
        self.screen_h = int(screen_h)

        self.health = int(health)
        self.fall_speed = float(fall_speed)
        self.follow_speed = float(follow_speed)

    def draw(self, surface):
        if self.health > 0:
            surface.blit(self.image, self.rect)    

    def update(self, player_rect=None):
        if self.health <= 0:
            self.kill()
            return
        
        #move down
        self.rect.y += self.fall_speed

        if self.rect.top >= self.screen_h:
            self.rect.y = -enemy_size[1]

        #follow player in x_led
        if player_rect is not None:
            target_x = player_rect.centerx
            if self.rect.centerx < target_x:
                self.rect.x += self.follow_speed
            elif self.rect.centerx > target_x:
                self.rect.x -= self.follow_speed

    def check_player_hits(self, player_sprite):
        if self.health <= 0:
            return 0
        hits = pygame.sprite.spritecollide(self, player_sprite.bullets, dokill=True)
        attack = len(hits)
        if attack > 0:
            self.health -= attack
            if self.health <= 0:  
                self.enemy_bullets.empty() 
                self.kill()
        return attack
    


    def reached_player_level(self, player_sprite):
        if self.health <= 0:
            return False
        
        try:
            target_rect = player_sprite.rect
            
        except:
            target_rect = player_sprite
            
        if self.rect.bottom >= target_rect.top:
            try:
                player_sprite.lives = 0   
            except:
                pass
            return True

        return False
            
    

    def body_hit_player(self, player_sprite):
        if self.health <= 0:
            return False
        
        try:
            target_rect = player_sprite.rect
            
        except:
            target_rect = player_sprite
            
        if self.rect.colliderect(target_rect):
            try:
                player_sprite.lives = 0   
            except:
                pass
            return True

        return False



#test part
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((900, 900))
    pygame.display.set_caption("Enemy classes demo")
    clock = pygame.time.Clock()

    
    enemy_a = EnemyA(900, 900, 100, 100, speed=5, health=3,
                     fire_every_ms=300, bullet_speed=4)
    enemy_b = EnemyB(900, 900, 700, 100, health=5,
                     fall_speed=0.8, follow_speed=2)

    
    player_rect = pygame.Rect(430, 820, 40, 40)
    player_speed = 6

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < 900:
            player_rect.x += player_speed
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] and player_rect.bottom < 900:
            player_rect.y += player_speed

        
        #update enemy
        enemy_a.update(player_rect)
        enemy_b.update(player_rect)

        # die player
        if enemy_b.body_hit_player(player_rect):
            #Game Over
            screen.fill((30, 30, 30))
            font = pygame.font.SysFont(None, 48)
            msg = font.render("Game Over (EnemyB touched player)", True, (255, 80, 80))
            screen.blit(msg, (900//2 - msg.get_width()//2, 900//2 - msg.get_height()//2))
            pygame.display.update()
            pygame.time.delay(900)
            running = False

        
        screen.fill((0, 130, 130))

        
        pygame.draw.rect(screen, (200, 200, 200), player_rect)

        
        enemy_a.draw(screen)
        enemy_b.draw(screen)

        pygame.display.update()

    pygame.quit()
