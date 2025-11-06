import pygame

Color_bullet = (255, 230, 0)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=10):
        super().__init__()

        self.image = pygame.Surface((20,30), pygame.SRCALPHA)
        self.image.fill((Color_bullet))
        # Startposition
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = speed
    
    def update(self):
        #Flyttar kulan uppåt
        self.rect.y -= self.speed
        # Tar bort kulan när den lämnar skärmen
        if self.rect.bottom < 0:
            self.kill()
    
# Spelarens startposition, hastighet, kantmarginal, kulgrupp och startliv   
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=6, margin = 30):
        super().__init__()
        img = pygame.image.load("alienBeige_stand.png").convert_alpha()
        self.image = pygame.transform.scale(img, (100, 100))
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = speed
        self.margin = margin
        self.bullets = pygame.sprite.Group()
        self.lives = 3


        # Tangenter som styr spelet
    def handle_keys(self, keys, width, height):
        if keys[pygame.K_LEFT] and self.rect.left > self.margin:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < width - self.margin:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > self.margin:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < height - self.margin:
            self.rect.y += self.speed

    
    def shoot(self):
        # Skjut en kula om inga finns ute
        if len(self.bullets) == 0:
            self.bullets.add(Bullet(self.rect.centerx, self.rect.top))
            return
        # Avståndet till senaste kula
        last = self.bullets.sprites()[-1]
        if (self.rect.centery - last.rect.centery) > 50:
            # Skapa ny kula
            self.bullets.add(Bullet(self.rect.centerx, self.rect.top))                 

    def update(self):
        # Uppdaterar alla kulor
        self.bullets.update()

    def on_boss_spawn(self):
        # När bossen kommer får spelaren 5 liv
        self.lives = 5

    def check_enemy_hits(self, enemy_bullets):
        # Kollar om spelaren träffas av fiendekulor
        hits = pygame.sprite.spritecollide(self, enemy_bullets, True)
        if hits:
            self.lives -= len(hits)  # Minska liv per träff
            print(f"Got shot! Lives left: {self.lives}")
        return self.lives

    def check_beam_hit(self, beam, boss):
        # Kollar om bossens beam träffas spelaren
        self.lives = beam.beam_hit_player(self.rect, boss, self.lives)
        # Stoppa negativa liv
        if self.lives < 0:
            self.lives = 0

    def is_dead(self):
        # Returnerar True om liv = 0
        return self.lives <= 0