from random import random
import pygame
import math
import random
import constants
class Weapon():
    def __init__(self, image, arrow_image):
        self.original_image = image
        self.angle =0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.arrow_image = arrow_image
        self.rect = self.image .get_rect()
        self.fire = False
        self.last_shot = pygame.time.get_ticks()

    def update (self, player):
        shot_cooldown = 300
        arrow = None
        self.rect.center = player.rect.center

        pos = pygame.mouse.get_pos()
        x_dist=pos[0] - self.rect.centerx
        y_dist=-(pos[1] - self.rect.centery)
        self.angle = math.degrees(math.atan2(y_dist,x_dist))

        #get mouse clicks
        if pygame.mouse.get_pressed()[0] and self.fire == False and (pygame.time.get_ticks()- self.last_shot )> shot_cooldown:
            #HERE ZERO IS THE LEFT MOUSE BUTTON
            arrow = Arrow(self.arrow_image,self.rect.centerx,self.rect.centery, self.angle)
            self.fire= True
            self.last_shot = pygame.time.get_ticks()
        #rest mouse click
        if pygame.mouse.get_pressed()[0] == False:
            self.fire = False

        return arrow

    def draw (self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image,((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height())/2))

class Arrow (pygame.sprite.Sprite):

    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image 
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center =(x,y)
        #calculate the horizonatal and verticular speed baded on the angle
        self.speed = 10
        self.dx =   math.cos(math.radians(self.angle)) * constants.ARROW_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * constants.ARROW_SPEED)
        #negtuve y because the origin is at the top left corner

    def update (self, screen_scroll,obstacle_tiles,enemy_list):

        #reset variables
        damage = 0
        damage_pos = None

        #reposition the arrow based on the speed and angle
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        #check for collision between arrow and tiles
        for obstacle in obstacle_tiles:
            if self.rect.colliderect(obstacle[1]):
                #if the arrow collides with an obstacle, remove it
                self.kill()
                

        #check if the arrow is out of bounds
        if self.rect.right< 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom< 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill()  # remove the arrow if it goes out of bounds

            #check collision with enemies
        for enemy in enemy_list:
           if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage =10 +random.randint(-5,5)
                damage_pos = enemy.rect
                enemy.health -= damage
                enemy.hit = True
                self.kill()  # remove the arrow if it hits an enemy
                break
        return damage, damage_pos


    def draw (self,surface):
        surface.blit(self.image,((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height())/2))


class Fireball (pygame.sprite.Sprite):

    def __init__(self, image, x, y, target_x, target_y):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image 
        x_dist = target_x - x
        y_dist = -(target_y - y)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center =(x,y)
        #calculate the horizonatal and verticular speed baded on the angle
        self.speed = 10
        self.dx =   math.cos(math.radians(self.angle)) * constants.FIREBALL_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * constants.FIREBALL_SPEED)
        #negtuve y because the origin is at the top left corner

    def update (self, screen_scroll,player):
        #reposition the arrow based on the speed and angle
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        #check if the fire is out of bounds
        if self.rect.right< 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom< 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill()  # remove the arrow if it goes out of bounds

         #check collision with enemies
        if player.rect.colliderect(self.rect) and player.hit == False:
            player.hit = True
            player.last_hit = pygame.time.get_ticks()
            player.health -= 10 
            self.kill()



    def draw (self,surface):
        surface.blit(self.image,((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height())/2))

