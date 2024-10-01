# camera.py
import pygame as pg  
from setting import *

class CameraGroup(pg.sprite.Group):
    def __init__(self, screen, background_image):
        super().__init__()
        self.screen = screen
        self.display_surface = pg.display.get_surface()
        
        # 镜头偏移
        self.offset = pg.math.Vector2()
        self.half_w=self.display_surface.get_size()[0]
        self.half_h=self.display_surface.get_size()[1]
        
        # 背景
        self.ground_surf=background_image
        self.ground_rect=self.ground_surf.get_rect(topleft=(0,0)) 
        
        # 键盘速度
        self.keyboard_speed=20
        
        # 两种状况
        self.is_free_camera = True
        
    def center_target_camera(self,target):
        self.offset.x=target.rect.centerx-self.half_w/2
        self.offset.y=target.rect.centery-self.half_h/2
        
    def keyboard_control(self):
        keys=pg.key.get_pressed()
        if keys[pg.K_a]:
            self.offset.x -= self.keyboard_speed
        if keys[pg.K_d]:
            self.offset.x += self.keyboard_speed
        if keys[pg.K_w]:
            self.offset.y -= self.keyboard_speed
        if keys[pg.K_s]:
            self.offset.y += self.keyboard_speed

    def custom_draw(self,player):
        if  self.is_free_camera:
            self.keyboard_control()
        else:
            self.center_target_camera(player)
            
        # 限制镜头偏移量y的范围
        if self.offset.y > 1600:
            self.offset.y = 1600
        elif self.offset.y < 0:
            self.offset.y = 0
            
        if self.offset.x > 1750:
            self.offset.x = 1750
        elif self.offset.x < 0:
            self.offset.x = 0
        # 背景偏移
        ground_offset=self.ground_rect.topleft-self.offset
        self.display_surface.blit(self.ground_surf,ground_offset)
        
        for sprite in self.sprites():
            offset_pos=sprite.rect.topleft-self.offset
            self.display_surface.blit(sprite.image,offset_pos)