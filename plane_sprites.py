import random
import pygame


SCREEN_RECT = pygame.Rect(0, 0, 480, 700)

FRAME_PER_SEC = 60

CREATE_ENEMY_EVENT = pygame.USEREVENT
HERO_FIRE = pygame.USEREVENT + 1

HERO_SPEED = 4
HERO_PIC = "./images/me1.png"


class GameSprites(pygame.sprite.Sprite):
    """游戏精灵基类"""

    def __init__(self, image, speed=1):

        # 调用父类的初始方法
        super().__init__()

        # 加载图像
        self.image = pygame.image.load(image)

        # 设置尺寸
        self.rect = self.image.get_rect()

        # 记录速度
        self.speed = speed

        # EK 定义游戏中各元素（除背景图）的x轴最大边界
        self.max_x = SCREEN_RECT.width - self.rect.width

    def update(self):

        # 默认垂直向下匀速运动
        self.rect.top += self.speed

    # TODO EK
    @staticmethod
    def image_names(prefix, count):
        pass


class Background(GameSprites):
    """背景精灵"""

    def __init__(self, is_alt=False):

        super().__init__("./images/background.png")

        # is_alt 即“是否为替换”的意思， is_alt == True 即代表该背景图是替代的图，替代图片在开始时要在屏幕上方。
        # if is_alt is True:
        if is_alt:
            self.rect.bottom = 0

    def update(self):

        # 调用父类方法
        super().update()

        # 判断是否超出屏幕
        if self.rect.top >= self.rect.height:
            self.rect.bottom = 0


class Enemy(GameSprites):

    def __init__(self):
        super().__init__("./images/enemy1.png")

        # 随机敌机出现的位置
        self.rect.left = random.randint(0, self.max_x)
        self.speed = random.randint(2, 4)
        self.rect.bottom = 0

    def update(self):
        super().update()

        # 判断敌机精灵是否飞出屏幕，如果是，执行self.kill()方法从内存中删除该精灵
        if self.rect.y >= SCREEN_RECT.height:
            self.kill()

    # 测试self.kill()是否真的执行成功，成功了的话会输出下面语句。
    def __del__(self):
        print("敌机挂了 %s " % self.rect)


class Hero(GameSprites):
    """英雄精灵"""

    def __init__(self):
        super().__init__(HERO_PIC, HERO_SPEED)

        # 设置初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 100

        # 创建子弹组
        self.bullet_group = pygame.sprite.Group()

    def update(self):

        # 通过pygame.key 获取用户按键
        keys_pressed = pygame.key.get_pressed()
        # if keys_pressed[pygame.K_RIGHT]:
        #     self.rect.x += self.speed
        # elif keys_pressed[pygame.K_LEFT]:
        #     self.rect.x -= self.speed
        dir = keys_pressed[pygame.K_RIGHT] - keys_pressed[pygame.K_LEFT]

        # 飞机水平移动
        self.rect.x += dir * self.speed

        # 超出屏幕检测
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):

        for i in range(0, 3):
            # 1. 创建子弹精灵
            bullet = Bullet()

            # 2. 设置精灵的位置
            bullet.rect.centerx = self.rect.centerx
            bullet.rect.bottom = self.rect.y - i * 20

            # 3. 将精灵添加到精灵组
            self.bullet_group.add(bullet)

    def __del__(self):
        print("英雄阵亡！")
        print("游戏结束")


class Bullet(GameSprites):
    """子弹精灵"""

    def __init__(self):
        super().__init__("./images/bullet1.png", -2)
        self.rect.x = 220
        self.rect.y = 400

    def update(self):

        super().update()

        # 判断是否超出屏幕
        if self.rect.bottom <= 0:
            self.kill()

    def __del__(self):
        print("子弹被销毁了！")
