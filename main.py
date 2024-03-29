import random
from math import cos, sin, radians
import time

import pygame
import sys

size = width, height = 800, 600
black = 0, 0, 0
color = [0, 255, 0]

class Ball:
    filename = 'basketball.png'

    def __init__(self, x=100, y=100):
        self.image = pygame.image.load(Ball.filename)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.x = x
        self.y = y

    def process_event(self, event):
        pass

    def process_logic(self):
        pass

    def process_draw(self, screen):
        screen.blit(self.image, self.rect)


class MovingBall(Ball):
    def __init__(self, c_x=200, c_y=200, c_r=150, c_delta=5):
        super().__init__()
        self.center_x = c_x
        self.center_y = c_y
        self.center_radius = c_r
        self.center_delta = c_delta
        self.alpha = 0

    def process_logic(self):
        self.alpha += self.center_delta
        self.rect.centerx = self.center_x - self.rect.width // 2 + self.center_radius * cos(radians(self.alpha))
        self.rect.centery = self.center_y - self.rect.height // 2 + self.center_radius * sin(radians(self.alpha))


class LinearMovingBall(Ball):
    def __init__(self, window_width, window_height):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height
        self.rect.x = random.randint(10, self.window_width - self.rect.width - 10)
        self.rect.y = random.randint(10, 200)
        self.shift_x = 1 if random.randint(0, 1) == 1 else -1
        self.shift_y = 1 if random.randint(0, 1) == 1 else -1

    def process_logic(self):
        self.rect.x += self.shift_x
        self.rect.y += self.shift_y
        if self.rect.left <= 0 or self.rect.right >= self.window_width:
            self.shift_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= self.window_height:
            self.shift_y *= -1

    def collides_with_plat(self, platform):
        if platform.y == self.rect.y + 100 and (self.rect.x >= platform.x - 50 and self.rect.x <= platform.x + 100):
            return True

    def collision(self, other_ball):
        self.shift_x, other_ball.shift_x = other_ball.shift_x, self.shift_x
        self.shift_y, other_ball.shift_y = other_ball.shift_y, self.shift_y



class Platform:
    def __init__(self, x = width // 2, y = height // 2 + 100):
        self.x = x
        self.y = y

    def process_draw(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, 100, 50), 5)

    def process_logic(self, current_shift):
        if current_shift == -1:
            if self.x != 0:
                self.x -= 2
        elif current_shift == 1:
            if self.x <= width - 100:
                self.x += 2


def main():
    global width
    global height
    global size
    current_shift = 0
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    font = pygame.font.SysFont('Comic Sans MS', 100, True)
    ts = font.render("", False, (255, 255, 255))
    objects = []
    for i in range(3):
        objects.append(LinearMovingBall(width, height))

    plat = Platform()
    flag_stop_platform = False # Флаг для остановки платформы после проигрыша
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.VIDEORESIZE:
                size = width, height = event.w, event.h
                screen = pygame.display.set_mode(size, pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN and flag_stop_platform == False:
                if chr(event.key) == 'a':
                    current_shift = -1
                elif chr(event.key) == 'd':
                    current_shift = 1
            elif event.type == pygame.KEYUP:
                if event.key in [97, 100]:
                    current_shift = 0
        for item in objects:
            if item.rect.y == height - 100:
                ts = font.render("Game Over", False, (255, 255, 255))
                item.shift_y, item.shift_x = 0, 0
                flag_stop_platform = True


        plat.process_logic(current_shift)
        for item in objects:
            item.process_logic()

        for item in objects:
            if item.collides_with_plat(plat):
                item.shift_y = -1


        screen.fill(black)

        for item in objects:
            item.process_draw(screen)
        screen.blit(ts, (125,200))
        plat.process_draw(screen, (0,255,100))
        pygame.display.flip()
        pygame.time.wait(10)

        if flag_stop_platform:
            time.sleep(2)
            game_over = True


    sys.exit()


if __name__ == '__main__':
    main()