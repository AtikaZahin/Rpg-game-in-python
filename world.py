from character import Character
import constants
from items import Item

class World():
    def __init__(self):
        self.map_tiles= []
        self.obstale_tiles = []
        self.exit_tile = None
        self.item_list = []
        self.player = None
        self.character_list = []

    def process_data(self,data,tile_list, item_images,mob_animations):
        self.level_length = len(data)
        #iterate through each value in level data
        for y,row in enumerate(data):
            for x,tile in enumerate(row):
                if tile >= 0:
                    img = tile_list[tile]
                    img_rect = img.get_rect()
                    img_x =x * constants.TILE_SIZE
                    img_y = y * constants.TILE_SIZE
                    img_rect.x = img_x
                    img_rect.y = img_y
                    #img_rect.center = (img_x,img_y)
                    tile_data = [img,img_rect, img_x, img_y]

                    if tile ==7:
                        self.obstale_tiles.append(tile_data)
                    elif tile == 8:
                        #exit tile
                        self.exit_tile = tile_data 
                    elif tile == 9:
                        coin = Item(img_x, img_y, 0, item_images[0])
                        self.item_list.append(coin)
                        tile_data[0] = tile_list[0]  # Replace the image with the coin image
                    elif tile == 10:
                        potion = Item(img_x, img_y, 1, [item_images[1]])
                        self.item_list.append(potion) 
                        tile_data[0] = tile_list[0]
                    elif tile == 11:
                        player = Character(img_x,img_y,100, mob_animations,0, False,1)
                        self.player = player
                        tile_data[0] = tile_list[0]
                    elif tile >= 12 and tile <= 16:
                        enemy = Character(img_x,img_y,100, mob_animations, tile - 11,False,1)  # Adjust the enemy type based on tile value
                        #add enemy to the main tile list
                        self.character_list.append(enemy)
                        tile_data[0] = tile_list[0]
                    elif tile == 17 :
                        #add boss
                        enemy = Character(img_x,img_y,100, mob_animations, 6,True,2)
                        self.character_list.append(enemy)
                        tile_data[0] = tile_list[0]
                   

                    #add image data to  main tile list
                    if tile>=0:
                        self.map_tiles.append(tile_data)

    def update(self, screen_scroll):
        for tile in self.map_tiles:
            # Update the position of the tile rect based on the scroll
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2] , tile[3])


    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])