import pygame
import random
import math


"""Big bad boss actions >:D"""
class Boss(pygame.sprite.Sprite):
    # x and y are screen width and height
    def __init__(self, sw, sh, boss_health): 
        super().__init__()
        # load og sprite
        original_sprite = pygame.image.load("sprites/shipYellow_manned.png").convert_alpha()

        # scale sprite
        scale = 2 
        self.scale = scale # saving for boss_dies
        new_width = original_sprite.get_width() * scale
        self.new_height = original_sprite.get_height() * scale # save for boss_dies()
        self.image = pygame.transform.scale(original_sprite, (new_width, self.new_height))

        # create hit box
        self.rect = self.image.get_rect()
       
        # save desired position for shake()
        self.pos_x = (sw-new_width)/2-100
        self.pos_y = sh/9

        # Set start position (before moving into frame)
        self.rect.x = (sw-new_width)/2
        self.rect.y = 0-self.new_height

        # Save boss health
        self.health = boss_health

    # for boss shaking and staying in frame
    def shake(self):
        # shake horiziontally
        if self.rect.x < self.pos_x + 100:
            self.rect.x += 1
        elif self.rect.x > self.pos_x-100 : # boss moves into frame
            self.rect.x -= 1
        else:
            self.rect.x += random.choice([-1, 1])

        # shake vertically
        #boss move into frame (from top)
        if self.rect.y < self.pos_y:
            self.rect.y += 5
        elif self.rect.y > self.pos_y +50:
            self.rect.y -= 1
        else:
            self.rect.y += random.choice([-1, 1])

    def boss_dies(self):
        # load dead sprite for boss
        dead_sprite = pygame.image.load("sprites/alienYellow_hurt.png").convert_alpha()

        # scale sprite
        scale = self.scale 
        new_width = dead_sprite.get_width() * scale
        new_height = dead_sprite.get_height() * scale # save for boss_dies()
        self.image = pygame.transform.scale(dead_sprite, (new_width, new_height))

        if self.rect.y > 0-self.new_height:
            self.rect.y -= random.choice([1, 3, 5])
            self.rect.x -= random.choice([-1, 1])


    # boss health and death
    def take_damage(self, bullets):
        # check for collision between boss and player bullet
        if pygame.sprite.spritecollide(self, bullets, True):
            self.health -= 1
            print("Boss health:", self.health) 
        if self.health <= 0:
            print("You win, yippie!")

        return self.health

        


"""Boss BEAM XD"""
class Beam(pygame.sprite.Sprite):
    def __init__(self, beam_speed, beam_damage, boss):
        super().__init__()

        # load og sprite
        original_img = pygame.image.load("sprites/laserYellow_burst.png").convert_alpha()

        # scale sprite
        scale = 1/2
        new_width = original_img.get_width() * scale
        new_height = original_img.get_height() * scale
        self.image = pygame.transform.scale(original_img, (new_width, new_height))
        
        # create hitbox
        self.rect = self.image.get_rect()

        self.rect.x = boss.rect.center[0]
        self.rect.y = boss.rect.center[1]

        # save beam_speed for shoot_beam()
        self.beam_speed = beam_speed
        self.beam_damage = beam_damage

    # shoot beam to player, beam continues to chase player
    def shoot_beam(self, player): 
        # find player and beam center coordinates
        player_center = player.rect.center
        beam_center = self.rect.center 

        # if the beam is to the left or right of the player, move towards the player
        if player_center[0] < beam_center[0]:
            self.rect.x -= self.beam_speed
        elif player_center[0] > beam_center[0]:
            self.rect.x += self.beam_speed

        # if the beam is to the top or bottom of the player, move towards the player
        if player_center[1]  < beam_center[1]:
            self.rect.y -= self.beam_speed
        elif player_center[1] > beam_center[1]:
            self.rect.y += self.beam_speed
    
    # check collision between beam and player
    def beam_hit_player(self, player, player_health, boss):
        # find boss center coordinates
        boss_center  = boss.rect.center

        # Check collision between beam and player
        if player.rect.colliderect(self.rect):

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
        super().__init__()
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

    # reset to x=0 once asteroid has reached left side of screen
    def throw_asteroid(self, speed, sw):
        if self.rect.x > 0-self.new_width:
            self.rect.x -= speed
        else:
            self.rect.x = sw + self.new_width
            self.rect.y = random.randint(0, 750)

    # Player collide with asteroid
    def collided_asteroid(self, player, player_health, sw):
        if player.rect.colliderect(self.rect):
            # reset asteroid position (right side of screen, random y)
            self.rect.x = sw
            self.rect.y = random.randint(0, 750)
            
            # Decrease health on hit
            player_health -= self.asteroid_damage  
            print("Player health:", player_health)
        return player_health # return new health



"""Scrolling background for boss fight"""          
class Infinite_Background:
    def __init__(self, sw, bg_path):
        # load background
        self.bg = pygame.image.load(bg_path).convert()
        self.bg_width  = self.bg.get_width()

        self.scroll = 0
        # the numbers of pictures ti fill the screen
        self.tiles = math.ceil(sw / self.bg_width) + 1
        
        # save screen width and height for draw_background()
        self.screen_width = sw

    def draw_background(self,screen, scroll_speed):
        # Draw scrolling background
        for i in range(self.tiles):
            screen.blit(self.bg, (i * self.bg_width + self.scroll, 0))

        # Update scroll
        self.scroll -= scroll_speed
        if abs(self.scroll) >= self.bg_width:
            self.scroll = 0 
    