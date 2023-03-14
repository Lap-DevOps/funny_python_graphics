import pygame as pg

RES = WIDTH, HIGHT = 1200, 800

pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()

font = pg.font.SysFont('Vernada', 200)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
