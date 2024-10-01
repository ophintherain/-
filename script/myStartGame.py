import pygame as pg
import sys
from setting import *
from sprites import *
from pygame.locals import *
from camera import *
from window import *
from level import *

class Game:
    def __init__(self):
        pg.init()
        
        self.end1_image = pg.image.load('asset/end1.png')
        self.end2_image = pg.image.load('asset/end2.png')
        
        # 摄像机
        self.is_free_camera=True
        
        # 事件A计数
        self.event_A_count=0
        
        # 设置窗口
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        
        # 加载音频
        pg.mixer.init()

        # 加载并播放背景音
        pg.mixer.music.load('asset/bgm.mp3')
        pg.mixer.music.set_volume(0.75)
        pg.mixer.music.play(-1)
        
        # 加载音效
        self.bo_sound = pg.mixer.Sound('asset/bo.mp3')
        self.glass_sound=pg.mixer.Sound('asset/glass.mp3')
    
        # 初始状态
        self.state = 'show_cover'
        self.cover_image = pg.image.load('asset/cover.png').convert_alpha()
        self.start_game_rect = pg.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 215, 300, 100)  # 假设矩形区域的中心在屏幕中央，宽200，高100
        
        self.start=True
        self.start_manka=False
        
         # 初始化过场图片列表
        self.intro_images = []

        # 加载过场图片资源，并添加到列表中
        self.intro_images.append(pg.image.load('asset/man1.png').convert_alpha())
        self.intro_images.append(pg.image.load('asset/man2.png').convert_alpha())
        self.current_intro_image = 0  # 跟踪当前展示的图片
        
        # 加载骰子
        self.chosen_image = pg.image.load('asset/7.png').convert_alpha()
        
        # 弹出窗口
        self.popup_surface = None
        
        # 创造精灵组
        self.all_sprites = pg.sprite.Group()
        self.player_sprite = Player(self)
        self.special_sprites = pg.sprite.Group() 
        
        # 设置关卡
        self.level1 = Level1(self)
        self.level2 = Level2(self,self.screen)
        self.current_level=self.level1
        
        # 创建玩家精灵，并添加到精灵组
        if self.current_level==self.level1:
            self.all_sprites.add(self.player_sprite)
        
        # 创建并排列四个骰子
        self.first_roll=True
        self.dices = [Dice( 50 + i * 110, 680,i,is_tool_dice=False) for i in range(4)]  # 假设每个骰子间隔100像素
        for dice in self.dices:
            self.all_sprites.add(dice)
            
        # 创建碎片ui
        self.suipian=Suipian(self)
        self.all_sprites.add(self.suipian)
        
        # 创建工具ui
        self.tool=Tool(self)
        self.all_sprites.add(self.tool)
        
        self.enemy =None
        self.pause_enemy=False
        
        # 初始化窗口
        self.popup_store = None
        self.popup_eventa = None
        self.popup_eventb = None
        self.popup_toolA=None
        
        # 用于跟踪选中的骰子    
        self.selected_dice = None
        
        # 加载背景图像
        self.background_image = pg.image.load('asset/map1.png')
        
        # 设置键盘重复延迟和速率
        pg.key.set_repeat(500, 10)
        
        # 初始化时钟
        self.clock = pg.time.Clock()

    def run(self):
        # 游戏主循环
        running = True
        while running:
            self.event()
 
            # 绘制游戏内容
            self.draw()
            
            # 更新屏幕显示
            pg.display.flip()
            
            # 更新游戏状态
            self.update()

            # 限制帧率
            self.clock.tick(FPS)
        
        # 退出游戏
        pg.quit()
        sys.exit()
        
    def update(self):
        # 更新游戏状态
        self.all_sprites.update()
        self.special_sprites.update()
        

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:  # 假设按空格键投骰子
                    self.roll_dice()
                    for dice in self.dices:
                        dice.selected=False
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                self.start_game_rect = pg.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 215, 300, 100)
                if self.state == 'show_cover' and self.start_game_rect.collidepoint(mouse_pos):
                    self.state = 'show_intro_images'  # 点击封面区域后显示过场图片
                elif self.state == 'show_intro_images':
                    if self.current_intro_image == 0:
                        self.current_intro_image += 1  # 从 man1 切换到 man2
                    elif self.current_intro_image == 1:
                        self.start_game()  # 从 man2 开始游戏
                for dice in self.dices:
                    if dice.check_click(mouse_pos)and dice.selected==False:
                        self.select_dice(dice)
                        self.image = self.chosen_image
                        self.selected=True
                        break  # 假设一次只能选择一个骰子
                # 定义商店按钮对应的属性和成本         
                # 检查商店按钮是否被点击
                if self.popup_store and self.popup_store.open_store:
                    for rect, item_info in shop_actions.items():  # 使用 items() 获取键值对
                        shop_rect = pg.Rect(rect)
                        if shop_rect.collidepoint(mouse_pos):  # 检查是否点击了商店按钮
                            item_type, increment, cost_in_fragments = item_info
                            if self.suipian.count >= cost_in_fragments:  # 检查是否有足够的碎片
                                # 更新碎片数量和工具数量
                                setattr(self.tool, item_type, getattr(self.tool, item_type, 0) + increment)
                                # 调用购买道具并播放动画的方法
                                self.purchase_item_and_play_animation(item_type)
                    if self.popup_store and self.popup_store.open_store:
                        self.popup_store.check_exit_click(event)  # 检查是否点击了退出商店按钮
                                
                # 事件a 
                if  self.popup_eventa and self.popup_eventa.open_eventa:
                    self.popup_eventa.check_exit_click(event)
                    rect1 = pg.Rect(410, 510, 380, 70)
                    rect2 = pg.Rect(410, 610, 380, 70)

                    # 检查是否点击了矩形区域1
                    if rect1.collidepoint(mouse_pos):
                        self.handle_rectangle_click('1')  # 传递矩形编号作为参数

                    # 检查是否点击了矩形区域2
                    if rect2.collidepoint(mouse_pos):
                        self.handle_rectangle_click('2')  # 传递矩形编号作为参数
                        
                # 事件b不知道为啥不能两个写一起那就先这样吧  
                if self.popup_eventb and self.popup_eventb.open_eventb:
                    self.popup_eventb.check_exit_click(event)
                    
                if self.popup_eventb and self.popup_eventb.open_eventb:
                    self.popup_eventb.check_activate_click(event)
                
                # 道具a    
                toolA_rect = pg.Rect(740, 640, 130, 160)
                if toolA_rect.collidepoint(mouse_pos) and self.tool.tool_a > 0:
                    # 减少 tool_c 的数量
                    self.tool.tool_a -= 1
                    self.open_toolA_popup()
                if self.popup_toolA and self.popup_toolA.open_toolA:
                    self.popup_toolA.check_exit_click(event)
                    
                # 道具b
                toolB_rect = pg.Rect(890, 640, 130, 160)
                if toolB_rect.collidepoint(mouse_pos) and self.tool.tool_b > 0:
                    # 减少 tool_c 的数量
                    self.tool.tool_b -= 1
                    # 确保工具 C 窗口未打开
                    self.pause_enemy=True
                    
                # 道具c
                toolC_rect = pg.Rect(1040, 640, 130, 160)
                if toolC_rect.collidepoint(mouse_pos) and self.tool.tool_c > 0:
                    # 减少 tool_c 的数量
                    self.tool.tool_c -= 1
                    # 确保工具 C 窗口未打开
                    if not hasattr(self, 'popup_toolC') or not self.popup_toolC.open_toolC:
                        self.open_toolC_popup()
            # 如果工具 C 窗口已打开，检查移动区域
                if hasattr(self, 'popup_toolC') and self.popup_toolC.open_toolC:
                    # 定义移动区域
                    moves = {
                        (342, 295): 1, (530, 295): 2, (725, 295): 3,
                        (342, 458): 4, (528, 458): 5, (725, 458): 6
                    }
                    for (x, y), steps in moves.items():
                        move_rect = pg.Rect(x, y, 125, 125)
                        if move_rect.collidepoint(mouse_pos):
                            self.player_sprite.move_to_next_position(steps)
                            # 关闭工具 C 窗口
                            self.popup_toolC.close()
                            break  # 点击后立即退出循环
                    
                    
                    
    def draw(self):
        if self.state == 'show_cover':
            self.draw_cover()
        elif self.state == 'show_intro_images':
            self.draw_intro_images()
        elif self.state == 'game_started':
            # 清屏
            self.screen.fill(BLACK)

            # 绘制关卡背景
            self.current_level.draw(self.screen)
    
            # 绘制精灵
            for sprite in self.all_sprites:
                sprite.draw(self.screen)
            # 如果弹出窗口存在，则绘制它
            if self.popup_surface:
                self.screen.blit(self.popup_surface, (0, 0))
                
            self.special_sprites.draw(self.screen)
                
            pg.display.flip()
            
        elif self.state == 'win':
            self.win_draw()
            
        elif self.state == 'lost':
            self.lost_draw()

        # 道具b
        # pg.draw.rect(self.screen, BLACK, pg.Rect(890, 640, 130, 160))
        # 绘制
        # 更新屏幕显示
        
        
    def roll_dice(self):
        for dice in self.dices:
            dice.roll()  # 掷每个骰子
            
    def select_dice(self, dice):
        if self.selected_dice is not None:
            self.selected_dice.selected = False  # 取消之前选中的骰子
        dice.selected = True  # 选中当前点击的骰子
        self.selected_dice = dice  # 更新跟踪的选中骰子
        self.move_player()
        

    def move_player(self):
        if self.selected_dice is not None:
            print(f" {self.selected_dice.last_roll}")
            steps = self.selected_dice.last_roll  # 获取选中骰子的步数值
            if self.current_level==self.level2:
                self.current_level.camera_group.center_target_camera(self.player_sprite)
                print("主中相机开启")
                # 设置为以主角为中心的摄像机模式
                if self.enemy is None:
                    self.create_enemy_sprite()
                else:
                    if self.pause_enemy==False:
                        self.move_enemy()  # 移动敌人
                    else:
                        self.pause_enemy=False
            self.player_sprite.move_to_next_position(steps)
            if isinstance(self.current_level, Level2):  # 确保只在第二关改变相机模式
                self.current_level.camera_group.is_free_camera = False
                self.current_level.camera_group.is_free_camera = True
                print("自由相机开启")
            self.selected_dice = None  # 移动完成后重置选中的骰子
            
    def create_enemy_sprite(self):
        if not self.enemy:  # 确保敌人尚未创建
            self.enemy = Enemy(self)
            # 确保敌人精灵被添加到Level2的摄像机组
            if isinstance(self.current_level, Level2):
                self.current_level.add_enemy_to_camera(self.enemy)

    def move_enemy(self):
        # 敌人每次固定走3步
        enemy_steps = 3
        if self.enemy:
            self.enemy.e_move_to_next_position(enemy_steps) 
        
    def purchase_item_and_play_animation(self, item_type):
        # 根据道具类型创建对应的动画精灵
        if item_type == 'tool_a':
            animation_sprite = Tool_Afei(self)
        elif item_type == 'tool_b':
            animation_sprite = Tool_Bfei(self)
        elif item_type == 'tool_c':
            animation_sprite = Tool_Cfei(self)

    # 将动画精灵添加到精灵组
        self.special_sprites.add(animation_sprite)  # 确保使用正确的精灵组
        
    def event_A(self):
        # 事件 A 的处理逻辑
        print("触发事件 A")
        # 弹出窗口逻辑
        self.bo_sound.play()
        self.popup_eventa = Popup_EventA(self, self.current_level, self.player_sprite.m_current_position_index)
        self.all_sprites.add(self.popup_eventa)
        
    def handle_rectangle_click(self, rect_num):
        if self.popup_eventa and self.popup_eventa.open_eventa:
            # 从当前图片名称中提取编号部分，并构建新的图片名称
            base_image_number = int(self.popup_eventa.image_name[1:-4])  # 例如从 'A1.  png' 提取 '1'
            new_image_prefix = f'asset/A{base_image_number}{rect_num}'  # 根据点击的矩形编号构建新的前缀
            new_image_name = new_image_prefix + '.png'  # 构建新的图片名称

            # 关闭当前的事件窗口
            self.popup_eventa.close()

            # 创建一个新的事件窗口实例，并更新图片
            new_popup_eventa = Popup_EventA(self, self.current_level, self.player_sprite.m_current_position_index)
            new_popup_eventa.change_image(new_image_name)

            # 将新的事件窗口实例添加到精灵组
            self.all_sprites.add(new_popup_eventa)
            
            self.popup_eventa = new_popup_eventa

    def event_B(self):
        # 事件 B 的处理逻辑
        print("触发事件 B")    
        self.bo_sound.play()  
        # 弹出窗口逻辑
        self.popup_eventb = Popup_EventB(self, self.current_level, self.player_sprite.m_current_position_index)
        self.all_sprites.add(self.popup_eventb)
        
    def event_C(self):
        # 事件 B 的处理逻辑
        print("触发事件 C")
        # 弹出窗口逻辑
        self.bo_sound.play()
        self.popup_store = Popup_Store(self)
        self.all_sprites.add(self.popup_store)
        
    def open_toolA_popup(self):
        self.bo_sound.play()
        self.popup_toolA = Popup_toolA(self)  # 假设 Popup_toolC 是已定义好的类
        self.all_sprites.add(self.popup_toolA)
        
    def open_toolC_popup(self):
        self.bo_sound.play()
        self.popup_toolC = Popup_toolC(self)  # 假设 Popup_toolC 是已定义好的类
        self.all_sprites.add(self.popup_toolC)
        
    def change_level(self):
        # 第一关完成，更新为第二关的路径
        if self.current_level == self.level2:
            self.win_end()
        if self.current_level==self.level1:
            self.player_sprite.change_level(positions_level2)
            # 更新当前关卡为第二关           
            self.current_level = self.level2
            self.all_sprites.remove(self.player_sprite)
        
            
        
    def start_game(self):
        # 这里添加开始游戏的逻辑
        self.state = 'game_started'  # 更新状态为游戏已开始
        self.cover_image = None  # 隐藏封面图片
        self.start = False
    
    def draw_cover(self):
        # 清屏
        self.screen.fill(BLACK)
        # 绘制封面
        self.screen.blit(self.cover_image, (0, 0))
        # 更新屏幕显示
        pg.display.flip()

    def draw_intro_images(self):
        # 清屏
        self.screen.fill(BLACK)
        # 绘制当前过场图片
        self.screen.blit(self.intro_images[self.current_intro_image], (0, 0))
        # 更新屏幕显示
        pg.display.flip()
        
    def win_draw(self):
        # 清屏
        self.screen.fill(BLACK)
        # 绘制封面
        self.screen.blit(self.end1_image, (0, 0))
        # 更新屏幕显示
        pg.display.flip()
        
    def win_end(self):
        self.state = 'win'
        
    def lost_draw(self):
        # 清屏
        self.screen.fill(BLACK)
        # 绘制封面
        self.screen.blit(self.end2_image, (0, 0))
        # 更新屏幕显示
        pg.display.flip()
        
    def lost_end(self):
        self.state = 'lost'
            
# 游戏主函数
if __name__ == "__main__" :
    game = Game()
    game.run()