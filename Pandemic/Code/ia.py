from entity import Entity
import pygame
from support import import_folder
import tkinter as tk
from openai_api import OPENAI_API

class IA(Entity):

    def __init__(self, pos,  groups, obstacle_sprites):
        super().__init__(groups)
        
        self.sprite_type = 'IA'

        self.import_graphics()
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.animation_speed = 0.10
        self.rect = self.image.get_rect(bottomright = pos)
        self.hitbox  = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites

        self.interact_radius = 200
        
    def import_graphics(self):

        self.animations = {'idle':[], 'jump':[]}
        main_path = f'../Images/Robot/'

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path+animation)
    
    def animate(self):
        animation = self.animations[self.status]
        # Loop over the frame index
        self.frame_index += self.animation_speed


        if self.frame_index >= len(animation):
            self.frame_index=0

        # setting the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(bottomright = self.hitbox.center)
    
    def get_player_distance(self, player):
        ia_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec-ia_vec).magnitude()

        return distance

    def get_status(self, player):

        distance = self.get_player_distance(player)
        if distance <= self.interact_radius:
            self.status='jump'
        else:
            self.status = 'idle'

    def actions(self):
        if self.status =='idle':
            pass
        if self.status == 'jump':
            keys = pygame.key.get_pressed()
            if keys[pygame.K_t]:
                    chat_bot = OPENAI_API()
                    chat_bot.talk()
        else:
            pass

        
    def update(self):
        self.animate()    

    def ia_update(self, player):
        self.get_status(player)
        self.animate()
        self.actions()
    