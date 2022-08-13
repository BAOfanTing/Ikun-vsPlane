import pygame
import sys
import traceback
import myplane
import enemy
import bullet
import supply
from pygame.locals import *
from random import  *
#初始化
pygame.init()
pygame.mixer.init()

BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)

#设置背景大小
bg_size = width,height = 480,700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战坤坤")

background = pygame.image.load("images/background.png").convert_alpha()

#载入音乐
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)

bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.3)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(3)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.5)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(1)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(1)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.5)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(1)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(1)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.5)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.5)




clock = pygame.time.Clock()

def add_small_enemies(group1,group2,num):
    for i in range(num):
        e1 = enemy.Smallenemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.Midenemy(bg_size)
        group1.add(e2)
        group2.add(e2)


def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.Bigenemy(bg_size)
        group1.add(e3)
        group2.add(e3)

#用于增加速度
def inc_speed(target,inc):
    for each in target:
        each.speed += inc


def main():
    pygame.mixer.music.play(-1)

    #生成我方飞机
    me = myplane.Myplane(bg_size)

    #生成敌机
    enemies = pygame.sprite.Group()
    #生成小型飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies,enemies,15)
    # 生成中型飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 10)
    # 生成大型飞机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 3)

    #生成子弹
    bullet1 = []
    bullet1_index = 0
    for i in range(4):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    #生成敌方子弹
    bullet3 = []
    bullet3_index = 0
    for each in big_enemies:
        for i in range(2):
            bullet3.append(bullet.Bullet3(each.rect.midbottom))

    #生成超级子弹
    bullet2 = []
    bullet2_index = 0
    for i in range(4):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 33,me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))
    clock = pygame.time.Clock()
    # 中弹毁灭图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    running = True
    #用于切换我方飞机图片
    switch_image = True

    #用于延显示飞机动画效果
    delay = 100
    #统计得分
    score = 0
    score_font = pygame.font.Font("font/myfont.ttf",20)
    gameover_font = pygame.font.Font("font/myfont.ttf",40)
    #设置难度
    level = 1
    #没30秒发放补给包
    bullet_supply = supply.Bullet_supply(bg_size)
    bomb_supply = supply.Bomb_supply(bg_size)
    SUPPLY_TIME = USEREVENT #变为自定义事件来响应
    pygame.time.set_timer(SUPPLY_TIME,30*1000)

    #超级子弹计时器
    DOUBLE_BULLET_TIME = USEREVENT + 1

    #标志是否超级子弹
    is_double_bullet = False

    #解除无敌的计时器
    INVINCIBLE_TIME = USEREVENT + 2

    #剩余生命
    life_image = pygame.image.load("images/life.png")
    life_rect = life_image.get_rect()
    life_num = 5
    #阻止多级打开文件
    recored = False
    #全屏炸弹
    bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/myfont.ttf",48)
    bomb_num = 5

    #游戏结束图片
    gamerestart_image = pygame.image.load("images/again.png").convert_alpha()
    gamerestart_rect = gamerestart_image.get_rect()
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()

    #标志是否暂停游戏
    paused = False
    paused_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
    paused_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
    paused_rect = paused_nor_image.get_rect()
    paused_rect.left,paused_rect.top = width - paused_rect.width - 10,10
    paused_image = paused_nor_image

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #检测暂停
            elif event.type == MOUSEBUTTONDOWN:
                # 检测鼠标是否在暂停按钮之内
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME,0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME,30*1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
                # #检测鼠标是否在重新开始内
                # elif event.button == 1 and gamerestart_rect.collidepoint(event.pos):
                #     main()
                # elif event.button == 1 and gameover_rect.collidepoint(event.pos):
                #     pygame.quit()
                #     sys.exit()
            #暂停按钮
            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = paused_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = paused_nor_image
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
            #给炸弹事件
            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                if choice([True,False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
            #
            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME,0)

            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME,0)


        #根据用户得分增加难度
        if level == 1 and score > 20:
            #增加3小，2中
            level = 2
            upgrade_sound.play()
            add_small_enemies(small_enemies,enemies,3)
            add_mid_enemies(mid_enemies,enemies,2)

            #增加敌方速度
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies, 1)
            inc_speed(big_enemies,1)

        elif level == 2 and score > 80:
            #增加3小，2中
            level = 3
            upgrade_sound.play()
            add_small_enemies(small_enemies,enemies,3)
            add_mid_enemies(mid_enemies,enemies,2)

            #增加敌方速度
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies, 1)
        elif level == 3 and score > 150:
            #增加3小，2中
            level = 4
            upgrade_sound.play()
            add_small_enemies(small_enemies,enemies,3)
            add_mid_enemies(mid_enemies,enemies,2)
            add_big_enemies(big_enemies, enemies, 1)
            #增加敌方速度
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies, 1)
            inc_speed(big_enemies, 1)
        elif level == 4 and score > 300:
            #增加3小，2中
            level = 5
            upgrade_sound.play()
            add_small_enemies(small_enemies,enemies,5)
            add_mid_enemies(mid_enemies,enemies,2)
            add_big_enemies(big_enemies, enemies, 1)
            #增加敌方速度
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies, 1)
            inc_speed(big_enemies, 1)



         # 打印背景
        screen.blit(background, (0, 0))
        if not paused and life_num:
            #检测用户键盘操作
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()
            #检测炸弹是否获得
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image,bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply,me):
                    get_bomb_sound.play()
                    if bomb_num < 99:
                        bomb_num += 1
                        life_num += 1
                    bomb_supply.active = False
            #检测双倍子弹补给
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image,bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply,me):
                    get_bullet_sound.play()
                    life_num += 1
                    bomb_num += 1
                    #发射超级子弹事件
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME,18*1000)
                    bullet_supply.active = False




            #发射子弹
            if not(delay % 10):
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx-33,me.rect.centery))
                    bullets[bullet2_index+1].reset((me.rect.centerx + 30, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % 8
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % 4
            #检测子弹是否击中
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image,b.rect)
                    enemies_hit = pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
                    if enemies_hit:
                        b.active = False
                        for e in enemies_hit:

                            #大和中型敌机扣血
                            if e in mid_enemies or e in big_enemies:
                                e.hp -= 1
                                if e.hp == 0:
                                    e.active = False
                                e.hit = True
                            else:
                                 e.active = False


            #绘制大敌机
            for each in big_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.hit_image, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    #绘制血槽(屏幕，颜色，起始，结束，宽度)
                    pygame.draw.line(screen,BLACK, \
                                     (each.rect.left,each.rect.bottom+5), \
                                     (each.rect.right,each.rect.bottom+5),2)
                    #当生命小于20时显示为红色血条
                    hp_remian = each.hp / enemy.Bigenemy.hp
                    if hp_remian > 0.2:
                        hp_color = GREEN
                    else:
                        hp_color = RED
                    pygame.draw.line(screen,hp_color , \
                                     (each.rect.left,each.rect.bottom+5),
                                     (each.rect.left + each.rect.width * hp_remian,each.rect.bottom+5),2)

                    #出现在画面中，播放音效
                    if each.rect.bottom == -50:
                        enemy3_fly_sound.play(-1)
                    #发射子弹
                    if each.rect.bottom > 0:
                        if not(delay % 60):
                            each.shoot = bullet3
                            each.shoot[bullet3_index].reset(each.rect.midbottom)
                            bullet3_index = (bullet3_index + 1) % 2
                        #检测碰撞
                        for b in each.shoot:
                            if b.active:
                                b.move()
                                screen.blit(b.image, b.rect)
                                enemies_bullet_hit = pygame.sprite.collide_rect(b, me)
                                if enemies_bullet_hit and not me.invincible:
                                    b.active = False
                                    me.active = False

                #被摧毁
                else:
                    if not (delay % 3):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index],each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score +=3
                            each.reset()


            #绘制中型飞机
            for each in mid_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.hit_image, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)
                    #绘制血槽(屏幕，颜色，起始，结束，宽度)
                    pygame.draw.line(screen,BLACK, \
                                     (each.rect.left,each.rect.bottom+5), \
                                     (each.rect.right,each.rect.bottom+5),2)
                    #当生命小于20时显示为红色血条
                    hp_remian = each.hp / enemy.Midenemy.hp
                    if hp_remian > 0.2:
                        hp_color = GREEN
                    else:
                        hp_color = RED
                    pygame.draw.line(screen,hp_color , \
                                     (each.rect.left,each.rect.bottom+5),
                                     (each.rect.left+each.rect.width * hp_remian,each.rect.bottom+5),2)

                # 被摧毁
                else:
                    if not (delay % 3):
                        if e2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 2
                            each.reset()

            #绘制小型飞机
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                # 被摧毁
                else:
                    if not (delay % 3):
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = ((e1_destroy_index + 1) % 4)
                        if e1_destroy_index == 0:
                            score += 1
                            each.reset()
            #检测我方飞机是否被撞
            enemies_down = pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for each in enemies_down:
                    each.active = False


            #绘制我方飞机
            if me.active:
                if switch_image:
                    screen.blit(me.image1,me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            # 被摧毁
            else:
                if not (delay % 3):
                    if me_destroy_index == 0:
                        me_down_sound.play()
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME,3000)

            #绘制剩余炸弹
            bomb_text = bomb_font.render("* %d" % bomb_num,True,WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image,(10,height -10 - bomb_rect.height))
            screen.blit(bomb_text,(80,height - 20- text_rect.height))
            #绘制剩余生命
            if life_num:
                screen.blit(life_image, \
                            (width - 80- life_rect.width,\
                             height - 10 -life_rect.height))
                life_text = bomb_font.render("* %d" % life_num, True, WHITE)
                life_text_rect = bomb_text.get_rect()
                screen.blit(life_text, (400, height - 20 - life_text_rect.height))

            # 绘制分数
            score_text = score_font.render("击败坤坤： %s" % str(score), True, WHITE)
            screen.blit(score_text, (10, 5))
        #绘制游戏结束画面
        elif life_num == 0:
            #背景音乐停止
            pygame.mixer.music.stop()
            #停止全部音效
            pygame.mixer.stop()
            #停止发放补给
            pygame.time.set_timer(SUPPLY_TIME,0)
            if not recored:
                recored = True
                #读取历史最高分
                with open("record.txt","r") as f:
                    record_score = int(f.read())
                #如果玩家分高就存档
                if score > record_score:
                    with open("record.txt","w") as f:
                        f.write(str(score))
                    maxscore = score
                else:
                    maxscore = record_score

            # 绘制历史最佳分数
            maxscore_text = gameover_font.render("历史最高 %d" % maxscore, True, WHITE)
            maxscore_text_rect = maxscore_text.get_rect()
            screen.blit(maxscore_text, ((width - maxscore_text_rect.width) // 2, \
                                        height - maxscore_text_rect.height - 600))

            #绘制结束画面
            gameover_text1 = gameover_font.render("你的分数",True,WHITE)
            gameover_text1_rect = gameover_text1.get_rect()
            screen.blit(gameover_text1,((width - gameover_text1_rect.width)//2,\
                                        height - gamerestart_rect.height - 500))

            #绘制分数
            score_text = gameover_font.render("%s" % str(score), True, WHITE)
            score_text_rect = score_text.get_rect()
            screen.blit(score_text,((width - score_text_rect.width)//2,\
                                    height -gamerestart_rect.height - 450 ))

            #绘制重新开始
            gamerestart_rect.left,gamerestart_rect.top =(width - gamerestart_rect.width)//2,\
                                           height - gamerestart_rect.height - 300
            screen.blit(gamerestart_image,gamerestart_rect)
            #绘制退出游戏
            gameover_rect.left,gameover_rect.top = (width - gameover_rect.width)//2, \
                                            height - gameover_rect.height - 250
            screen.blit(gameover_image, gameover_rect)

            #检测鼠标的操作
            #如果按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                #获取鼠标当前位置
                pos = pygame.mouse.get_pos()
                #点击重新开始
                if gamerestart_rect.left < pos[0] < gamerestart_rect.right and \
                        gamerestart_rect.top < pos[1] < gamerestart_rect.bottom:
                    #调用main函数重新开始
                    main()
                #点击退出游戏
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                        gameover_rect.top < pos[1] < gameover_rect.bottom:
                    pygame.quit()
                    sys.exit()




        #绘制暂停按钮
        screen.blit(paused_image,paused_rect)


        #切换图片
        if not(delay % 5):
            switch_image = not switch_image
        delay -= 1
        if not delay:
            delay = 100


        #刷新屏幕
        pygame.display.flip()
        #设置帧率
        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()

