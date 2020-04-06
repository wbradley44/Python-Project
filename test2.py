import pygame as pg
import math
import time
pg.init()

class Ball():
    #make a class for the ball that contains the variables for x and y position as well as speed
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bounce = .4
        self.speed = 0
        self.angle = math.pi/2
        self.falling = False
        
    def draw(self, screen):
        #Uses the pygame draw command, but redraws the same ball
        pg.draw.circle(screen, (0,0,0), (self.x, self.y), 10)

    def update(self):
        #this is the position update while the ball is falling
        if self.falling and self.y< 540:
            self.speed += .9
            self.y = int(self.y + self.speed )
        elif self.falling and self.y >= 540:
            self.y = 539
            self.speed = -self.speed * self.bounce
        elif self.falling and self.y > 530 and abs(self.speed) <= 2:
            self.y = 540
            self.speed = 0
            self.falling = False
        elif not self.falling:
            self.speed = 0.0

def redrawGameWindow():
    screen.fill((255,255,255))
    pg.draw.rect(screen, (100,200,100), (0,550, 600, 50), 0)
    ball.update()
    ball.draw(screen)

screen = pg.display.set_mode([600,600])

running = True
clock = pg.time.Clock()
ball = Ball(300, 150)
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            keyname = pg.key.name(event.key).upper()
            if keyname == "UP" and not ball.falling:
                #moves ball up on up arrow press
                ball.y -=10
            elif keyname == "DOWN" and ball.y<540 and not ball.falling:
                #moves ball down on down arrow press
                ball.y +=10
            elif keyname == "SPACE":
                ball.falling =  not ball.falling
    pg.display.set_caption("height: {} speed: {:.2f}".format(540-ball.y, ball.speed))
    pg.display.flip()
    redrawGameWindow()
    
    clock.tick(10)
    time.sleep(.1)
    #sets the framerate to 10/s and the refresh rate to the same
    #this prevents the code from executing faster than the framerate
pg.quit()
