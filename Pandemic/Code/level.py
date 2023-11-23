import pygame
from settings import TILESIZE
from tile import Tile
from player import Player

from support import import_csv_layout, import_folder
from ia import IA

class Level():
    
    def __init__(self):
        
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.talkable_sprites = pygame.sprite.Group()
        self.talk_sprites = pygame.sprite.Group()
        
        self.create_map()

    def create_map(self):
        heaven      = True
        deco        = True

        layouts = {
            'boundary'      :    import_csv_layout('../Map/Level 0_floor blocks.csv'),
            'hell'      :    import_csv_layout('../Map/Level 0_paredes sur.csv'),
            'player'        :    import_csv_layout('../Map/Level 0_player.csv'),
            'heaven'      :    import_csv_layout('../Map/Level 0_segunda planta.csv'),
            'heaven_walls'      :    import_csv_layout('../Map/Level 0_paredes segunda planta.csv'),
            'IA'            : import_csv_layout('../Map/Level 0_IA.csv'),
            'deco'          : import_csv_layout('../Map/Level 0_deco.csv')
        }

        for style , layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index*TILESIZE
                        y = row_index*TILESIZE
                        if style == 'boundary': 
                            Tile((x,y), [self.obstacle_sprites], 'invisible', surface = pygame.image.load('../Images/stop block.png'))

                        if style == 'hell':
                            
                            surf = pygame.image.load(f'../Images/walls/{int(col)}.png')
                            Tile((x,y), [self.visible_sprites], 'hell_walls', surf)
                        

                        if style == 'player':
                            self.player = Player((x,y),[self.visible_sprites], self.obstacle_sprites)
                        
                        
                        if style == 'heaven' and heaven:
                            
                            surf = pygame.image.load('../Images/heaven.png')
                            Tile((x,y), [self.visible_sprites], 'heaven', surf)
                            heaven = False
                            
                        if style == 'heaven_walls':
                            surf = pygame.image.load(f'../Images/walls/{int(col)}.png')
                            Tile((x,y), [self.visible_sprites], 'heaven_walls', surf)

                        if style == 'IA':

                            IA((x,y),
                             [self.visible_sprites, self.talkable_sprites], 
                             self.obstacle_sprites)

                        if style == 'deco' and deco:
                            deco = False
                            surf = pygame.image.load(f'../Images/deco.png')
                            Tile((x,y), [self.visible_sprites], 'deco', surf)

                            

                    
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.ia_update(self.player)

        
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general set-up
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] //2
        self.half_height = self.display_surface.get_size()[1] //2

        self.offset = pygame.math.Vector2(100,200)
        
        # Floor
        self.floor_surface = pygame.image.load('../Images/hell.png').convert()
        self.floor_surface = pygame.transform.scale(self.floor_surface, (2944, 2240))
        self.floor_rect = self.floor_surface.get_rect(topleft=(0,0))
    
    def ia_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and  sprite.sprite_type == 'IA']

        for enemy in enemy_sprites:
            enemy.ia_update(player)


    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for sprite in sorted(self.sprites(), key = lambda sprite : sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
    

