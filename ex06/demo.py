import pygame as pg
import math
import sys
import random
import tkinter.messagebox as tkm
import tkinter as tk
import time

from pygame.locals import *


class Screen(pg.sprite.Sprite):#スクリーンクラス 山
    def __init__(self, title, wh_pos:tuple, file_path):#初期設定
        pg.sprite.Sprite.__init__(self)
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh_pos)
        self.rect = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(file_path)
        self.bgi_rect = self.bgi_sfc.get_rect()

    def bilt(self):#背景の描画
        self.sfc.blit(self.bgi_sfc, self.bgi_rect)


class Paddle(pg.sprite.Sprite):#パドルクラス 山
    def __init__(self, scrn:Screen):#初期設定
        pg.sprite.Sprite.__init__(self)
        #長方形の作成
        self.image = pg.Surface((100, 10))
        self.image.set_colorkey((0, 0, 0))
        pg.draw.rect(self.image, "blue", (0,0,100,10))
        self.rect = self.image.get_rect()
        self.rect.centerx = scrn.rect.centerx
        self.rect.bottom = scrn.rect.bottom
        self.scrn = scrn
        self.scrn.sfc.blit(self.image, self.rect)#描写

    def update(self):#アップデート関数
        self.rect.centerx = pg.mouse.get_pos()[0]#マウスのx座標と同期する
        self.rect.clamp_ip(self.scrn)#画面外に出ていかないように


class Ball(pg.sprite.Sprite):#ボールクラス 山
    speed = 5#スピード
    #反射角
    angle_left = 135
    angle_right = 45
    count = 3# 残基

    def __init__(self, paddle, scrn:Screen):#初期設定
        pg.sprite.Sprite.__init__(self)
        #長方形の描画
        self.image = pg.Surface((20, 20))
        self.image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.image, "red", (10, 10), 10)
        self.rect = self.image.get_rect()
        self.paddle = paddle
        #アップデートの切り替え
        self.update = self.start
        self.scrn = scrn
        # ボールの速度
        self.dx = 0
        self.dy = 0
        self.count = 3 #残機

    def start(self):#初期座標
        self.rect.centerx = pg.mouse.get_pos()[0]#マウスのx座標に同期
        self.rect.bottom = self.paddle.rect.top
        if pg.mouse.get_pressed()[0] == 1:#左クリックで発射
            self.dx = 0
            self.dy = -self.speed
            self.update = self.move#アップデート切り替え

    def move(self):#移動処理
        if self.rect.bottom == self.scrn.rect.bottom:#落ちた場合
            self.update = self.start
            Ball.count -= 1
        yoko,tate = check_bound(self.rect, self.scrn.rect)#反射チェック

        self.dx = self.dx * yoko
        self.dy = self.dy * tate
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        self.rect.clamp_ip(self.scrn)#画面外に出ないように


def check_bound(obj_rect, scr_rect): #反射チェック関数 山
    yoko,tate = +1,+1
    if obj_rect.left == scr_rect.left or obj_rect.right == scr_rect.right:
        yoko = -1#反転
    if obj_rect.top == scr_rect.top:
        tate = -1#反転
    return yoko, tate


class Block(pg.sprite.Sprite):#ブロッククラス 山 赤嶺
    def __init__(self, scrn:Screen, x, y, judg):#初期設定
        lst = ["red","blue","yellow","green","orange","violet"]#ランダムカラー用リスト
        leststar = [[0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],#星型カラーリスト
                    [0,0,0,0,0,0,1,0,1,0,0,0,0,0,0],
                    [0,0,0,0,0,1,0,0,0,1,0,0,0,0,0],
                    [0,1,1,1,1,0,0,0,0,0,1,1,1,1,0],
                    [0,0,1,0,0,0,0,0,0,0,0,0,1,0,0],
                    [0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
                    [0,0,0,0,1,0,0,1,0,0,1,0,0,0,0],
                    [0,0,0,1,0,0,1,0,1,0,0,1,0,0,0],
                    [0,0,1,0,1,1,0,0,0,1,1,0,1,0,0],
                    [0,1,1,1,0,0,0,0,0,0,0,1,1,1,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
        pg.sprite.Sprite.__init__(self)
        #長方形描画
        self.image = pg.Surface((40, 20))
        self.image.set_colorkey((0, 0, 0))
        if judg > 0.5:#ランダムか星型か判定
            pg.draw.rect(self.image, random.choice(lst), (0,0,30,10))
        else:
            if leststar[y][x] == 1:
                colours = "red"
            else:
                colours = "white"
            pg.draw.rect(self.image, colours, (0,0,30,10))
        self.rect = self.image.get_rect()
        #描画位置設定
        self.rect.left = 5 + scrn.rect.left + x * self.rect.width
        self.rect.top = 5 + scrn.rect.top + y * self.rect.bottom


class Sub_screen(): #スタート画面 宮島
    def button_click(event):
        tkm.showwarning("ルール","マウスパッドをタップでスタート!ポインターを左右に動かしてボールをブロックにぶつけよう!!")

    def start(self):
        root = tk.Tk()
        root.title("start")
        root.geometry("600x250")
        label = tk.Label(root,
                        text="ブロック崩しEX!!",
                        font=("",50)
                        )
        label.pack()
        label = tk.Label(root,
                        text=" ~ 目指せハイスコア!!! ~ ",
                        font=("",30)
                        )
        label.pack()
        #ルールボタン
        button = tk.Button(root, text="ルール", command=self.button_click)
        button.pack()
        label = tk.Label(root,
                        text=" 右上の×ボタンをクリックしてゲームスタート!! ",
                        font=("",20)
                        )
        label.pack()
        root.mainloop()
        self.timerFlag = True

    def end(self, Score, scrn):#終了画面 赤嶺 山
        self.font = pg.font.SysFont(None,55)
        text = self.font.render("GAME OVER",True,(255,0,0))
        scrn.blit(text,(200, 300))
        pg.display.update()
        root = tk.Tk()
        root.title("お疲れ様")
        root.geometry("300x100")
        score = Score.score
        if score > Score.HISCORE:#ハイスコア判定と書き込み
            with open('ex06/text.txt', mode="w", encoding="UTF-8") as file:
                file.write(f"{score}")
        label = tk.Label(root,
                        text=f"お疲れ様{score}点だよ\n前回までのハイスコアは\n{Score.HISCORE}点だよ",
                        font=("", 20)
                        )
        label.pack()
        root.mainloop()


def check_collision(balls, paddle, paddles, blocks, score, bgm):#衝突チェック関数 山
    oldblocks = len(blocks)
    for ball in balls:#各ボールに対して処理を実行
        blocks_collided = pg.sprite.spritecollide(ball, blocks, True)
        paddle_collided = pg.sprite.spritecollide(ball, paddles, False)
        if blocks_collided:#ボールがブロックにぶつかったら
            score.add(oldblocks - len(blocks))#スコア加算
            bgm.Collision_BGM()
            oldrect = ball.rect
            for block in blocks_collided:
                # ボールが左から衝突
                if oldrect.left < block.rect.left < oldrect.right < block.rect.right:
                    ball.rect.right = block.rect.left
                    ball.dx = -ball.dx
                # ボールが右から衝突
                if block.rect.left < oldrect.left < block.rect.right < oldrect.right:
                    ball.rect.left = block.rect.right
                    ball.dx = -ball.dx
                # ボールが上から衝突
                if oldrect.top < block.rect.top < oldrect.bottom < block.rect.bottom:
                    ball.rect.bottom = block.rect.top
                    ball.dy = -ball.dy
                # ボールが下から衝突
                if block.rect.top < oldrect.top < block.rect.bottom < oldrect.bottom:
                    ball.rect.top = block.rect.bottom
                    ball.dy = -ball.dy

        if paddle_collided:#ボールがパドルにぶつかったら
            (x1, y1) = (paddle.rect.left - ball.rect.width, ball.angle_left)
            (x2, y2) = (paddle.rect.right, ball.angle_right)
            x = ball.rect.left                          # ボールが当たった位置
            y = (float(y2-y1)/(x2-x1)) * (x - x1) + y1  # 線形補間
            angle = math.radians(y)                     # 反射角度
            ball.dx = ball.speed * math.cos(angle)
            ball.dy = -ball.speed * math.sin(angle)


class Score():#スコアクラス 山
    def __init__(self):#初期設定
        self.font = pg.font.SysFont("arial", 30)#フォント設定
        self.score = 0
        self.x = 10#x座標
        self.y = 250#y座標
        nums = ""
        with open('ex06/text.txt', mode="r", encoding="UTF-8") as file:# ハイスコア読み込み
            for num in file.readline():
                nums += num
        self.HISCORE = int(nums)

    def draw(self, Ball, scrn:Screen):#スコア描画
        text = self.font.render(f"life{Ball.count} SCORE{self.score}", True, (255,0,255))
        scrn.blit(text,(self.x, self.y))

    def add(self, x):#スコア加算
        self.score += x*10


class BGM: # BGMクラス 松永
    def __init__ (self):# 初期設定
        pg.mixer.init(frequency = 44100)
        self.bgm = pg.mixer.Sound("music/BGM.mp3")     # 音楽ファイルの読み込み
        self.gameover_BGM = pg.mixer.Sound("music/gameover.mp3")
        self.gameclear_BGM = pg.mixer.Sound("music/gameclear.mp3")
        self.collision_BGM = pg.mixer.Sound("music/衝突.mp3")
        self.bgm.set_volume(0.5)  # 音量設定
        self.bgm.play(-1)   # -1でループ再生

    def Gameover_BGM(self): # ゲームオーバーBGMクラス
        self.bgm.stop()
        self.gameover_BGM.set_volume(0.7)
        self.gameover_BGM.play()   # 1回再生

    def Gameclear_BGM(self): # ゲームクリアBGM
        self.bgm.stop()
        self.gameclear_BGM.set_volume(0.7)
        self.gameclear_BGM.play()

    def Collision_BGM(self): # 衝突BGM
        self.collision_BGM.set_volume(0.7)
        self.collision_BGM.play()


class Timer: # タイマークラス 松永
    def __init__(self, xy):#初期設定
        self.sfc = pg.Surface((80, 80))
        self.sfc.set_colorkey((0, 0, 0))
        self.rct = self.sfc.get_rect()
        self.sysfont = pg.font.SysFont(None, 40)
        self.x, self.y = xy

    def up_score(self, value):
        self.score += value

    def blit(self, scrn:Screen, backtime):
        now_time = ((pg.time.get_ticks())/1000)
        img = self.sysfont.render("TIME:" + str(int(now_time-backtime)), True, (0, 0, 0))
        scrn.sfc.blit(img, (self.x, self.y))


def main():# 山
    sttime = time.time()
    scrn = Screen("ブロック崩し", (600, 600), "fig/haikei.jpg")#背景画像 宮島
    group = pg.sprite.OrderedUpdates()  # 描画用のスプライトグループ
    blocks = pg.sprite.Group()       # ブロック衝突判定用のスプライトグループ
    paddles = pg.sprite.Group()      #パドル衝突判定用のスプライトグループ
    paddle = Paddle(scrn)#パドル描画
    group.add(paddle)
    paddles.add(paddle)
    judg = random.random()
    for x in range(0, 15):#ブロック描画
        for y in range(0, 11):
            black = Block(scrn, x, y, judg)
            group.add(black)
            blocks.add(black)
    balls = []# 宮島
    for i in range(2):#ボール複数描写
        ball = Ball(paddle, scrn)
        balls.append(ball)
        group.add(ball)
    clock = pg.time.Clock()
    subscreen = Sub_screen()
    subscreen.start()
    score = Score()#スコア
    poseFlag = False#ポーズフラグ
    bgm = BGM()  # BGM再生
    edtime =time.time()
    timer = Timer((480, 250)) # タイマーを画面(480, 250)に表示
    clock = pg.time.Clock()

    while True:
        scrn.bilt()
        clock.tick(60)      # フレームレート(60fps)
        group.update()        # 全てのスプライトグループを更新
        group.draw(scrn.sfc)    # 全てのスプライトグループを描画
        score.draw(Ball, scrn.sfc)    # スコアを描画
        check_collision(balls, paddle, paddles, blocks, score, bgm)#衝突判定
        timer.blit(scrn, edtime-sttime)#タイマー描写
        #ポーズ判定
        while poseFlag:
            for event in pg.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    poseFlag = not poseFlag
        #ライフ判定
        if Ball.count == 0:
            bgm.Gameover_BGM()
            subscreen.end(score, scrn.sfc)
            return
        if len(blocks) == 0:#ブロックが全て消えたら
            bgm.Gameclear_BGM()
            subscreen.end()
            return
        #イベント判定
        for event in pg.event.get():
            if event.type == QUIT:#×ボタン
                bgm.Gameover_BGM()
                subscreen.end(score, scrn.sfc)
                return
            if event.type == KEYDOWN and event.key == K_ESCAPE:#エスケープキー
                bgm.Gameover_BGM()
                subscreen.end(score, scrn.sfc)
                return
            if event.type == KEYDOWN and event.key == K_n:#Nキー
                pg.quit()
                pg.init()
                main()
                return
            if event.type == KEYDOWN and event.key == K_SPACE:#スペースキー
                poseFlag = not poseFlag
        pg.display.update()


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()