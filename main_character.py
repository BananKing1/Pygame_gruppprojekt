import pygame, sys, math
from boss_file import Boss, Beam

Color_bullet = (255, 230, 0)
Color_player= (120, 160, 255)
Color_text = (220, 70, 70)
FPS = 60
Debug = False


class Infinite_Background:
    def __init__(self, screen_width, screen_height, bg_path):
        self.bg = pygame.image.load(bg_path).convert()
        self.bg_width  = self.bg.get_width()
        self.bg_height = self.bg.get_height()

        self.scroll = 0
        self.tiles = math.ceil(screen_width / self.bg_width) + 1
        
        self.screen_width = screen_width
        self.screen_height = screen_height

    def draw(self, screen, scroll_speed):
        # Draw scrolling background
        for i in range(self.tiles):
            screen.blit(self.bg, (i * self.bg_width + self.scroll, 0))

        # Update scroll
        self.scroll -= scroll_speed
        if abs(self.scroll) >= self.bg_width:
            self.scroll = 0
# skapar en kula med startposition x,y och med hastigheten 10, samt storlek bredd, höjd
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=10):
        super().__init__()
        self.image = pygame.Surface((20,30), pygame.SRCALPHA)
        self.image.fill((Color_bullet))
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = speed
    
    def update(self):
        # flyttar sig uppåt varje gång
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()
    
# Spelaren position, hastighet, kantmarginal så att den inte går ut från fönstrets kant osv.    
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=6, margin = 30):
        super().__init__()
        img = pygame.image.load("alienBeige_stand.png").convert_alpha()
        self.image = pygame.transform.scale(img, (100, 100))
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = speed
        self.margin = margin
        self.bullets = pygame.sprite.Group()


        # Den här delen flyytar figuren runt i spelet med tangenterna och skjuter kulor med space
    def handle_keys(self, keys, width, height):
        if keys[pygame.K_LEFT] and self.rect.left > self.margin:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < width - self.margin:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > self.margin:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < height - self.margin:
            self.rect.y += self.speed

    # det gör att man inte kan skjuta jättemånga kulor samtidigt, om det inte finns några kulor ute eller är minst 50 pixlar uppåt så skapas en ny kula
    def shoot(self):
        if len(self.bullets) == 0:
            self.bullets.add(Bullet(self.rect.centerx, self.rect.top))
            return
        
        last = self.bullets.sprites()[-1]
        if (self.rect.centery - last.rect.centery) > 50:
            self.bullets.add(Bullet(self.rect.centerx, self.rect.top))
                                  

    # Flyttar alla kulor och tar bort de som har flugit utanför skärmen
    def update(self):
        self.bullets.update()


def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0))
    width, height = screen.get_size()
    pygame.display.set_caption("shooter - sprite-version")
    screen = pygame.display.set_mode((width, height))

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)

    background = Infinite_Background(width, height, "backgrounds/boss_bg_img.png")
    player = Player(width//2, height - 80)
    lives = 3

    enemy_bullets = pygame.sprite.Group()
    
    boss = Boss(width, height)
    beam = Beam(boss.rect.centerx, boss.rect.centery)

    lives = 5

    all_sprites = pygame.sprite.Group(player)
    
    running = True
    while running:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                elif e.key == pygame.K_SPACE:
                    player.shoot()

        keys = pygame.key.get_pressed()
        player.handle_keys(keys, width, height)  

        all_sprites.update()
        boss.wiggle()
        beam.move_beam(player.rect, boss)

        hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        if hits:
            lives -= len(hits)
            print(f"The player got shooted! Lives left: {lives}")

            if lives <= 0:
                print("The player died! Game Over")
                running = False

            lives = beam.beam_hit_player(player.rect, boss, lives)
            if lives <= 0: 
                print("The player died! Game over")
                running = False

        background.draw(screen, scroll_speed=5)
        all_sprites.draw(screen)
        player.bullets.draw(screen)

        screen.blit(boss.image, boss.rect)
        screen.blit(beam.image, beam.rect)

        # skriver "liv: 3" i röd text uppe till vänster
        text = font.render(f"Lives: {lives}", True, Color_text)
        screen.blit(text, (10, 10))

        pygame.display.flip()
    pygame.quit()
    sys.exit()
if __name__ == "__main__": 
    main()
