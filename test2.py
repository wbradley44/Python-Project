import pygame as pg
import math
pg.init()

class Ball():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0.01
        self.angle = math.pi/2

    def draw(self, screen):
        pg.draw.circle(screen, (0,0,0), (self.x, self.y), 10)

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

    def drop(self):
        g = 1
        while self.y < 540:
            self.speed += g
            self.y = int(self.y + self.speed )
            if self.y + 10:
                self.speed = 0

def redrawGameWindow():
    screen.fill((255,255,255))
    pg.draw.rect(screen, (100,200,100), (0,550, 600, 50), 0)
    ball.draw(screen)

screen = pg.display.set_mode([600,600])

running = True

ball = Ball(300, 150)
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            keyname = pg.key.name(event.key).upper()
            if keyname == "UP":
                #moves ball up on up arrow press
                ball.y -=10
            elif keyname == "DOWN":
                #moves ball down on down arrow press
                ball.y +=10
            elif keyname == "SPACE":
                ball.drop()
    pg.display.set_caption("height: {}".format(540-ball.y))
    pg.display.flip()
    redrawGameWindow()
pg.quit()
