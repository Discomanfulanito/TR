import pygame
from settings import *

class Tile(pygame.sprite.Sprite):

    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
               
        self.sprite_type = sprite_type
            
        if self.sprite_type == 'heaven':
            self.image = pygame.transform.scale(surface,(704*2,672*2))
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1]))
        elif self.sprite_type == 'deco':
            self.image= pygame.transform.scale(surface,(1179*2,955*2))
            self.rect = self.image.get_rect(topleft = (pos[0]+TILESIZE*0, pos[1]+TILESIZE*0))
        
        else:
            self.image = pygame.transform.scale(surface,(64,64))
            self.rect = self.image.get_rect(topleft = pos)
            
        # overlapping in Y dir
        self.hitbox = self.rect.inflate(0,-20)

