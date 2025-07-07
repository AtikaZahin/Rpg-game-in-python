import pygame

class Item(pygame.sprite.Sprite):

    def __init__(self, x, y,item_type, animation_list, dummy_coin = False):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type #0 is the coin , #1 is the heart
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dummy_coin = dummy_coin  # If True, the item will not be collected


    def update(self,screen_scroll,player):
        #does't apply to the dummy coin at the header
        if not self.dummy_coin:
            #move the item based on the scroll
            self.rect.x += screen_scroll[0]
            self.rect.y += screen_scroll[1]


        #check to see if item is collected
        if self.rect.colliderect(player.rect):
            #coin collected
            if self.item_type == 0:
                player.score += 1
            elif self.item_type == 1:
                #heart collected
                player.health += 10
                if player.health > 100:
                    player.health = 100
            self.kill()

        #handle animation cooldown
        animation_cooldown = 150
        self.image = self.animation_list[self.frame_index]
        # check if enough time passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            #check if the frame index is out of bounds
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)