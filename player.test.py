import pygame, sys
from boss import Boss, Beam, Infinite_Background
from player import Player

Color_text = (220, 70, 70)
FPS = 60

def main():
    pygame.init()
    # Skärmstorlek
    screen = pygame.display.set_mode((0, 0))
    width, height = screen.get_size()
    pygame.display.set_caption("Namn för spelen")

    # Tidskontroll
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)

    # Skapar bakgrunden
    background = Infinite_Background(width, height, "backgrounds/boss_bg_img.png")
    # Spelaren position mitt på skärmen
    player = Player(width//2, height - 80)
    player.lives = 3

    # Group för fienden kulor
    enemy_bullets = pygame.sprite.Group()

    # Skapa bossen
    boss = Boss(width, height)
    beam = Beam(boss.rect.centerx, boss.rect.centery, width, height)
    
    running = True
    while running:
        clock.tick(FPS)
        # stänger spelet vid klick på X
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                # Tryck ESC för att avsluta spelet
                if e.key == pygame.K_ESCAPE:
                    running = False
                elif e.key == pygame.K_SPACE:
                    player.shoot()
        #input och rörelse
        # Spelarens förflyttnig, uppdaterar kulorna
        keys = pygame.key.get_pressed()
        player.handle_keys(keys, width, height)  
        player.update()
        enemy_bullets.update()

        # Boss och Beam
        boss.wiggle()
        # Beam rör sig mot spelaren
        beam.move_beam(player.rect, boss)
        # Beamen återställs om den lämnar skärmen
        beam.beam_reset(boss)

        # Kollisioner
        # träffas från vanliga fiender
        hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        if hits:
            player.lives -= len(hits)  # Tar bort liv vid träff
            print(f"The player got shot! Lives left: {player.lives}")

        # bossen beam träffar spelaren
        player.lives = beam.beam_hit_player(player.rect, boss, player.lives)

        # Game Over
        if player.lives <= 0: 
            print("The player died! Game Over")
            running = False
        # Rita
        background.draw(screen, scroll_speed=5)
        screen.blit(boss.image, boss.rect)
        screen.blit(beam.image, beam.rect)
        screen.blit(player.image, player.rect)
        player.bullets.draw(screen)
        enemy_bullets.draw(screen)

        # skriver "liv: 3" i röd text uppe till vänster
        text = font.render(f"Lives: {player.lives}", True, Color_text)
        screen.blit(text, (10, 10))

        pygame.display.flip()
    pygame.quit()
    sys.exit()
if __name__ == "__main__": 
    main()