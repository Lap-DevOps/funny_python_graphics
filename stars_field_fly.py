import math
import random

import pygame as pg

vec2, vec3 = pg.math.Vector2, pg.math.Vector3
RES = WIDTH, HEIGHT = 1200, 800
NUM_STARS = 1500
CENTER = vec2(WIDTH // 2, HEIGHT // 2)
COLORS = 'red blue green orange purple cyan '.split()
Z_DISTANCE = 40
ALPHA = 30


class Star:
    def __init__(self, app):
        self.screen = app.screen
        self.pos3d = self.get_pos3d()
        self.ve1 = random.uniform(0.05, 0.25)
        self.color = random.choice(COLORS)
        self.screen_pos = vec2(0, 0)
        self.size = 10
        self.img = pg.image.load('img/star.png').convert_alpha()
        self.img = pg.transform.scale(self.img, (20,20))
        self.new_img = pg.Surface(self.img.get_size(), pg.SRCALPHA)
        self.fix_new_img()

    def fix_new_img(self):
        for x in range(self.img.get_width()):
            for y in range(self.img.get_height()):
                # Get the color of the pixel
                color = self.img.get_at((x, y))
                # Check if the pixel is not transparent
                if color.a != 0:
                    # Fill the non-transparent pixel with black color
                    blend_color = pg.Color.lerp(color, self.color, 0.5)
                    self.new_img.set_at((x, y), blend_color)

    def get_pos3d(self, scale_poz=35):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.randrange(HEIGHT // scale_poz, HEIGHT) * scale_poz
        x = radius * math.sin(angle)
        y = radius * math.cos(angle)
        return vec3(x, y, Z_DISTANCE)

    def update(self):
        self.pos3d.z -= self.ve1
        self.pos3d = self.get_pos3d() if self.pos3d.z < 1 else self.pos3d
        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
        self.size = (Z_DISTANCE - self.pos3d.z) / (0.2 * self.pos3d.z)

        # rotate xy
        self.pos3d.xy = self.pos3d.xy.rotate(0.2)
        # mouse
        mouse_pos = CENTER - vec2(pg.mouse.get_pos())
        self.screen_pos += mouse_pos

    def draw(self):
        self.screen.blit(self.new_img, (self.screen_pos))
        self.screen.blit(self.img, (self.screen_pos))


class StarField:
    def __init__(self, app):
        self.stars = [Star(app) for star in range(NUM_STARS)]

    def run(self):
        [star.update() for star in self.stars]
        self.stars.sort(key=lambda star: star.pos3d.z, reverse=True)
        [star.draw() for star in self.stars]


class App:
    def __init__(self):
        self.flags = pg.OPENGL | pg.FULLSCREEN
        self.screen = pg.display.set_mode(RES)
        self.alpha_surface = pg.Surface(RES)
        self.alpha_surface.set_alpha(ALPHA)
        self.clock = pg.time.Clock()
        self.starfield = StarField(self)

    def run(self):
        while True:
            self.screen.fill('black')
            self.screen.blit(self.alpha_surface, (0, 0))
            self.starfield.run()

            pg.display.flip()
            [exit() for event in pg.event.get() if event.type == pg.QUIT]
            self.clock.tick(60)


if __name__ == '__main__':
    app = App()
    app.run()
