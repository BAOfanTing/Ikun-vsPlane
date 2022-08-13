import pygame
from random import *

class Smallenemy(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/enemy1.png").convert_alpha()
        self.rect = self.image.get_rect()
        # 被摧毁的图片
        self.destroy_images = []
        self.destroy_images.extend([ \
            pygame.image.load("images/enemy1_down1.png").convert_alpha(), \
            pygame.image.load("images/enemy1_down2.png").convert_alpha(), \
            pygame.image.load("images/enemy1_down3.png").convert_alpha(), \
            pygame.image.load("images/enemy1_down4.png").convert_alpha(), \
            ])

        self.speed = 2
        self.width,self.height = bg_size[0],bg_size[1]
        self.rect.left,self.rect.top = \
            randint(0,self.width-self.rect.width),\
            randint(-5*self.height,0)
        # 检测是否存活
        self.active = True
        # 把不透明的部分变为碰撞区域
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()
    #重置敌人
    def reset(self):
        self.active = True
        self.rect.left, self.rect.top = \
            randint(0,self.width - self.rect.width), \
                randint(-5 * self.height, 0)


class Midenemy(pygame.sprite.Sprite):
    hp = 10
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/enemy2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.hit_image = pygame.image.load("images/enemy2_hit.png").convert_alpha()
        # 被摧毁的图片
        self.destroy_images = []
        self.destroy_images.extend([ \
            pygame.image.load("images/enemy2_down1.png").convert_alpha(), \
            pygame.image.load("images/enemy2_down2.png").convert_alpha(), \
            pygame.image.load("images/enemy2_down3.png").convert_alpha(), \
            pygame.image.load("images/enemy2_down4.png").convert_alpha(), \
            ])

        self.speed = 1
        self.width,self.height = bg_size[0],bg_size[1]
        self.rect.left,self.rect.top = \
            randint(0,self.width-self.rect.width),\
            randint(-10*self.height,-self.height)
        #检测是否存活
        self.active = True
        # 把不透明的部分变为碰撞区域
        self.mask = pygame.mask.from_surface(self.image)
        self.hp = Midenemy.hp
        self.hit = False
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()
    #重置敌人
    def reset(self):
        self.active = True
        self.hp = Midenemy.hp
        self.rect.left, self.rect.top = \
            randint(0 ,self.width - self.rect.width), \
            randint(-10 * self.height, -self.height)

class Bigenemy(pygame.sprite.Sprite):
    hp = 20
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load("images/enemy3_n1.png").convert_alpha()
        self.image2 = pygame.image.load("images/enemy3_n2.png").convert_alpha()
        self.hit_image = pygame.image.load("images/enemy3_hit.png").convert_alpha()
        # 被摧毁的图片
        self.destroy_images = []
        self.destroy_images.extend([ \
            pygame.image.load("images/enemy3_down1.png").convert_alpha(), \
            pygame.image.load("images/enemy3_down2.png").convert_alpha(), \
            pygame.image.load("images/enemy3_down3.png").convert_alpha(), \
            pygame.image.load("images/enemy3_down4.png").convert_alpha(), \
            pygame.image.load("images/enemy3_down5.png").convert_alpha(), \
            pygame.image.load("images/enemy3_down6.png").convert_alpha(), \
            ])
        self.rect = self.image1.get_rect()
        self.speed = 1
        self.width,self.height = bg_size[0],bg_size[1]
        self.rect.left,self.rect.top = \
            randint(0,self.width-self.rect.width),\
            randint(-15*self.height,-5*self.height)
        # 检测是否存活
        self.active = True
        # 把不透明的部分变为碰撞区域
        self.mask = pygame.mask.from_surface(self.image1)
        self.hp = Bigenemy.hp
        self.hit = False
        #用于发射子弹
        self.shoot = []

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()
    #重置敌人
    def reset(self):
        self.active = True
        self.hp = Bigenemy.hp
        self.rect.left, self.rect.top = \
            randint(0,self.width - self.rect.width), \
            randint(-15 * self.height, -5*self.height)