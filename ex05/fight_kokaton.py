import sys
import time
import random

import pygame as pg
import tkinter as tk

from tkinter import messagebox as tkm


class Timer(): #タイマークラス
    def __init__(self):
        pass

    def score_time(self,st):
        nowt = time.time()
        nowtm = nowt - st
        nowtm //= 1
        nowtm = int(nowtm)
        return nowtm


class Music():#ミュージッククラス
    def __init__(self):
        pg.mixer.init(frequency=44100)
        self.BGM = pg.mixer.Sound("music/春よ、強く美しく.mp3")
        self.EXPlOSION = pg.mixer.Sound("music/爆発2.mp3")

    def bgm(self):
        self.BGM.play(-1)

    def explosion(self):
        self.EXPlOSION.play(1)


class ScoreTime(): #スコアクラス
    def __init__(self):
        root = tk.Tk()
        root.withdraw()
        with open('ex05/text.txt', mode="r", encoding="UTF-8") as file:# ハイスコア読み込み
            for num in file.readline():
                self.HISCORE = int(num)

    def score(self,timer,st):
        self.score_time = timer.score_time(st)
        if self.score_time > self.HISCORE:#ハイスコア判定と書き込み
            with open('ex05/text.txt', mode="w", encoding="UTF-8") as file:
                file.write(f"{self.score_time}")
            tkm.showinfo("Hit", f"ハイスコア:{self.HISCORE}秒  生存時間:{self.score_time}秒")
            tkm.showinfo("Hit", "ハイスコア更新おめでとう！")
            return
        tkm.showinfo("Hit", f"ハイスコア:{self.HISCORE}秒  生存時間:{self.score_time}秒")#最終結果表示
        tkm.showinfo("Hit", "次も頑張ろう！")


class Text_blit():#テキスト描画クラス
    def __init__(self):
        self.font = pg.font.Font(None, 50)

    def text(self, text1, scrn, xy):
        text = self.font.render(text1, True, (0,0,0))
        scrn.blit_text(text, xy)


class Screen(pg.sprite.Sprite): #スクリーンと背景のクラス　　
    def __init__(self, title, wh_pos:tuple, file_path):
        pg.sprite.Sprite.__init__(self)
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh_pos)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(file_path)
        self.bgi_rct = self.bgi_sfc.get_rect()

    def blit(self, *bilt_item):
        if len(bilt_item) != 0:
            self.sfc.blit(bilt_item[0], bilt_item[1])
        else:
            self.sfc.blit(self.bgi_sfc, self.bgi_rct)

    def blit_text(self, text, pos:list):
        self.sfc.blit(text, pos)

    def get_rect(self):
        return self.rct

    def get_bgi_rct(self):
        return self.bgi_rct


class Bird(pg.sprite.Sprite): #こうかとんのクラス
    key_move = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
        }

    def __init__(self, file_path, ratio, xy):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(file_path)
        self.image = pg.transform.rotozoom(self.image, 0, ratio)
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.judge = 0
        self.MOUSE_MODE = False

    def blit(self, scrn):
        scrn.blit(self.image, self.rect)

    def final_blit(self, scrn, file_path):
        self.image = pg.image.load(file_path)
        self.rect.centerx = 450
        self.rect.centery = 300
        scrn.blit(self.image, self.rect)

    def update(self, scrn):
        key_states = pg.key.get_pressed()
        rct = scrn.get_rect()
        if self.MOUSE_MODE:
            (x, y)= pg.mouse.get_pos()
            self.rect.centerx = x
            self.rect.centery = y
        else:
            for key, move in self.key_move.items():
                if key_states[key]:
                    if key_states[pg.K_LEFT] and self.judge == 1:
                        self.image = pg.transform.flip(self.image, 1, 0)
                        self.judge = 0
                    elif key_states[pg.K_RIGHT] and self.judge == 0:
                        self.image = pg.transform.flip(self.image, 1, 0)
                        self.judge = 1
                    self.rect.move_ip(move[0], move[1])
                    if check_bound(self.rect, rct) != (1, 1):
                        self.rect.move_ip(-1*move[0], -1*move[1])
        scrn.blit(self.image, self.rect)


class Bomb(pg.sprite.Sprite):# 爆弾を生成するクラス
    speed = [-3,-2,-1,1,2,3]
    def __init__(self, color, rad, scrn:Screen):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((2*rad, 2*rad))
        self.image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.image, color, (rad, rad), rad)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(10, scrn.rct.width-10)
        self.rect.centery = random.randint(10, scrn.rct.height-10)
        self.move_x = random.choice(self.speed)
        self.move_y = random.choice(self.speed)

    def blit(self, scrn:Screen):
        scrn.sfc.blit(self.image, self.rect)

    def update(self, scrn:Screen):
        yoko, tate = check_bound(self.rect, scrn.rct)
        self.move_x *= yoko
        self.move_y *= tate
        self.rect.move_ip(self.move_x, self.move_y)
        scrn.blit(self.image, self.rect)


def check_bound(obj_rct, scr_rct): #衝突チェック関数
    yoko,tate = +1,+1
    if obj_rct.left < scr_rct.left or obj_rct.right > scr_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or obj_rct.bottom > scr_rct.bottom:
        tate = -1
    return yoko, tate


def main():
    scrn = Screen("戦う！こうかとん", (1600, 900), "fig/pg_bg.jpg")#スクリーン描画
    bird = Bird("fig/6.png", 2.0, (900, 400))#こうかとん描画
    bombs = Bomb((255, 0, 0), 10, scrn)#爆弾描画
    bomb_lst = [bombs]
    bird_grp = pg.sprite.Group(bird)
    bomb_grp = pg.sprite.Group(*bomb_lst)
    groop = pg.sprite.Group(bird, *bomb_lst)#グループ化
    font = pg.font.Font(None, 50)
    music = Music()#ミュージック
    score_time = ScoreTime()#スコア
    timer = Timer()#タイマー
    st = time.time()
    text_blit = Text_blit()#テキスト
    clock = pg.time.Clock()
    music.bgm()
    FIGHT_MODE = True
    count = 5

    while True:
        scrn.blit()
        if FIGHT_MODE:
            text_blit.text("FIGHT_MODE",scrn , [1200,10])#ファイトモードの表示
            if (count >= 0
                    and pg.sprite.groupcollide(bird_grp,bomb_grp,dokilla=False, dokillb=True)):
                count -= 1
            elif count < 0:
                FIGHT_MODE = False
        else:#通常
            if pg.sprite.groupcollide(bird_grp, bomb_grp, dokilla=True, dokillb=True):
                bird.final_blit(scrn.sfc,"fig/bakuhatsu.png")
                pg.display.update()
                music.explosion()
                score_time.score(timer,st)
                return

        groop.update(scrn)
        groop.draw(scrn.sfc)

        for event in pg.event.get():
            if (event.type == pg.MOUSEBUTTONDOWN
                    and event.button == 1): #マウス操作モード判定
                bird.MOUSE_MODE = not bird.MOUSE_MODE
            if (event.type == pg.KEYUP
                    and event.key == pg.K_SPACE):#無敵モード判定
                FIGHT_MODE = not FIGHT_MODE
                count = 5
            if event.type == pg.QUIT:
                return
            if event.type == 30:#爆弾の追加
                bombs = Bomb((255, 0, 0), 10, scrn)
                groop.add(bombs)
                bomb_grp.add(bombs)

        if bird.MOUSE_MODE:
            text_blit.text("MOUSEMODE ON", scrn , [700,10])#マウスモードの表示

        times = timer.score_time(st)
        text_blit.text(f"ScoreTime{times}", scrn , [10,10])#タイマーの表示

        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init() # 初期化
    main()    # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()