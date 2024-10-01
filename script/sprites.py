# sprites.py  
import pygame as pg  
import random
from setting import * 

class Player(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game=game
        self.image = pg.image.load('asset/mc.png').convert_alpha()
        self.rect = self.image.get_rect(bottomleft=(270, 250))  # 精灵出生
        self.change_y = 0  # 垂直速度
        self.change_x = 0  # 水平速度
        self.position = 0
        self.temp_position = False
        self.m_current_position_index = 0
        self.positions=positions_level1
        self.animating = False  # 动画正在进行
        self.animation_duration = 1000  # 动画持续时间1.5
        self.e_current_position_index=-3
        
    def update(self):
        self.rect.y += self.change_y  # 改变y坐标实现上下移动
        self.rect.x += self.change_x  # 改变x坐标实现左右移动
        
        # m_next_position_index = self.m_current_position_index + 1

        # next_position = self.positions[m_next_position_index]
        
        # if not self.animating:
        #     return

        # # 计算经过的时间
        # elapsed_time = pg.time.get_ticks() - self.animation_start_time

        # # 计算当前动画的完成比例 [0, 1]
        # progress = elapsed_time / self.animation_duration

        # # 计算当前位置，使用线性插值
        # current_pos = (
        #     self.rect.centerx + (next_position[0] - self.rect.centerx) * progress,
        #     self.rect.centery + (next_position[1] - self.rect.centery) * progress
        # )

        # # 更新精灵的位置
        # self.rect = self.image.get_rect(center=current_pos)
        
        # if elapsed_time >= self.animation_duration:
        #     self.animating = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def move_to_next_position(self, steps):
        
        m_target_position_index = self.m_current_position_index + steps

        # 检查是否到达终点
        if m_target_position_index >= len(self.positions):
            # 到达终点，游戏结束
            self.game.change_level()  # 假设game对象有一个方法来处理关卡切换
            return
        if self.game.current_level == self.game.level2:
            self.e_current_position_index+=3
            if m_target_position_index <=self.e_current_position_index:
                self.game.lost_end()
                return

        # 移动到下一个位置
        # self.animation_start_time = pg.time.get_ticks() 
        # self.animation=True
        self.move(steps-1)
        
        # 检测事件
        self.judge_position()
             
    def move(self, steps):
        
        # 获取下一步位置
        m_next_position_index = self.m_current_position_index + 1
        
        current_position = self.positions[self.m_current_position_index]
        next_position = self.positions[m_next_position_index]
        
        dx = next_position[0] - current_position[0]
        dy = next_position[1] - current_position[1]
        print(f"主角位置: ({next_position[0]}, {next_position[1] })")  # 打印玩家当前位置
        
        # 计算向量的长度
        distance_to_target = (dx**2 + dy**2)**0.5

        # 更新玩家位置
        self.rect.x += distance_to_target * (dx / distance_to_target)
        self.rect.y += distance_to_target * (dy / distance_to_target)
        
        # 更新玩家已经走过的距离
        self.m_current_position_index = self.m_current_position_index + 1
        
        self.game.update()
    
        # 如果还有步骤需要移动，则继续移动
        if steps >= 1:
            self.move(steps - 1)
            
    def judge_position(self):
        # 获取当前关卡编号和位置索引
        level_number = 1 if self.game.current_level == self.game.level1 else 2
        # 检查当前位置是否触发事件 A
        if (level_number, self.m_current_position_index) in eventa_positions:
            self.game.event_A()  # 触发事件 A
        if (level_number, self.m_current_position_index) in eventb_positions:
            self.game.event_B()  # 触发事件 B
        if (level_number, self.m_current_position_index) in store_positions:
            self.game.event_C()  # 触发事件 C
        print("judge_position")
        
    def change_level(self, level_positions):
        self.positions = level_positions  # 更新位置列表
        self.m_current_position_index = 0  # 重置当前位置索引
        self.rect = self.image.get_rect(bottomleft=level_positions[0])     
        
class Enemy(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game=game
        self.image = pg.image.load('asset/enemy.png').convert_alpha()
        self.e_current_position_index = 0
        self.positions=positions_level2
        self.rect = self.image.get_rect(bottomleft=(487, 440))    # 精灵出生
        self.change_y = 0  # 垂直速度
        self.change_x = 0  # 水平速度
        self.position = 0
        self.temp_position = False
        
    def e_move_to_next_position(self,steps):
        
        e_target_position_index = self.e_current_position_index + steps

        # 移动到下一个位置
        self.move(steps-1)

        
    def move(self, steps):
        
        print(f"步数: ({steps})")  # 打印玩家当前位置
        print(f"位置: ({self.e_current_position_index})")  # 打印玩家当前位置
         
        # 获取下一步位置
        e_next_position_index = self.e_current_position_index + 1
        
        current_position = self.positions[self.e_current_position_index]
        next_position = self.positions[e_next_position_index]
        
        dx = next_position[0] - current_position[0]
        dy = next_position[1] - current_position[1]
        print(f"敌人位置: ({next_position[0]}, {next_position[1] })")  # 打印玩家当前位置

        # 计算向量的长度
        distance_to_target = (dx**2 + dy**2)**0.5

        # 更新玩家位置
        self.rect.x += distance_to_target * (dx / distance_to_target)
        self.rect.y += distance_to_target * (dy / distance_to_target)
        
        # 更新玩家已经走过的距离
        self.e_current_position_index = self.e_current_position_index + 1
        
        pg.display.update()
    
        # 如果还有步骤需要移动，则继续移动
        if steps >= 1:
            self.move(steps - 1)
        
    def update(self):
        self.rect.y += self.change_y  # 改变y坐标实现上下移动
        self.rect.x += self.change_x  # 改变x坐标实现左右移动

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    
class Dice(pg.sprite.Sprite):
    def __init__(self, x, y,index,is_tool_dice=False):
        super().__init__()
        self.die_images = [pg.image.load(f'asset/{num}.png').convert_alpha() for num in range(1, 7)]
        self.chosen_image = pg.image.load('asset/7.png').convert_alpha()
        self.image = self.chosen_image  # 初始化时显示第一张图
        self.rect = self.image.get_rect(topleft=(x, y))
        self.last_roll = None
        self.rolling = False  # 新增标志，表示骰子是否在滚动
        self.roll_time = 0  # 新增变量，用于控制滚动时间
        self.roll_duration = 1000  # 滚动持续时间，单位为毫秒
        self.selected = False  # 新增标志，表示骰子是否被选中
        self.is_first_roll = True
        self.index=index
        self.is_tool_dice = is_tool_dice 
        self.norepeat=1
        
    def roll(self):
        if self.is_first_roll and not self.is_tool_dice:
            # 设置第一次摇骰子的预定点数，这里我们使用预设序列 [1, 2, 1, 2]
            self.last_roll = [1, 2, 1, 2][self.index % 4]  # 假设self.index是骰子的索引
            self.rolling = True
            self.roll_time = pg.time.get_ticks()
            self.is_first_roll = False  # 重置标志
        else:
            # 正常随机摇骰子
            self.rolling = True
            self.last_roll = random.randint(1, 6)
            if self.last_roll==self.norepeat:
                self.last_roll = random.randint(1, 6)
            self.fangchongfu=self.last_roll
            
            self.roll_time = pg.time.get_ticks()
        return self.last_roll
        
    def update(self):
        if self.rolling:
            current_time = pg.time.get_ticks()
            # 检查是否达到了滚动持续时间
            if current_time - self.roll_time > self.roll_duration:
                # 停止滚动，并更新骰子图像为最终的随机数字
                self.rolling = False
                self.image = self.die_images[self.last_roll-1]
            else:
                # 如果还在滚动时间内，可以在这里实现滚动动画效果
                # 例如，这里我们简单地改变骰子的图像
                self.image = self.die_images[(int)((current_time / 100)%38) % 6]
        # 如果不在滚动状态，则保持当前图像不变
                pass
            

    def draw(self, surface):
        if self.selected:
            # 如果骰子被选中
            self.image = self.chosen_image
            
        surface.blit(self.image, self.rect)
        
    def check_click(self, pos):
        # 检查鼠标点击位置是否在骰子区域内
        return self.rect.collidepoint(pos)
    
class Suipian(pg.sprite.Sprite):
    def __init__(self,screen):
        super().__init__()
        self.screen = screen
        self.image = pg.image.load("asset/suipian.png").convert_alpha()
        self.rect = self.image.get_rect(bottomleft=(750, 200))
        self.count=9
    
    def draw(self, screen):
        # 绘制图像
        screen.blit(self.image, self.rect)
        # 调用 count_suipian 方法来绘制文本
        self.count_suipian(screen)
        
    def count_suipian(self, screen):
        font_suipian_path = pg.font.match_font("Akzidenz-Grotesk BQ Extended")
        font = pg.font.Font(font_suipian_path, 100)
        text = f"{self.count}"
        text_surface = font.render(text, True, (101, 65, 32))
        text_rect = text_surface.get_rect(center=(1000, 100))
        screen.blit(text_surface, text_rect)
        
class Tool(pg.sprite.Sprite):
    def __init__(self,screen):
        super().__init__()
        self.screen = screen
        self.image = pg.image.load("asset/tool.png").convert_alpha()
        self.rect = self.image.get_rect(bottomleft=(730, 800))
        self.tool_a=5
        self.tool_b=5
        self.tool_c=5
        
    def draw(self, screen):
        # 绘制图像
        screen.blit(self.image, self.rect)
        self.count_tool(screen)
        
    def count_tool(self, screen):
        font_tool_path = pg.font.match_font("Akzidenz-Grotesk BQ Extended")
        font = pg.font.Font(font_tool_path, 50)
        text_a = f"{self.tool_a}"
        text_b = f"{self.tool_b}"
        text_c = f"{self.tool_c}"
        text_a_surface = font.render(text_a, True, (101, 65, 32))
        text_a_rect = text_a_surface.get_rect(center=(810, 777))
        screen.blit(text_a_surface, text_a_rect)
        text_b_surface = font.render(text_b, True, (101, 65, 32))
        text_b_rect = text_b_surface.get_rect(center=(955, 777))
        screen.blit(text_b_surface, text_b_rect)
        text_c_surface = font.render(text_c, True, (101, 65, 32))
        text_c_rect = text_c_surface.get_rect(center=(1100, 777))
        screen.blit(text_c_surface, text_c_rect)
    
    def update_tool(self, tool_type, increment=1):
        if hasattr(self, tool_type):
            setattr(self, tool_type, getattr(self, tool_type) + increment)
        

