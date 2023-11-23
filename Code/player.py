from support import import_folder
import pygame
from settings import *
from entity import Entity

class Player(Entity):

    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        
        self.image = pygame.image.load(r'../Images/Player/right/1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        # overlapping in Y dir
        self.hitbox = self.rect.inflate(0,-13)

        
        self.import_player_assets()
        self.status = 'right'
        self.obstacle_sprites = obstacle_sprites
    
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status:
                self.status = self.status + '_idle'

    def import_player_assets(self):

        player_path = '../Images/Player/'
        self.animations = {'left':[], 'right':[],
                            'right_idle':[], 'left_idle':[]}

        for animation in self.animations.keys():
                full_path = player_path + animation
                self.animations[animation] = import_folder(full_path)

    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.direction.y = -1
            
        elif keys[pygame.K_DOWN]:
           self.direction.y = 1
          
        else:
            self.direction.y = 0
        
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

    def animate(self):

        animation = self.animations[self.status]
        # Loop over the frame index
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index=0

        # setting the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.input()
        self.animate()
        self.get_status()
        self.move(8)