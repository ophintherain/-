# level.py
import pygame as pg
from camera import *
from sprites import *
class Level1:
    def __init__(self,game):
        self.game=game
        self.background_image = pg.image.load('asset/map1.png')

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))

class Level2:
    def __init__(self,game,screen):
        self.game=game
        self.screen=screen
        self.background_image = pg.image.load('asset/map2.png')
        self.camera_group = CameraGroup(self.screen,self.background_image)  # 初始化摄像机组
        self.player_sprite = game.player_sprite
        self.camera_group.add(self.player_sprite)

    def update(self):
        # 更新关卡2特有的状态，可能包括摄像机逻辑
        pass

    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))
        self.camera_group.custom_draw(self.player_sprite)
    # def draw(self, screen):
        # self.camera_group.update_camera(screen)  # 更新摄像机位置
        # self.camera_group.draw(screen)  # 使用摄像机绘制屏幕
    def add_enemy_to_camera(self, enemy_sprite):
        self.enemy_sprite = enemy_sprite
        self.camera_group.add(self.enemy_sprite)