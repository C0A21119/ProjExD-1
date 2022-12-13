import pygame as pg
import sys
import tkinter as tk
from tkinter import messagebox as tkm
import time



def timer(st):
    nowtm = time.time() - st
    nowtm//=1
    return int(nowtm)

def main():
    st = time.time()
    pg.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = pg.display.set_mode((1600, 900))
    scrn_rct = scrn_sfc.get_rect()
    bg_sfc = pg.image.load("fig/pg_bg.jpg")
    bg_rct = bg_sfc.get_rect()

    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 800, 450
    scrn_sfc.blit(tori_sfc,tori_rct)
    clock = pg.time.Clock()

    pg.display.update()
    clock.tick(1000)
    print(timer(st))


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
