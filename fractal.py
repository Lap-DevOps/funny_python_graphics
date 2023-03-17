import numpy as np
import pygame as pg
import numba

# settings
RES = WIDTH, HEIGTH = 800, 450
ofset = np.array([1.3 * WIDTH, HEIGTH]) // 2
max_iter = 30
zoom = 2.2 / HEIGTH

# texture

texture = pg.image.load('img/gradient.jpeg')
texture_size = min(texture.get_size()) - 1
texture_array = pg.surfarray.array3d(texture)


class Fractal:
    def __init__(self, app):
        self.app = app
        self.screen_array = np.full((WIDTH, HEIGTH, 3), [0, 0, 0], dtype=np.uint8)
        self.x = np.linspace(0, WIDTH, num=WIDTH, dtype=np.float32)
        self.y = np.linspace(0, HEIGTH, num=HEIGTH, dtype=np.float32)

    @staticmethod
    @numba.njit(fastmath=True, parallel =True)
    def render(screen_array):
        for x in numba.prange(WIDTH):
            for y in range(HEIGTH):
                c = (x - ofset[0]) * zoom + 1j * (y - ofset[1]) * zoom
                z = 0
                num_iter = 0
                for i in range(max_iter):
                    z = z ** 2 + c
                    if z.real ** 2 + z.imag ** 2 > 4:
                        break
                    num_iter += 1
                col = int(texture_size * num_iter / max_iter)
                screen_array[x,y] = texture_array[col, col]
        return screen_array

    def update(self):
        self.screen_array = self.render(self.screen_array)

    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)

    def run(self):
        self.update()
        self.draw()


class App:
    def __init__(self):
        self.screen = pg.display.set_mode(RES, pg.SCALED)
        self.clock = pg.time.Clock()
        self.fractal = Fractal(self)

    def run(self):
        while True:
            self.screen.fill('black')
            self.fractal.run()
            pg.display.update()

            [exit() for event in pg.event.get() if event.type == pg.QUIT]
            self.clock.tick()
            pg.display.set_caption(f'FPS {self.clock.get_fps()}')


if __name__ == '__main__':
    app = App()
    app.run()
