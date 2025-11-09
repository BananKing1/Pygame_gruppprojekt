import pygame
import math

enemy_size = (64, 64)  

#bullet
class EnemyBullet(pygame.sprite.Sprite):
    """bullet tas bort när går utanför skärmen"""

    #screen_width (screen_w) / screen_height (screen_h) 
    def __init__(self, x, y, vx, vy, screen_w, screen_h):
        super().__init__()

        #ladda bullet's bild
        img = pygame.image.load("bullet.png").convert_alpha()

        #bullet storlek
        self.image = pygame.transform.scale(img, (12, 12))

        #bullet position på skärm enligt bullet's center
        self.rect = self.image.get_rect(center=(x, y))

        #bullet's hastighet på x_y_led på decimal
        self.vx = float(vx)
        self.vy = float(vy)

        #skärm storlek (heltal)
        self.screen_w = screen_w
        self.screen_h = screen_h

    def update (self):
        # bullet's rörelse med sin hastighet
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)

        # tas bort bullet (när går ut från alla sidan av skärmen)
        if (self.rect.right < 0 or self.rect.left > self.screen_w or self.rect.bottom < 0 or self.rect.top > self.screen_h):
            self.kill()


#enemyA
class EnemyA(pygame.sprite.Sprite):
    
    """när åker ut längs ner, kommer tillbaka uppifrån/ når till kanten, går ner en rad/ skjutar på main charakter """
    def __init__(self, screen_w, screen_h, start_x=100, start_y=100, speed=5, health=3, fire_every_ms=300, bullet_speed=4):
        super().__init__()
        img = pygame.image.load("enemy1.png").convert_alpha()
        self.image = pygame.transform.scale(img, enemy_size)

        #position på skärm
        self.rect = self.image.get_rect(topleft=(start_x, start_y))

        self.screen_w = int(screen_w)
        self.screen_h = int(screen_h)

        #antal liv
        self.health = int(health)
        self.speed = int(speed)

         #går åt höger
        self.direction = +1     
        #max högergräns som kan gå ( vänster gräns är 0)           
        self.right_max = self.screen_w - enemy_size[0]

        #en grupp av massor bullets
        self.enemy_bullets = pygame.sprite.Group()
        #tid mellan skotten
        self.fire_every_ms = int(fire_every_ms)
        self.last_shot_ms = 0
        self.bullet_speed = float(bullet_speed)
    
    #rita enemy och bullet på skärmen så längre enemy lever
    def draw(self, surface):
        if self.health > 0:
            #sätta bild på skärm
            surface.blit(self.image, self.rect)
        self.enemy_bullets.draw(surface)        

    def update(self, player_rect=None):
        #försvinner när livet slutas (enemy och bullet)
        if self.health <= 0:
            self.enemy_bullets.empty()
            self.kill()
            return

        # hur röra sig på x_led
        self.rect.x += self.speed * self.direction


        # vänder och går ner en rad när träffar kanten(höger och vänster) 
        if self.rect.x <= 0:
            self.rect.x = 0
            #åt höger
            self.direction = +1
            #går ner (en fiende storlek)
            self.rect.y += enemy_size[1]
        elif self.rect.x >= self.right_max:
            #går inte mer max högergräns
            self.rect.x = self.right_max
            #åt vänster
            self.direction = -1
            self.rect.y += enemy_size[1]

        # när åker ut längs ner, kommer tillbaka uppifrån
        if self.rect.bottom >= self.screen_h:
            self.rect.y = -enemy_size[1]    

        #sjukas mot player( om plater finns)
        if player_rect is not None:

            #nuvarande tid(för skott beräkning)
            now = pygame.time.get_ticks()
            if now - self.last_shot_ms >= self.fire_every_ms:
                #enemy centere (bullets plats)
                sx, sy = self.rect.center
                #bullet's mål
                tx, ty = player_rect.center
                #avstånd mellan player och enemys bullet på (x,y)
                dx, dy = tx - sx, ty - sy
                dist = math.hypot(dx, dy) or 1.0
                #att gå i riktning mot player med en hastighet
                vx = (dx / dist) * self.bullet_speed
                vy = (dy / dist) * self.bullet_speed
                #ny bullet med vx, vy hastighet
                self.enemy_bullets.add(EnemyBullet(sx, sy, vx, vy, self.screen_w, self.screen_h))                                  
                self.last_shot_ms = now

        self.enemy_bullets.update()

    def check_player_hits(self, player_sprite):
        """varje bullet = en attack, player's bullet träffar enemyA """
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
   
    """följer spelare på x_led, när går ut längst ner från skärm, kommer tillbaka uppefrån """
    def __init__(self, screen_w, screen_h, start_x, start_y, health=5, fall_speed=0.8, follow_speed=2):
        super().__init__()
        img = pygame.image.load("enemy2.png").convert_alpha()
        self.image = pygame.transform.scale(img, enemy_size)
        #position på skärm
        self.rect = self.image.get_rect(topleft=(start_x, start_y))

        self.screen_w = int(screen_w)
        self.screen_h = int(screen_h)

        self.health = int(health)
        self.fall_speed = float(fall_speed)
        self.follow_speed = float(follow_speed)

    def draw(self, surface):
        if self.health > 0:
            surface.blit(self.image, self.rect)    

    #enemy dör = stoppas uppdatering
    def update(self, player_rect=None):
        if self.health <= 0:
            self.kill()
            return
        
        # faller ner
        self.rect.y += self.fall_speed
        # tillbaka uppefrån
        if self.rect.top >= self.screen_h:
            self.rect.y = -enemy_size[1]

        # following player på x_led (om player finns)
        if player_rect is not None:
            target_x = player_rect.centerx

            #om är på player's vänster sidan gåt till höger (x ökar) och tvärtom
            if self.rect.centerx < target_x:
                self.rect.x += self.follow_speed
            elif self.rect.centerx > target_x:
                self.rect.x -= self.follow_speed

    def check_player_hits(self, player_sprite):
        if self.health <= 0:
            return 0
        
        #self=enemyB / player_sprite.bullets=grupp av bullets/om träffas tas bort bullet
        hits = pygame.sprite.spritecollide(self, player_sprite.bullets, dokill=True)
        attack = len(hits)
        if attack > 0:
            self.health -= attack
            if self.health <= 0:   
                self.kill()
        return attack
            
    
    # player träffar enemy eller inte
    def body_hit_player(self, player_sprite):
        if self.health <= 0:
            return False
        
        try:
            target_rect = player_sprite.rect
            
        except:
            target_rect = player_sprite
            
        if self.rect.colliderect(target_rect):
            player_sprite.lives -= 1   
            return True

        

#test part
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((900, 900))
    pygame.display.set_caption("Enemies")

    #att kontrollera spels hastighet
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

        
        #update enemies
        enemy_a.update(player_rect)
        enemy_b.update(player_rect)

        # die player
        if enemy_b.alive() and enemy_b.body_hit_player(player_rect):
            #Game Over
            screen.fill((30, 30, 30))
            font = pygame.font.SysFont(None, 48)
            msg = font.render("Game Over (EnemyB touched player)", True, (255, 80, 80))
            screen.blit(msg, (900//2 - msg.get_width()//2, 900//2 - msg.get_height()//2))
            pygame.display.update()
            pygame.time.delay(900)
            running = False

        #rita
        screen.fill((0, 130, 130))

        
        pygame.draw.rect(screen, (200, 200, 200), player_rect)

        
        enemy_a.draw(screen)
        enemy_b.draw(screen)

        pygame.display.update()

    pygame.quit()