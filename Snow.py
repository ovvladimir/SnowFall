import pygame
import random
import sys
import time
import os
# from ctypes import windll
os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'

pygame.init()

FPS = 60
clock = pygame.time.Clock()

Info = pygame.display.Info()
MAX_X, MAX_Y = pygame.display.list_modes()[0]  # for FULLSCREEN
MIN_X, MIN_Y = Info.current_w * 100 // 125, Info.current_h * 100 // 125
# MIN_X, MIN_Y = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
MAX_SNOW = 150  # кол-во снежинок
SNOW_SIZE = 64  # размер снежинки
BG_COLOR = (25, 25, 25)


class Snow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = random.randint(1, 3)
        self.img_num = random.randint(1, 2)
        self.SNOW_SIZE = random.randint(32, 64)
        self.image_filename = f'Snowflakes/snowflake{self.img_num}.png'
        self.image_orig = pygame.image.load(self.image_filename)
        self.image_orig = pygame.transform.scale(self.image_orig, (self.SNOW_SIZE, self.SNOW_SIZE))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect(center=(x, y))

        self.rot = 0
        self.angle = random.randint(-1, 1)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > MAX_Y:
            self.rect.y = -self.SNOW_SIZE  # снежинка падает вниз и плавно появляется сверху

        n = random.randint(1, 3)
        if n == 1:  # направо
            self.rect.x += 2
            if self.rect.x > MAX_X:
                self.rect.x = -self.SNOW_SIZE
        elif n == 2:  # налево
            self.rect.x -= 2
            if self.rect.x < -self.SNOW_SIZE:
                self.rect.x = MAX_X

        self.rot = (self.rot + self.angle) % 360
        self.image = pygame.transform.rotate(self.image_orig, self.rot)
        self.rect = self.image.get_rect(center=self.rect.center)


def initialize_snow(max_snow):
    for _ in range(max_snow):
        snow = Snow(random.randint(0, MAX_X), random.randint(0, MAX_Y))
        snowfall.add(snow)


def check_for_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            fscreen.reverse()
            if fscreen[0] == 1:
                screen = pygame.display.set_mode((MIN_X, MIN_Y))
            elif fscreen[0] == 2:
                screen = pygame.display.set_mode((MAX_X, MAX_Y), pygame.FULLSCREEN)


' ______________________MAIN___________________ '

pygame.display.set_icon(pygame.image.load('snow.ico'))
pygame.display.set_caption('Снегопад')
pygame.mouse.set_visible(False)

# screen = pygame.display.set_mode((MAX_X, MAX_Y), pygame.FULLSCREEN)
screen = pygame.display.set_mode((MIN_X, MIN_Y))
fscreen = [1, 2]
snowfall = pygame.sprite.Group()
initialize_snow(MAX_SNOW)

while True:
    check_for_exit()
    snowfall.update()
    screen.fill(BG_COLOR)
    snowfall.draw(screen)

    pygame.display.update()
    clock.tick(FPS)
