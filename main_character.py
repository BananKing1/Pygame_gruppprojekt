import pygame, sys, math

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
class Bullet:
    def __init__(self, x, y, speed = 10):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 6
        self.height = 10
    
    def update(self):
        # flyttar sig uppåt varje gång
        self.y -= self.speed

        # när kular går över skärmen så tas kulan bort
    def outside(self):
        return self.y < 0
    
    def draw(self, screen):
        pygame.draw.rect(screen, Color_bullet, (self.x, self.y, self.width, self.height))
    
# Spelaren position, hastighet, kantmarginal så att den inte går ut från fönstrets kant osv.    
class Player:
    def __init__(self, x, y, speed=6, margin = 30):
        self.x = x
        self.y = y
        self.speed = speed
        self.margin = margin
        self.bullet = []
        self.image = None

        try: 
            img = pygame.image.load("alienBeige_stand.png").convert_alpha()
            #skalar bilden på skärmen
            self.image = pygame.transform.scale(img, (50, 50))
        except Exception: 
            self.image = None
            self.fallback_size = 40

        # Den här delen flyytar figuren runt i spelet med tangenterna och skjuter kulor med space
    def handle_keys(self, keys, width, height):
        if keys[pygame.K_LEFT] and self.x > self.margin:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < width - self.margin:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > self.margin:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < height - self.margin:
            self.y += self.speed

    # det gör att man inte kan skjuta jättemånga kulor samtidigt, om det inte finns några kulor ute eller är minst 50 pixlar uppåt så skapas en ny kula
    def shoot(self):
        if len(self.bullet) == 0 or self.bullet[-1].y < self.y - 50:
            self.bullet.append(Bullet(self.x, self.y))

    # Flyttar alla kulor och tar bort de som har flugit utanför skärmen
    def update_bullets(self):
        for k in self.bullet[:]:
            k.update()
            if k.outside():
                self.bullet.remove(k)
    
    # Ritar antingen bilden, eller en blå fyrkant om bilden saknas
    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x - self.image.get_width()//2, self.y - self.image.get_height()//2 ))

        else:
            pygame.draw.rect(
            screen, Color_player,
            (self.x - self.fallback_size//2, self.y - self.fallback_size//2,
            self.fallback_size, self.fallback_size)
            )
        # Ritar kulorna
        for k in self.bullet:
            k.draw(screen)

def main():
    pygame.init()
    # gör ett spelfönster som är 600 x 400
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    # håller koll på tiden så att spelet inte går för snabbt
    clock = pygame.time.Clock()
    # används för texten liv
    font = pygame.font.SysFont(None, 30)

    background = Infinite_Background(width, height, "backgrounds/boss_bg_img.png")
    # skapar spelaren mitt på skärmen, och sen är spelet igång
    player = Player(width//2, height - 80)
    lives = 3
    running = True

    # körs 60 gånger per sekund
    while running:
        clock.tick(FPS)
        # om man stänger fönstret så avslutas spelet
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        # flyttar spelaren
        keys = pygame.key.get_pressed()
        player.handle_keys(keys, width, height)
        # skjuter med mellanslag
        if keys[pygame.K_SPACE]:
            player.shoot()

        player.update_bullets()
        #bakgrunden, samt ritar spelaren och kulorna
    
        background.draw(screen, scroll_speed=5)
        player.draw(screen)

        # skriver "liv: 3" i röd text uppe till vänster
        text = font.render(f"Lives: {lives}", True, Color_text)
        screen.blit(text, (10, 10))

        pygame.display.flip()
    pygame.quit()
    sys.exit()
if __name__ == "__main__": 
    main()
