import pygame
import random
import math


"""Big bad boss actions XD"""
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_img = pygame.image.load("sprites/shipYellow_manned.png").convert_alpha()

        # Scale sprite
        scale_factor = 2  
        new_width = original_img.get_width() * scale_factor
        new_height = original_img.get_height() * scale_factor
        
        self.image = pygame.transform.scale(original_img, (new_width, new_height))
        # Create rect
        self.rect = self.image.get_rect()
       
        # Save center position for wiggle movement
        self.center_x = x - 300
        self.center_y = y - 500

        # Set initial position
        self.rect.x = self.center_x
        self.rect.y = self.center_y

        # Boss health
        self.health = 10  

    def move(self):
        # Horizontal wiggle
        if self.rect.x < self.center_x - 100:
            self.rect.x += 1
        elif self.rect.x > self.center_x + 100:
            self.rect.x -= 1
        else:
            self.rect.x += random.choice([-1, 1])

        # Vertical wiggle
        if self.rect.y < self.center_y - 100:
            self.rect.y += 1
        elif self.rect.y > self.center_y + 100:
            self.rect.y -= 1
        else:
            self.rect.y += random.choice([-1, 1])

    """Handle boss taking damage"""
    def take_damage(self, amount):
        self.health -= amount
        print("Boss Health:", self.health)
        if self.health <= 0:
            print("Boss defeated!")
            self.kill()


"""Boss beam actions XD"""
class Beam(Boss):
    def __init__(self, x, y):
        super().__init__(x, y)  # pass x, y to Boss

        original_img = pygame.image.load("sprites/laserYellow_burst.png").convert_alpha()

        scale_factor = 1/2
        new_width = original_img.get_width() * scale_factor
        new_height = original_img.get_height() * scale_factor

        self.image = pygame.transform.scale(original_img, (new_width, new_height))
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 15
    
    def move_beam(self, player, boss):
        player_center = player.center  # pygame.Rect.center
        boss_center = boss.rect.center  # Boss rect

        dx = player_center[0] - boss_center[0]
        dy = player_center[1] - boss_center[1]

        magnitude = (dx ** 2 + dy ** 2) ** 0.5

        if magnitude != 0:
            self.velocity = [dx / magnitude * self.speed, dy / magnitude * self.speed]
        else:
            self.velocity = [0, 0]

        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
    
    def beam_hit_player(self, player, boss, health):
        # Check collision between BEAM and PLAYER
        if self.rect.colliderect(player):
            health -= 1
            print("Health:", health)

            # Reset beam back to boss's position
            self.rect.center = boss.rect.center  

        return health


"""Asteroid actions XD"""
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, scale_factor):
        super().__init__()
        original_img = pygame.image.load("sprites/spinner.png").convert_alpha()
                
        # Scale sprite
        self.scale_factor = scale_factor
        new_width = original_img.get_width() * scale_factor
        new_height = original_img.get_height() * scale_factor

        self.image = pygame.transform.scale(original_img, (new_width, new_height))
        self.rect = self.image.get_rect(center=(x, y))

    def move_asteroid(self, speed, size, sw, sh):
        self.rect.x -= speed
        if self.rect.x < -size:
            self.rect.x = sw+100
            self.rect.y = random.randint(10, sh - size)


    def bullet_hit_asteroid(self, bullets, enemy, sw, sh, score):
        for bullet in bullets[:]:
            if bullet['rect'].colliderect(enemy):
                bullets.remove(bullet)
                enemy.x = sw
                enemy.y = random.randint(0, sh)

                score += 100
                print("Score:", score)
        return score

    # Health = asteroid.collided_asteroid(player, asteroid, health, SCREEN_WIDTH)
    def collided_asteroid(self, object1, object2, health, sw):
        if object1.colliderect(object2):
            # Move object2 to a new position
            object2.x = sw
            object2.y = random.randint(0, 750)
            health -= 1  # Decrease health on hit
            print("Health:", health)
        return health
    
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