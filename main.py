import math
import pygame
import sys
from random import choice
from random import randint
from pygame.sysfont import SysFont
from pygame.sprite import Group
from pygame.sprite import Sprite
import time

FPS = 60


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
y = randint(300, 550)

class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=550):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y + gun.movey
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
        self.vy += 125 * (1/30)
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


class Gun(Sprite):
    def __init__(self, screen):
        super(Gun, self).__init__()
        self.live = 1
        self.screen = screen
        self.f2_power = 0
        self.f2_on = 1
        self.an = 1
        self.color = GREY
        self.movey = 0
        self.image = pygame.image.load('images/Пушка.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.rect.centery = (500 + self.movey + 550 + l * self.an + self.movey) // 2
        self.rect.x = 0
        self.i = 0
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
        if self.i % 2 == 0:
            new_ball.r += 0
        else:
            new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y),(event.pos[0]-new_ball.x))
        new_ball.vx = 1.25 * self.f2_power * math.cos(self.an)
        new_ball.vy = 1.25 * self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 1
        self.f2_power = 150

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if (event.pos[0] - 20) == 0:
            self.an = math.pi / 2
        else:
            self.an = math.atan((event.pos[1] - 450) / (event.pos[0] - 20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        self.screen.blit(self.image, self.rect)
        pygame.draw.line(
            self.screen,
            self.color,
            (40, 550 + self.movey), (l * math.cos(self.an) + 40, 550 + l * math.sin(self.an) + self.movey),
            20
        )
        self.screen.blit(self.image, self.rect)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 300:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY
    def moving_up(self):
        if up == True:
            self.movey -= 5
            self.rect.centery -= 5
            self.rect.x = 0

    def moving_down(self):
        if down == True:
            self.movey += 5
            self.rect.centery += 5
            self.rect.x = 0

    def gun_kill(self, Bomblist):
            Bomblist.empty()
            time.sleep(1)
            self.live -= 1
            screen.blit(text, text_rect)


class Target:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        x = self.x = randint(600,700)
        y = self.y = randint(300, 550)
        r = self.r = 30
        color = self.color = RED
        self.points = 0
        self.vy = 5
    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = randint(200, 780)
        y = self.y = randint(100, 550)
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
    def move(self):
        if ((-self.r + self.y) < 0) and self.vy < 0:
            self.vy = 5
        elif ((self.r + self.y) > 600) and self.vy > 0:
            self.vy = -5
        self.y += self.vy
class Target1:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.x = randint(600,700)
        self.y = randint(350, 600)
        self.r = 15
        self.color = BLUE
        self.points = 0
        self.vx = 5
        points = 1
    def new_target1(self):
        """ Инициализация новой цели. """
        x = self.x = randint(200, 780)
        y = self.y = randint(100, 500)
        r = self.r = 15
        color = self.color = BLUE

    def hit(self, points = 1):
        """Попадание шарика в цель."""
        self.points += 1
        points = self.points

    def move(self):
        if ((-self.r + self.x) < 0) and self.vx < 0:
            self.vx = 5
        elif ((self.r + self.x) > 800) and self.vx > 0:
            self.vx = -5
        self.x += self.vx

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )


class Bombs(pygame.sprite.Sprite): #РОДИТЕЛЬСКИЙ КЛАСС SPRITE
    def __init__(self,screen):
        "привязываем пулю к шарику"
        super(Bombs, self).__init__() # наследуем init от класса sprite
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 2, 12)
        self.color = (0, 0, 0)
        self.speed = 4.5
        self.rect.centerx = target1.x
        self.rect.bottom = target1.y + target1.r
        self.y = float(self.rect.y)

    def moving(self):
        "Перемещение пули"
        self.y += self.speed
        self.rect.y = self.y

    def draw_balls(self):
        "Рисуем пулю"
        pygame.draw.rect(self.screen, self.color, self.rect)




pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
Bomblist = Group()
lives = 1

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
target1 = Target1(screen)
finished = False
r = pygame.Rect(40, 40, 120, 120)
pygame.draw.rect(screen, (255, 0, 0), r, 0)
up = False
down = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    target1.draw()
    gun.moving_down()
    target.move()
    target1.move()
    gun.self.i += 1
    font = pygame.font.Font(None, 36)
    closing = "Ты проиграл, твой счет:" +  " " + str(target.points + target1.points)
    text = font.render( closing, True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (800 // 2, 600 // 2)
    if gun.live == 0:
        finished = True
        time.sleep(5)
    if pygame.sprite.spritecollideany(gun, Bomblist):
        gun.gun_kill(Bomblist)
    gun.moving_up()
    for Balls in Bomblist.sprites():
        Balls.draw_balls()
        Balls.moving()
    number = "Очки:" + " " + str(target.points + target1.points)
    SysFont(None, 10, bold=False, italic=False)
    font = pygame.font.SysFont('couriernew', 40)
    text = font.render(number, True, GREEN)
    screen.blit(text, (50, 50))
    keys = pygame.key.get_pressed()
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
        elif event.type == pygame.KEYDOWN:  # ТИП СОБЫТИЯ НАЖАТАЯ КЛАВИША
            # право
            if event.key == pygame.K_w:
                up = True
            # лево
            elif event.key == pygame.K_s:
                down = True
            elif event.key == pygame.K_SPACE:
                new_bomb = Bombs(screen)
                Bomblist.add(new_bomb)
        elif event.type == pygame.KEYUP:
            # право
            if event.key == pygame.K_w:
                up = False
            # лево
            elif event.key == pygame.K_s:
                down = False

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