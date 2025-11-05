import pygame, sys

Färg_kula = (255, 230, 0)
Färg_spelare = (120, 160, 255)
Färg_bakgrund = (20, 20, 30)
Färg_text = (220, 70, 70)
FPS = 60
Debug = False

# skapar en kula med startposition x,y och med hastigheten 10, samt storlek bredd, höjd
class Kula:
    def __init__(self, x, y, fart = 10):
        self.x = x
        self.y = y
        self.fart = fart
        self.bredd = 6
        self.höjd = 10
    
    def uppdatera(self):
        # flyttar sig uppåt varje gång
        self.y -= self.fart

        # när kular går över skärmen så tas kulan bort
    def utanför(self):
        return self.y < 0
    
    def rita(self, skärm):
        pygame.draw.rect(skärm, Färg_kula, (self.x-3, self.y - 10, self.bredd, self.höjd))
    
# Spelaren position, hastighet, kantmarginal så att den inte går ut från fönstrets kant osv.    
class Spelare:
    def __init__(self, x, y, fart=6, marginal = 30):
        self.x = x
        self.y = y
        self.fart = fart
        self.marginal = marginal
        self.kulor = []
        self.bild = None

        try: 
            img = pygame.image.load("alienBeige_stand.png").convert_alpha()
            #skalar bilden på skärmen
            self.bild = pygame.transform.scale(img, (50, 50))
        except Exception: 
            self.bild = None
            self.fallback_size = 40

        # Den här delen flyytar figuren runt i spelet med tangenterna och skjuter kulor med space
    def tangenter(self, keys, bredd, höjd):
        if keys[pygame.K_LEFT] and self.x > self.marginal:
            self.x -= self.fart
        if keys[pygame.K_RIGHT] and self.x < bredd - self.marginal:
            self.x += self.fart
        if keys[pygame.K_UP] and self.y > self.marginal:
            self.y -= self.fart
        if keys[pygame.K_DOWN] and self.y < höjd - self.marginal:
            self.y += self.fart

    # det gör att man inte kan skjuta jättemånga kulor samtidigt, om det inte finns några kulor ute eller är minst 50 pixlar uppåt så skapas en ny kula
    def skjut(self):
        if len(self.kulor) == 0 or self.kulor[-1].y < self.y - 50:
            self.kulor.append(Kula(self.x, self.y))

    # Flyttar alla kulor och tar bort de som har flugit utanför skärmen
    def uppdaterar_kulor(self):
        for k in self.kulor[:]:
            k.uppdatera()
            if k.utanför():
                self.kulor.remove(k)
    
    # Ritar antingen bilden, eller en blå fyrkant om bilden saknas
    def rita(self, skärm):
        if self.bild:
            skärm.blit(self.bild, (self.x - self.bild.get_width()//2, self.y - self.bild.get_height()//2 ))

        else:
            pygame.draw.rect(
            skärm, Färg_spelare,
            (self.x - self.fallback_size//2, self.y - self.fallback_size//2,
            self.fallback_size, self.fallback_size)
            )
        # Ritar kulorna
        for k in self.kulor:
            k.rita(skärm)

def main():
    pygame.init()
    # gör ett spelfönster som är 600 x 400
    bredd, höjd = 600, 400
    skärm = pygame.display.set_mode((bredd, höjd))
    # håller koll på tiden så att spelet inte går för snabbt
    clock = pygame.time.Clock()
    # används för texten liv
    font = pygame.font.SysFont(None, 30)

    # skapar spelaren mitt på skärmen, och sen är spelet igång
    spelare = Spelare(bredd//2, höjd - 80)
    liv = 3
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
        spelare.tangenter(keys, bredd, höjd)
        # skjuter med mellanslag
        if keys[pygame.K_SPACE]:
            spelare.skjut()

        spelare.uppdaterar_kulor()
        #bakgrunden, samt ritar spelaren och kulorna
        skärm.fill(Färg_bakgrund)
        spelare.rita(skärm)

        # skriver "liv: 3" i röd text uppe till vänster
        text = font.render(f"Liv: {liv}", True, Färg_text)
        skärm.blit(text, (10, 10))

        pygame.display.flip()
    pygame.quit()
    sys.exit()
if __name__ == "__main__": 
    main()
