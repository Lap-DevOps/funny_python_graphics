import math
from datetime import datetime

import pygame as pg

RES = WIDTH, HEIGHT = 1200, 800
H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2
RADIUS = H_HEIGHT - 50
RADIUS_ARK = RADIUS + 8
radius_list = {'sec': RADIUS - 10, 'min': RADIUS - 55, 'hour': RADIUS - 100, 'digit': RADIUS - 30}

pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()

clock12 = dict(zip(range(12), range(0, 360, 30)))
clock60 = dict(zip(range(60), range(0, 360, 6)))

img = pg.image.load('img/red-space-05.jpg').convert_alpha()
bg = pg.image.load('img/wallpaper.jpg').convert()
img = pg.transform.scale(img, RES)
bg_rect = bg.get_rect()
bg_rect.center = WIDTH, HEIGHT
dx, dy = 1, 1

font = pg.font.SysFont('Vernada', 60)


def get_clock_pos(clock_dict, clock_hand, key):
    x = H_WIDTH + radius_list[key] * math.cos(math.radians(clock_dict[clock_hand]) - math.pi / 2)
    y = H_HEIGHT + radius_list[key] * math.sin(math.radians(clock_dict[clock_hand]) - math.pi / 2)
    return x, y


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

    # set background
    dx *= -1 if bg_rect.left > 0 or bg_rect.right < WIDTH else 1
    dy *= -1 if bg_rect.top > 0 or bg_rect.bottom < HEIGHT else 1
    bg_rect.centerx += dx
    bg_rect.centery += dy

    # create the circular surface
    size = surface.get_size()
    cropped_background = pg.Surface(size, pg.SRCALPHA)
    pg.draw.circle(cropped_background, (255, 255, 255, 255), (H_WIDTH, H_HEIGHT), RADIUS_ARK)
    cropped_background.blit(bg, bg_rect, special_flags=pg.BLEND_RGBA_MIN)
    surface.blit(img, (0, 0))
    surface.blit(cropped_background, (0, 0))

    # get time
    time = datetime.now()
    hour, minute, second = ((time.hour % 12) * 5 + time.minute // 12), time.minute, time.second
    
    # draw face
    for digit, pos in clock60.items():
        radius = 20 if not digit % 3 and not digit % 5 else 8 if not digit % 5 else 2
        pg.draw.circle(surface, (175,15,15), get_clock_pos(clock60, digit, 'digit'), radius, 7)

    # draw clock
    pg.draw.line(surface, pg.Color('orange'), (H_WIDTH, H_HEIGHT), get_clock_pos(clock60, hour, 'hour'), 15)
    pg.draw.line(surface, pg.Color('green'), (H_WIDTH, H_HEIGHT), get_clock_pos(clock60, minute, 'min'), 7)
    pg.draw.line(surface, pg.Color('magenta'), (H_WIDTH, H_HEIGHT), get_clock_pos(clock60, second, 'sec'), 4)
    pg.draw.circle(surface, pg.Color('white'), (H_WIDTH, H_HEIGHT), 8)

    # draw digital clock
    time_render = font.render(f'{time:%H:%M:%S}', True, pg.Color('forestgreen'), pg.Color('orange'))
    surface.blit(time_render, (10, 10))

    # draw arc
    sec_angle = -math.radians(clock60[time.second]) + math.pi / 2
    pg.draw.arc(surface, pg.Color('magenta'),
                (H_WIDTH - RADIUS_ARK, H_HEIGHT - RADIUS_ARK, 2 * RADIUS_ARK, 2 * RADIUS_ARK),
                math.pi / 2, sec_angle, 8)

    pg.display.flip()
    clock.tick(20)
