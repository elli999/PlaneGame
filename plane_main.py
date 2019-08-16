import pygame
from plane_sprites import *


class PlaneGame(object):
    """主程序"""
    def __init__(self):

        # 1. pygame 初始化
        pygame.init()

        # 2. 创建游戏屏幕
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)

        # 3. 创建游戏时钟
        self.clock = pygame.time.Clock()

        # 4. 创建精灵组
        self.__create_sprites()

        # 5. 创建用户事件
        PlaneGame.__create_user_events()

    def __create_sprites(self):
        """创建精灵组"""

        # 背景组
        bg1 = Background()
        bg2 = Background(True)
        self.bg_group = pygame.sprite.Group(bg1, bg2)

        # 敌机组
        self.enemy_group = pygame.sprite.Group()

        # 因为后续要对hero做碰撞检测以及发射子弹，所以hero需要单独定义成属性（即加上“self.”，方便在后面调用）
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    @staticmethod
    def __create_user_events():
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE, 500)

    def start_game(self):
        """开始游戏"""

        print("开始游戏")

        while True:
            # 1. 设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)

            # 2. 事件监听
            self.__event_handler()

            # 3. 更新精灵组
            self.__update_sprites()

            # 4. 碰撞检测
            self.__check_collide()

            # 5. 更新屏幕显示
            pygame.display.update()

            # self.__game_over()

    def __event_handler(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # self.__game_over()
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                # 创建敌机，并且添加到敌机组
                self.enemy_group.add(Enemy())

                # 测试敌机精灵数量
                # enemy_count = len(self.enemy_group.sprites())
                # print("敌机精灵数量 %d" % enemy_count)
            elif event.type == HERO_FIRE:
                self.hero.fire()

    def __update_sprites(self):
        """更新精灵组"""

        for group in [self.bg_group, self.enemy_group,
                      self.hero_group, self.hero.bullet_group]:
            group.update()
            group.draw(self.screen)

    def __check_collide(self):
        """碰撞检测"""

        # 1. 子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullet_group, self.enemy_group, True, True)

        # 2. 英雄被撞毁
        enemy_collide_list = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)

        if len(enemy_collide_list) > 0:
            self.hero.kill()
            PlaneGame.__game_over()

    @staticmethod
    def __game_over():
        """游戏结束"""
        print("退出游戏")
        pygame.quit()
        exit()


if __name__ == '__main__':
    # 1. 创建游戏对象
    game = PlaneGame()

    # 2. 开始游戏
    game.start_game()
