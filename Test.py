# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 20:53:11 2020

@author: Admin
"""

import pygame as pg
pg.init()

def drop(scrn, pos, ball):
    # takes the kinematic equations and applies them while the ball is above the ground
    speed = 0
    g = 9.81
    while pos<540:
        speed = speed + .1 + g
        pos = int(pos + (speed + .5 * g * .1 ** 2)) 
        if pos >540:
            pos = 540
        ball = pg.draw.circle(screen, (0,0,0), (300, pos), 10)
        # draws all the balls at once for some reason
        pg.display.set_caption("height: {} speed: {}".format(540-pos, speed))
        pg.display.flip()
    return

screen = pg.display.set_mode([600,600])
ballpos = 150
running = True
clock = pg.time.Clock()
while running:
    clock.tick(10)
    #sets to 10 fps
    screen.fill((255,255,255))
    #fills screen with white
    ball = pg.draw.circle(screen, (0,0,0), (300, ballpos), 10)
    #draws a black circle
    pg.draw.rect(screen, (100,200,100), (0,550, 600, 50), 0)
    #draws the rectangle that is the ground
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            keyname = pg.key.name(event.key).upper()
            if keyname == "UP":
                #moves ball up on up arrow press
                ballpos -=10
            elif keyname == "DOWN":
                #moves ball down on down arrow press
                ballpos +=10
            elif keyname == "SPACE":
                drop(screen, ballpos, ball)
    pg.display.set_caption("height: {}".format(540-ballpos))
    pg.display.flip()
pg.quit()

