import pygame as pg
import math
import sys

from pygame.locals import *

class Screen(pg.sprite.Sprite):
    def __init__(self, title, wh_pos:tuple, file_path):
        pg.sprite.Sprite.__init__(self)
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh_pos)
        self.rect = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(file_path)
        self.bgi_rect = self.bgi_sfc.get_rect()

    def bilt(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rect)

class Paddle(pg.sprite.Sprite):
    def __init__(self, scrn:Screen):#引数にパドルのイメージ画像
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((100, 10))
        self.image.set_colorkey((0, 0, 0))
        pg.draw.rect(self.image, "blue", (0,0,100,10))
        self.rect = self.image.get_rect()
        self.rect.centerx = scrn.rect.centerx
        self.rect.bottom = scrn.rect.bottom
        self.scrn = scrn
        self.scrn.sfc.blit(self.image, self.rect)

    def update(self):
        self.rect.centerx = pg.mouse.get_pos()[0]
        self.rect.clamp_ip(self.scrn)

class Ball(pg.sprite.Sprite):
    speed = 5
    angle_left = 135
    angle_right = 45

    def __init__(self, paddle, scrn:Screen):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((20, 20))
        self.image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.image, "red", (10, 10), 10)
        self.rect = self.image.get_rect()
        self.paddle = paddle
        self.update = self.start
        self.scrn = scrn
        self.dx = 0 # ボールの速度
        self.dy = 0

    def start(self):
        self.rect.centerx = pg.mouse.get_pos()[0]
        self.rect.bottom = self.paddle.rect.top
        if pg.mouse.get_pressed()[0] == 1:
            self.dx = 0
            self.dy = -self.speed
            self.update = self.move

    def move(self):
        if self.rect.top > self.scrn.rect.bottom:
            self.update = self.start
        yoko,tate = check_bound(self.rect, self.scrn.rect)
        self.dx = self.dx * yoko
        self.dy = self.dy * tate
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
class Block(pg.sprite.Sprite):
    def __init__(self, scrn:Screen, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((40, 20))
        self.image.set_colorkey((0, 0, 0))
        pg.draw.rect(self.image, "blue", (0,0,30,10))
        self.rect = self.image.get_rect()
        self.rect.left = 5 + scrn.rect.left + x * self.rect.width
        self.rect.top = 5 + scrn.rect.top + y * self.rect.bottom

def check_collision(ball, paddle, paddles, blocks):
    blocks_collided = pg.sprite.spritecollide(ball, blocks, True)
    paddle_collided = pg.sprite.spritecollide(ball, paddles, False)
    if blocks_collided:
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
    if paddle_collided:
        (x1, y1) = (paddle.rect.left - ball.rect.width, ball.angle_left)
        (x2, y2) = (paddle.rect.right, ball.angle_right)
        x = ball.rect.left                          # ボールが当たった位置
        y = (float(y2-y1)/(x2-x1)) * (x - x1) + y1  # 線形補間
        angle = math.radians(y)                     # 反射角度
        ball.dx = ball.speed * math.cos(angle)
        ball.dy = -ball.speed * math.sin(angle)

def check_bound(obj_rect, scr_rect): #衝突チェック関数
    yoko,tate = +1,+1
    if obj_rect.left < scr_rect.left or obj_rect.right > scr_rect.right:
        yoko = -1
    if obj_rect.top < scr_rect.top:
        tate = -1
    return yoko, tate


def main():
    scrn = Screen("ブロック崩し", (600, 600), "fig/pg_bg.jpg")
    group = pg.sprite.OrderedUpdates()  # 描画用のスプライトグループ
    blocks = pg.sprite.Group()       # 衝突判定用のスプライトグループ
    paddles = pg.sprite.Group()
    paddle = Paddle(scrn)
    group.add(paddle)
    paddles.add(paddle)
    for x in range(0, 15):
        for y in range(0, 11):
            black = Block(scrn, x, y)
            group.add(black)
            blocks.add(black)
    ball = Ball(paddle, scrn)
    group.add(ball)
    clock = pg.time.Clock()

    while True:
        scrn.bilt()
        clock.tick(60)      # フレームレート(60fps)
        group.update()        # 全てのスプライトグループを更新
        group.draw(scrn.sfc)    # 全てのスプライトグループを描画
        check_collision(ball, paddle, paddles, blocks)
        pg.display.update()
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pg.quit()
                sys.exit()

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit() # 初期化の解除
    sys.exit()