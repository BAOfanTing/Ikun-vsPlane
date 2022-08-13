import pygame

class Myplane(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load("images/me1.png").convert_alpha()
        self.image2 = pygame.image.load("images/me2.png").convert_alpha()
        self.rect = self.image1.get_rect()
        self.width,self.height = bg_size[0],bg_size[1]
        #被摧毁的图片
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("images/me_destroy_1.png").convert_alpha(), \
            pygame.image.load("images/me_destroy_2.png").convert_alpha(), \
            pygame.image.load("images/me_destroy_3.png").convert_alpha(), \
            pygame.image.load("images/me_destroy_4.png").convert_alpha(), \
            ])
        self.speed = 5
        #把飞机放在中间
        self.rect.left,self.rect.top = \
            (self.width - self.rect.width) //2 ,\
            self.height - self.rect.height - 60
        # 检测是否存活
        self.active = True
        #把不透明的部分变为碰撞区域
        self.mask = pygame.mask.from_surface(self.image1)
        #无敌属性
        self.invincible = False
    #定义移动函数
    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveDown(self):
        if self.rect.bottom < self.height - 60:
            self.rect.bottom += self.speed
        else:
            self.rect.bottom = self.height - 60

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.right += self.speed
        else:
            self.rect.right = self.width
    def reset(self):
        self.active = True
        self.invincible = True
        # self.rect.left, self.rect.top = \
        #     (self.width - self.rect.width) // 2, \
        #     self.height - self.rect.height - 60



