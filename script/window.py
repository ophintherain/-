# window.py
import pygame as pg
from setting import *
from sprites import *

class Popup_Store(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()  # 确保调用父类的构造函数
        self.game = game
        self.image = pg.image.load('asset/store.png').convert_alpha()
        # 根据store.png的实际大小来设置rect的位置和大小
        self.rect = self.image.get_rect(center=(self.game.screen.get_width() // 2, self.game.screen.get_height() // 2))
        self.open_store = True  # 弹出窗口是否打开
        self.setup_exit_button()  # 确保调用设置关闭按钮的方法

    def setup_exit_button(self):
        # 假设退出按钮的尺寸和位置，这里需要根据实际退出按钮的图片来设置
        self.closing_rect = pg.Rect(1010,75, 60, 60)
        
    def check_exit_click(self, event):
        # 检查是否点击了退出按钮区域
        if self.closing_rect and event.type == pg.MOUSEBUTTONDOWN:
            if self.closing_rect.collidepoint(pg.mouse.get_pos()):
                self.close()  # 调用关闭方法
                
    def close(self):
        # 关闭弹出窗口
        self.open_store = False
        if self in self.game.all_sprites:
            self.game.all_sprites.remove(self)
        self.game.popup_store = None  # 重置Game类中的弹出窗口引用

    def draw(self, surface):
        if self.open_store:
            surface.blit(self.image, self.rect)
            
class Popup_EventA(pg.sprite.Sprite):
    def __init__(self, game,level,position_index):
        super().__init__()  # 确保调用父类的构造函数
        self.game = game
        self.level = level
        self.position_index = position_index
        self.level.level_number = 1 if self.game.current_level == self.game.level1 else 2
        image_name = event_A_images.get((self.level.level_number, self.position_index), 'default.png')
        # 根据store.png的实际大小来设置rect的位置和大小
        self.image = pg.image.load(f'asset/{image_name}').convert_alpha()
        self.rect = self.image.get_rect(center=(self.game.screen.get_width() // 2, self.game.screen.get_height() // 2))
        self.open_eventa = True  # 弹出窗口是否打开
        self.surface_2=False
        self.setup_exit_button()  # 确保调用设置关闭按钮的方法
        self.animating=False
        self.image_name = image_name
        
    def setup_exit_button(self):
        # 定义圆形按钮的圆心坐标和半径
        if self.surface_2==False:
            self.closing_circle_center = pg.math.Vector2(817, 80)  # 圆心坐标
            self.closing_circle_radius = 30  # 半径
        else:
            self.closing_circle_center = pg.math.Vector2(800, 100)  # 圆心坐标
            self.closing_circle_radius = 32  # 半径

        
    def check_exit_click(self, event):

        self.setup_exit_button()
        # 检查是否点击了退出按钮区域
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.math.Vector2(pg.mouse.get_pos())
            # 计算鼠标点击位置与圆心的距离
            distance = self.closing_circle_center.distance_to(mouse_pos)
            # 检查点击是否在圆的范围内
            if distance <= self.closing_circle_radius:
                self.close()  # 调用关闭方法
                print("关闭按钮被点击了")
    
    def close(self):
        # 关闭弹出窗口
        self.open_eventa = False
        if self in self.game.all_sprites:
            self.game.all_sprites.remove(self)
        self.game.popup_eventa = None  # 重置Game类中的弹出窗口引用
        
    def change_image(self, new_image_name):
        # 更新图片名称和图片资源
        self.image=None
        print(f"{self.image}")
        self.image_name = new_image_name
        self.image = pg.image.load(new_image_name).convert_alpha()
        # 重新设置 rect，如果需要的话
        self.rect = self.image.get_rect(center=(self.game.screen.get_width() // 2, self.game.screen.get_height() // 2))
        self.surface_2=True
        # 根据 event_A_count 确定道具类型
        event_a_count = self.game.event_A_count
        tool_type = 'tool_a' if event_a_count <= 3 else 'tool_b' if event_a_count <= 6 else 'tool_c'
        
        # 检查 tool_type 是否有效，并更新 Tool 类的属性
        if hasattr(self.game.tool, tool_type):
            setattr(self.game.tool, tool_type, getattr(self.game.tool, tool_type, 0) + 1)
        
    # 在 draw 方法中添加动画更新逻辑
    def draw(self, surface):
        # 绘制图像
        surface.blit(self.image, self.rect)
        
class EventA_daoju(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        start_pos = (600, 700)
        target_pos = (850, 100)
        self.image = pg.image.load('asset/suipianbenti.png').convert_alpha()
        self.rect = self.image.get_rect(center=start_pos)
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.animation_duration = 300  # 动画持续时间1.5秒
        self.animation_start_time = pg.time.get_ticks()  # 记录动画开始时间
        self.animating = True  # 动画正在进行

    def update(self):
        # 仅当动画正在进行时更新位置
        if not self.animating:
            return

        # 计算经过的时间
        elapsed_time = pg.time.get_ticks() - self.animation_start_time

        # 计算当前动画的完成比例 [0, 1]
        progress = elapsed_time / self.animation_duration

        # 计算当前位置，使用线性插值
        current_pos = (
            self.rect.centerx + (self.target_pos[0] - self.rect.centerx) * progress,
            self.rect.centery + (self.target_pos[1] - self.rect.centery) * progress
        )

        # 更新精灵的位置
        self.rect = self.image.get_rect(center=current_pos)

        # 检查动画是否完成
        if elapsed_time >= self.animation_duration:
            self.animating = False
            self.image=None
            self.kill()  # 从精灵组中移除自己

    def draw(self,screen):
        if self.image:
            screen.blit(self.image, self.rect)
    
            
class Popup_EventB(pg.sprite.Sprite):
    def __init__(self, game,level,position_index):
        super().__init__()  # 确保调用父类的构造函数
        self.game = game
        self.level = level
        self.position_index = position_index
        self.level.level_number = 1 if self.game.current_level == self.game.level1 else 2
        image_name = event_B_images.get((self.level.level_number, self.position_index), 'default.png')
        # 根据store.png的实际大小来设置rect的位置和大小
        self.image = pg.image.load(f'asset/{image_name}').convert_alpha()
        self.rect = self.image.get_rect(center=(self.game.screen.get_width() // 2, self.game.screen.get_height() // 2))
        self.open_eventb = True  # 弹出窗口是否打开
        self.setup_exit_button()  # 确保调用设置关闭按钮的方法
        self.setup_activate_button() 
        self.animating=False
        

    def setup_exit_button(self):
        # 定义圆形按钮的圆心坐标和半径
        self.closing_circle_center = pg.math.Vector2(818, 80)  # 圆心坐标
        self.closing_circle_radius = 28  # 半径
        
    def check_exit_click(self, event):
        # 检查是否点击了退出按钮区域
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.math.Vector2(pg.mouse.get_pos())
            # 计算鼠标点击位置与圆心的距离
            distance = self.closing_circle_center.distance_to(mouse_pos)
            # 检查点击是否在圆的范围内
            if distance <= self.closing_circle_radius:
                self.close()  # 调用关闭方法
                print("关闭按钮被点击了")
                
    def setup_activate_button(self):
        self.activate_rect = pg.Rect(480,660, 220, 70)
        
    def check_activate_click(self, event):
        if self.activate_rect and event.type == pg.MOUSEBUTTONDOWN:
            if self.activate_rect.collidepoint(pg.mouse.get_pos()):
                self.activate(self.game)  # 调用关闭方法
                print("jihuo1")
                
    def close(self):
        # 关闭弹出窗口
        self.open_eventb = False
        if self in self.game.all_sprites:
            self.game.all_sprites.remove(self)
        self.game.popup_eventb = None  # 重置Game类中的弹出窗口引用
        
    def activate(self,game):
        game.glass_sound.play()
        shard = Shard(self.game)
        self.game.all_sprites.add(shard)
        reward = event_B_rewards.get((self.level.level_number, self.position_index), 0)
        # 增加碎片数量
        game.suipian.count += reward

# 在 draw 方法中添加动画更新逻辑
    def draw(self, surface):
        # 绘制图像
        surface.blit(self.image, self.rect)
        
class Popup_toolA(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()  # 确保调用父类的构造函数
        self.game = game
        self.image = pg.image.load('asset/toolA.png').convert_alpha()
        # 根据store.png的实际大小来设置rect的位置和大小
        self.rect = self.image.get_rect(center=(self.game.screen.get_width() // 2, self.game.screen.get_height() // 2))
        self.open_toolA = True  # 弹出窗口是否打开
        self.dice=Dice(self.game.screen.get_width() // 2-50, self.game.screen.get_height() // 2,0,is_tool_dice=True)
        self.game.special_sprites.add(self.dice)
        self.dice.roll()
        self.steps=self.dice.last_roll
        self.setup_exit_button

    def draw(self,surface):
        surface.blit(self.image,self.rect)
        
    def close(self):
        self.open_toolA = False
        if self in self.game.all_sprites:
            self.game.all_sprites.remove(self)
        if self in self.game.special_sprites:
            self.game.special_sprites.remove(self)
        self.dice.kill()
    
    def setup_exit_button(self):
        # 定义圆形按钮的圆心坐标和半径
        self.closing_circle_center = pg.math.Vector2(750, 175)  # 圆心坐标
        self.closing_circle_radius = 20  # 半径
 
    def check_exit_click(self, event):

        self.setup_exit_button()
        # 检查是否点击了退出按钮区域
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.math.Vector2(pg.mouse.get_pos())
            # 计算鼠标点击位置与圆心的距离
            distance = self.closing_circle_center.distance_to(mouse_pos)
            # 检查点击是否在圆的范围内
            if distance <= self.closing_circle_radius:
                self.close()  # 调用关闭方法
                print("关闭按钮被点击了")
                self.game.player_sprite.move_to_next_position(self.steps)
        
class Popup_toolC(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()  # 确保调用父类的构造函数
        self.game = game
        self.image = pg.image.load('asset/toolC.png').convert_alpha()
        # 根据store.png的实际大小来设置rect的位置和大小
        self.rect = self.image.get_rect(center=(self.game.screen.get_width() // 2, self.game.screen.get_height() // 2))
        self.open_toolC = True  # 弹出窗口是否打开

    def draw(self,surface):
        surface.blit(self.image,self.rect)
        
    def close(self):
        self.open_toolC = False
        if self in self.game.all_sprites:
            self.game.all_sprites.remove(self)
            
class Tool_Afei(pg.sprite.Sprite):
    def __init__(self,game) :
        super().__init__()
        self.game = game
        start_pos = (300, 300)
        target_pos = (820, 700)
        self.image = pg.image.load('asset/tool_afei.png').convert_alpha()
        self.rect = self.image.get_rect(center=start_pos)
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.animation_duration = 300  # 动画持续时间1.5秒
        self.animation_start_time = pg.time.get_ticks()  # 记录动画开始时间
        self.animating = True  # 动画正在进行
        print("animating")
        
    def update(self):
        # 仅当动画正在进行时更新位置
        if not self.animating:
            return

        # 计算经过的时间
        elapsed_time = pg.time.get_ticks() - self.animation_start_time

        # 计算当前动画的完成比例 [0, 1]
        progress = elapsed_time / self.animation_duration

        # 计算当前位置，使用线性插值
        current_pos = (
            self.rect.centerx + (self.target_pos[0] - self.rect.centerx) * progress,
            self.rect.centery + (self.target_pos[1] - self.rect.centery) * progress
        )

        # 更新精灵的位置
        self.rect = self.image.get_rect(center=current_pos)
        
        # 根据动画进度计算缩放比例
        scale_factor = (1 - progress)  # 从1开始逐渐减小到0
        
        # 计算新的宽度和高度
        new_width = int(self.rect.width * scale_factor)
        new_height = int(self.rect.height * scale_factor)
        
        # 设置最小尺寸为80x80
        min_width = 100
        min_height = 100

        # 确保尺寸不会小于最小值
        new_width = max(new_width, min_width)
        new_height = max(new_height, min_height)
        
        # 更新图像尺寸
        self.image = pg.transform.scale(self.image, (new_width, new_height))

        # 检查动画是否完成
        if elapsed_time >= self.animation_duration:
            self.image = pg.transform.scale(self.image, (min_width, min_height))
            self.animating = False
            self.image=None
            self.kill()  # 从精灵组中移除自己

    def draw(self,screen):
        if self.image:
            screen.blit(self.image, self.rect)
            
class Tool_Bfei(pg.sprite.Sprite):
    def __init__(self,game) :
        super().__init__()
        self.game = game
        start_pos = (600, 300)
        target_pos = (950, 700)
        self.image = pg.image.load('asset/tool_bfei.png').convert_alpha()
        self.rect = self.image.get_rect(center=start_pos)
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.animation_duration = 500  # 动画持续时间1.5秒
        self.animation_start_time = pg.time.get_ticks()  # 记录动画开始时间
        self.animating = True  # 动画正在进行
        
    def update(self):
        # 仅当动画正在进行时更新位置
        if not self.animating:
            return

        # 计算经过的时间
        elapsed_time = pg.time.get_ticks() - self.animation_start_time

        # 计算当前动画的完成比例 [0, 1]
        progress = elapsed_time / self.animation_duration

        # 计算当前位置，使用线性插值
        current_pos = (
            self.rect.centerx + (self.target_pos[0] - self.rect.centerx) * progress,
            self.rect.centery + (self.target_pos[1] - self.rect.centery) * progress
        )

        # 更新精灵的位置
        self.rect = self.image.get_rect(center=current_pos)
        
        # 根据动画进度计算缩放比例
        scale_factor = (1 - progress)  # 从1开始逐渐减小到0
        
        # 计算新的宽度和高度
        new_width = int(self.rect.width * scale_factor)
        new_height = int(self.rect.height * scale_factor)
        
        # 设置最小尺寸为80x80
        min_width = 100
        min_height = 100

        # 确保尺寸不会小于最小值
        new_width = max(new_width, min_width)
        new_height = max(new_height, min_height)
        
        # 更新图像尺寸
        self.image = pg.transform.scale(self.image, (new_width, new_height))

        # 检查动画是否完成
        if elapsed_time >= self.animation_duration:
            self.image = pg.transform.scale(self.image, (min_width, min_height))
            self.animating = False
            self.image=None
            self.kill()  # 从精灵组中移除自己

    def draw(self,screen):
        if self.image:
            screen.blit(self.image, self.rect)
            
class Tool_Cfei(pg.sprite.Sprite):
    def __init__(self,game) :
        super().__init__()
        self.game = game
        start_pos = (900, 300)
        target_pos = (1100, 700)
        self.image = pg.image.load('asset/tool_cfei.png').convert_alpha()
        self.rect = self.image.get_rect(center=start_pos)
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.animation_duration = 500  # 动画持续时间1.5秒
        self.animation_start_time = pg.time.get_ticks()  # 记录动画开始时间
        self.animating = True  # 动画正在进行
        
    def update(self):
        # 仅当动画正在进行时更新位置
        if not self.animating:
            return

        # 计算经过的时间
        elapsed_time = pg.time.get_ticks() - self.animation_start_time

        # 计算当前动画的完成比例 [0, 1]
        progress = elapsed_time / self.animation_duration

        # 计算当前位置，使用线性插值
        current_pos = (
            self.rect.centerx + (self.target_pos[0] - self.rect.centerx) * progress,
            self.rect.centery + (self.target_pos[1] - self.rect.centery) * progress
        )

        # 更新精灵的位置
        self.rect = self.image.get_rect(center=current_pos)
        
        # 根据动画进度计算缩放比例
        scale_factor = (1 - progress)  # 从1开始逐渐减小到0
        
        # 计算新的宽度和高度
        new_width = int(self.rect.width * scale_factor)
        new_height = int(self.rect.height * scale_factor)
        
        # 设置最小尺寸为80x80
        min_width = 100
        min_height = 100

        # 确保尺寸不会小于最小值
        new_width = max(new_width, min_width)
        new_height = max(new_height, min_height)
        
        # 更新图像尺寸
        self.image = pg.transform.scale(self.image, (new_width, new_height))

        # 检查动画是否完成
        if elapsed_time >= self.animation_duration:
            self.image = pg.transform.scale(self.image, (min_width, min_height))
            self.animating = False
            self.image=None
            self.kill()  # 从精灵组中移除自己

    def draw(self,screen):
        if self.image:
            screen.blit(self.image, self.rect)
        
class Shard(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        start_pos = (600, 700)
        target_pos = (850, 100)
        self.image = pg.image.load('asset/suipianbenti.png').convert_alpha()
        self.rect = self.image.get_rect(center=start_pos)
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.animation_duration = 300  # 动画持续时间1.5秒
        self.animation_start_time = pg.time.get_ticks()  # 记录动画开始时间
        self.animating = True  # 动画正在进行

    def update(self):
        # 仅当动画正在进行时更新位置
        if not self.animating:
            return

        # 计算经过的时间
        elapsed_time = pg.time.get_ticks() - self.animation_start_time

        # 计算当前动画的完成比例 [0, 1]
        progress = elapsed_time / self.animation_duration

        # 计算当前位置，使用线性插值
        current_pos = (
            self.rect.centerx + (self.target_pos[0] - self.rect.centerx) * progress,
            self.rect.centery + (self.target_pos[1] - self.rect.centery) * progress
        )

        # 更新精灵的位置
        self.rect = self.image.get_rect(center=current_pos)

        # 检查动画是否完成
        if elapsed_time >= self.animation_duration:
            self.animating = False
            self.image=None
            self.kill()  # 从精灵组中移除自己

    def draw(self,screen):
        if self.image:
            screen.blit(self.image, self.rect)
            


