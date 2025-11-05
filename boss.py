import pygame
import random
import math


"""Big bad boss actions XD"""
class Boss(pygame.sprite.Sprite):
    # x and y are screen width and height
    def __init__(self, x, y, boss_health): 
        # load og sprite
        original_sprite = pygame.image.load("sprites/shipYellow_manned.png").convert_alpha()

        # scale sprite
        scale = 2  
        new_width = original_sprite.get_width() * scale
        new_height = original_sprite.get_height() * scale
        self.image = pygame.transform.scale(original_sprite, (new_width, new_height))
        
        # create hit box
        self.rect = self.image.get_rect()
       
        # save desired position for shake()
        self.pos_x = (x-new_width)/2-100
        self.pos_y = y/9

        # Set start position (before moving into frame)
        self.rect.x = (x-new_width)/2
        self.rect.y = 0-new_height

        # Save boss health
        self.health = boss_health

    # for boss shaking and staying in frame
    def shake(self):
        # shake left and right
        if self.rect.x < self.pos_x + 100:
            self.rect.x += 1
        elif self.rect.x > self.pos_x-100 : # boss moves into frame
            self.rect.x -= 1
        else:
            self.rect.x += random.choice([-1, 1])

        # shake up and down
        #boss move into frame
        if self.rect.y < self.pos_y:
            self.rect.y += 5
        elif self.rect.y > self.pos_y +50:
            self.rect.y -= 1
        else:
            self.rect.y += random.choice([-1, 1])

    # boss health and death
    def take_damage(self):
        self.health -= 1
        print("Boss health:", self.health)
        if self.health <= 0:
            print("You win, yippie!")


"""Boss BEAM XD"""
class Beam(Boss):
    def __init__(self, beam_speed, beam_damage, boss):
        # load og sprite
        original_img = pygame.image.load("sprites/laserYellow_burst.png").convert_alpha()

        # scale sprite
        scale = 1/2
        new_width = original_img.get_width() * scale
        new_height = original_img.get_height() * scale
        self.image = pygame.transform.scale(original_img, (new_width, new_height))
        
        # create hitbox
        self.rect = self.image.get_rect()
        self.beam_center = boss.rect.center

        # save beam_speed for shoot_beam()
        self.beam_speed = beam_speed
        self.beam_damage = beam_damage

    # shoot beam to player from boss
    def shoot_beam(self, player, boss): 
        player_center = player.center 
        boss_center = boss.rect.center 

        if player_center[0] < self.beam_center[0]:
            self.rect.x -= self.beam_speed
        elif player_center[0] > self.beam_center[0]:
            self.rect.x += self.beam_speed
        else:
            pass

        if player_center[1] < self.beam_center[1]:
            self.rect.y -= self.beam_speed
        elif player_center[1] > self.beam_center[1]:
            self.rect.y += self.beam_speed
        else:
            pass


    
    # check collision between beam and player
    def beam_hit_player(self, player, player_health, boss):
        # find boss center coordinates
        boss_center  = boss.rect.center

        # Check collision between beam and player
        if self.rect.colliderect(player):

            # player takes damage
            player_health -= 1
            print("Player health:", player_health)

            # Reset beam to boss center
            self.rect.center = boss_center  
        
        # return new player health
        return player_health
    
    
    # reset beam position (middle of boss) if it goes off screen
    def beam_reset(self, sw, sh, boss):
        # for the y-axis
        if self.rect.y < 0 or self.rect.y > sh:
            self.rect.center = boss.rect.center
        # for the x-axis
        if self.rect.x < 0 or self.rect.x > sw:
            self.rect.center = boss.rect.center
    


"""Asteroid woohoo XD"""
class Asteroid(pygame.sprite.Sprite):
    # attributes: sw (screen width), sh (screen height)
    def __init__(self, sw, sh, scale, asteroid_damage):
        # load og sprite
        original_sprite = pygame.image.load("sprites/spinner.png").convert_alpha()
                
        # scale sprite and save new width and height for throw_asteroid()
        self.new_width =  original_sprite.get_width() * scale
        self.new_height =  original_sprite.get_height() * scale
        self.image = pygame.transform.scale( original_sprite, (self.new_width,  self.new_height))
        
        # create hitbox
        self.rect = self.image.get_rect()

        # Set start position (right side of screen, random y)
        self.rect.x = sw
        self.rect.y = random.randint(10, sh - self.new_width)

        # Save asteroid damage (for collided_asteroid())
        self.asteroid_damage = asteroid_damage

    # reset x once asteroid has reached left side of screen
    def throw_asteroid(self, speed, sw):
        if self.rect.x > 0-self.new_width:
            self.rect.x -= speed
        else:
            self.rect.x = sw + self.new_width
            self.rect.y = random.randint(0, 750)

    # Player collide with asteroid
    def collided_asteroid(self, object1, asteroid, player_health, sw):
        if object1.colliderect(asteroid):
            # reset asteroid position (right side of screen, random y)
            asteroid.x = sw
            asteroid.y = random.randint(0, 750)
            
            # Decrease health on hit
            player_health -= self.asteroid_damage  
            print("Player health:", player_health)
        return player_health # return new health


"""Scrolling background for boss fight"""          
class Infinite_Background:
    def __init__(self, sw, sh, bg_path):
        # load background
        self.bg = pygame.image.load(bg_path).convert()
        self.bg_width  = self.bg.get_width()
        self.bg_height = self.bg.get_height()

        self.scroll = 0
        self.tiles = math.ceil(sw / self.bg_width) + 1
        
        self.screen_width = sw
        self.screen_height = sh

    def draw_background(self, screen, scroll_speed):
        # Draw scrolling background
        for i in range(self.tiles):
            screen.blit(self.bg, (i * self.bg_width + self.scroll, 0))

        # Update scroll
        self.scroll -= scroll_speed
        if abs(self.scroll) >= self.bg_width:
            self.scroll = 0