import pygame
import csv
import constants
from character import Character
from weapon import Weapon
from items import Item
from world import World

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")

#create clock for fps
clock = pygame.time.Clock()

#define game variables
level = 1
start_intro = False
screen_scroll =[0,0]  #x,y scroll

#define player movemnet variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

#define font
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)

#helper function to scale image
def scale_img(image , scale):
    w = image.get_width()
    h = image.get_height()
    new_image = pygame.transform.scale(image ,(w*scale , h* scale))
    return new_image

#load health bar images
heart_empty = scale_img(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(), constants.ITEM_SCALE)
heart_full = scale_img(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(), constants.ITEM_SCALE)
heart_half = scale_img(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(), constants.ITEM_SCALE)

#load coin images
coin_image =[]
for x in range(4):
    img = scale_img(pygame.image.load(f"assets/images/items/coin_f{x}.png").convert_alpha(),constants.ITEM_SCALE)
    coin_image.append(img)

#load potion images
red_potion= scale_img(pygame.image.load("assets/images/items/potion_red.png").convert_alpha(), constants.POTION_SCALE)

item_images =[]
item_images.append(coin_image)
item_images.append(red_potion)

#load weapon images
bow_image =scale_img (pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), constants.WEAPON_SCALE)
arrow_image =scale_img (pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPON_SCALE)
fireball_image =scale_img (pygame.image.load("assets/images/weapons/fireball.png").convert_alpha(), constants.FIREBALL_SCALE)


#load tile images
tile_list = []
for i in range(constants.TILE_TYPES):
    tile_image = pygame.image.load(f"assets/images/tiles/{i}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
    tile_list.append(tile_image)


#load character images
mob_animations = []
mob_types =["elf","imp","skeleton","goblin","muddy","tiny_zombie","big_demon"]
animation_types=["idle", "run"]

for mob in mob_types:
    
    #load images
    animation_list = []

    for animation in animation_types:
        #reset temporary list of images 
        temp_list =[]
        for i in range (4):
            img = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
            img = scale_img(img ,constants.SCALE) 
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

#function foroutputing health and score
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#FUNCTION FOR DISPPLAYING GAME INFO
def draw_info():

    #draw panel
    pygame.draw.rect(screen, constants.PANEL, (0, 0, constants.SCREEN_WIDTH, 50)) 
    pygame.draw.line(screen, constants.WHITE, (0, 50), (constants.SCREEN_WIDTH, 50))

    #draw lives
    half_heart_drawn = False
    for i in range(5):
        if i < player.health >=((i+1)*20):
            screen.blit(heart_full, ( i * 50+10, 0))

        elif player.health %20 >0 and half_heart_drawn == False:
            screen.blit(heart_half, ( i * 50+10, 0)) 
            half_heart_drawn = True
        else:
            screen.blit(heart_empty, ( i * 50+10, 0)) 

    
    #level
    draw_text(f"Level {level}", font, constants.WHITE, constants.SCREEN_WIDTH/2, 15)


    #show score
    draw_text(f"X {player.score}", font, constants.WHITE, constants.SCREEN_WIDTH -100,15)

#fuction to reset level
def reset_level():
    damage_text_group.empty()
    arrow_group.empty()
    item_group.empty()
    fireball_group.empty()

    #create emptuy tiles list
    data =[]
    for row in range(constants.ROWS):
        r =[-1] * constants.COLUMNS
        data.append(r)
    return data
    

#damage text class
class DamageText(pygame.sprite.Sprite):


    def __init__(self, x, y, damage,color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0

    def update(self):
        #Reposition the text based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        #move the text up
        self.rect.y -= 1
        #delete the counter after a few seconds
        self.counter += 1
        if self.counter > 30:  # Adjust the number to control how long the text stays
            self.kill()  # Remove the sprite from all groups
        
#class for handling screwen fade
class ScreenFade:
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0


    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:
            pygame.draw.rect(screen, self.color, (0-self.fade_counter, 0, constants.SCREEN_WIDTH//2, constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen,self.color,(constants.SCREEN_WIDTH //2 + self.fade_counter,0 ,constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))

        if self.fade_counter>= constants.SCREEN_WIDTH:
            fade_complete = True
        return fade_complete

#create empty world data list with 150 rows and 150 columns
world_data =[]
for row in range(constants.ROWS):
    r =[-1] * constants.COLUMNS
    world_data.append(r)

#load level data and create csv file
with open(f"levels/level{level}_data.csv", newline ="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for y, row in enumerate(reader):
        for x, tile in enumerate(row):
            world_data[y][x] = int(tile)

world = World()
world.process_data(world_data, tile_list,item_images, mob_animations)


#create player
player = world.player

#create player's weapon
bow = Weapon(bow_image,arrow_image)

#extract enemies from the world data
enemy_list = world.character_list


#create sprite groups
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()

score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_image,True)
item_group.add(score_coin)
#add the items from the level data
for item in world.item_list:
    item_group.add(item)

#create screen fade
intro_fade = ScreenFade(1, constants.BLACK, 4)
death_fade = ScreenFade(1, constants.RED, 4)

#main game loop
run = True
while run:

    #control fps
    clock.tick(constants.FPS)

    screen.fill(constants.BG)

    if player.alive:
    #calculate player movement
        dx= 0
        dy =0

        if moving_right == True:
            dx= constants.SPEED
        if moving_left == True:
            dx=-constants.SPEED
        if moving_up == True:
            dy = -constants.SPEED
        if moving_down == True:
            dy = constants.SPEED

        #move player
        screen_scroll, level_complete=player.move(dx,dy,world.obstale_tiles,world.exit_tile)

        #update all objects
        world.update(screen_scroll)
        for enemy in enemy_list:
            fireball =enemy.ai(player,world.obstale_tiles,screen_scroll, fireball_image)
            if fireball:
                fireball_group.add(fireball)
            if enemy.alive:
                enemy.update()

        #update player
        player.update()
        arrow = bow.update(player)
        if arrow:
            arrow_group.add(arrow)
        for arrow in arrow_group:
            damage , damage_pos =arrow.update(screen_scroll,world.obstale_tiles,enemy_list)
            if damage :
                damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
                damage_text_group.add(damage_text)
        damage_text_group.update()
        fireball_group.update(screen_scroll,player)
        item_group.update(screen_scroll,player)


    #draw player on screen
    world.draw(screen)
    for enemy in enemy_list:
        
        enemy.draw(screen)

    player.draw(screen)
    bow.draw(screen)

    for arrow in arrow_group:
        arrow.draw(screen)
    for fireball in fireball_group:
        fireball.draw(screen)
    damage_text_group.draw(screen)
    item_group.draw(screen)
    draw_info() 
    score_coin.draw(screen)

    #check level complete
    if level_complete:
        start_intro = True
        level += 1
        world_data =reset_level() 
        #load level data and create csv file
        with open(f"levels/level{level}_data.csv", newline ="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for y, row in enumerate(reader):
                for x, tile in enumerate(row):
                    world_data[y][x] = int(tile)

        world = World()
        world.process_data(world_data, tile_list,item_images, mob_animations)
        temp_hp = player.health
        temp_score = player.score
        player = world.player
        player.health = temp_hp
        player.score = temp_score
        enemy_list = world.character_list
        score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_image,True)
        item_group.add(score_coin)
        for item in world.item_list:
            item_group.add(item)
       

        
    #show intro screen
    if start_intro:
        if intro_fade.fade():
            start_intro = False
            intro_fade.fade_counter = 0

    #show death screen
    if player.alive == False:
        death_fade.fade()

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #take keyboard presses
        if event.type ==pygame.KEYDOWN:
            if event.key ==pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right= True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True


        #check for key released
        if event.type ==pygame.KEYUP:
            if event.key ==pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right= False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False

    pygame.display.update()

pygame.quit()