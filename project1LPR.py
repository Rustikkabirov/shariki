import math
import sys
from random import choice
from random import randint
from pygame.sysfont import SysFont
import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
point = 0
WIDTH = 800
HEIGHT = 600
l = 50


class Ball:
    def __init__(self, screen: pygame.Surface, x=0, y=500):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        self.x += self.vx * (1/30)
        self.vy += 90 * (1/30)
        self.y += self.vy * (1/30)

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, target):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (target.x - self.x)**2  + (target.y - self.y)**2 <= (target.r + self.r)**2:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 275
        self.f2_on = 150
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 150
        self.f2_power = 275

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(
            self.screen,
            self.color,
            (0, 500), (30, 500 + l * self.an),
            5
        )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 275:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        x = self.x = randint(600,700)
        y = self.y = randint(300, 550)
        r = self.r = 30
        color = self.color = RED
        self.points = 0
    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = randint(600, 780)
        y = self.y = randint(300, 550)
        r = self.r = 30
        color = self.color = RED
    def hit(self, points = 1):
        """Попадание шарика в цель."""
        self.points += 1
        points = self.points

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
class Target1:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        x = self.x = randint(600,700)
        y = self.y = randint(300, 550)
        r = self.r = 15
        color = self.color = BLUE
        self.points = 0
        points = 1
    def new_target1(self):
        """ Инициализация новой цели. """
        x = self.x = randint(600, 780)
        y = self.y = randint(300, 550)
        r = self.r = 15
        color = self.color = BLUE

    def hit(self, points = 1):
        """Попадание шарика в цель."""
        self.points += 1
        points = self.points

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
target1 = Target1(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    target1.draw()
    number = "Очки:" + " " + str(target.points + target1.points)
    SysFont(None, 10, bold=False, italic=False)
    font = pygame.font.SysFont('couriernew', 40)
    text = font.render(number, True, GREEN)
    screen.blit(text, (50, 50))
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target):
            balls.remove(b)
            target.hit()
            target.new_target()
        elif b.hittest(target1):
            balls.remove(b)
            target1.hit()
            target1.new_target1()
    gun.power_up()

pygame.quit()
