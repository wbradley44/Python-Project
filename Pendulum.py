import numpy as np
import time
from numpy import sin
from numpy import cos
from scipy.integrate import odeint
import pygame as pg
import random

""" 
Assumptions: center point located at 0,0
x1 = l1 sin(theta1)
y1 = -l1cos(theta1)
x2 = x1 + l2 sin(theta2)
y2 = y1 - l2 cos(theta2)
alpha = ddt omega = ddt ddt theta
"""
pg.init()

# Pendulum class stores values of angular displacement, velocity, and acceleration, as well as length and mass of the pendulum.
class pend:
    def __init__(self, m, l, theta1 = 0, l1 = 0):
        self.m = m
        self.l = l
        self.theta = 0
        self.omega = 0
        self.alpha = 0
        self.x = self.l * sin(self.theta) + sin(theta1) * l1
        self.y = -self.l * cos(self.theta) - cos(theta1) * l1

top = pend(1,1)  
bottom = pend(1,1,theta1 = 0, l1 = 1)      

#updates the positions and velocities of the pendulums.
def update(up, dn,t0,t1,tstep):
    #integrate both for the timestep
    #take in initial conditions
    y0 = [up.theta, up.omega, dn.theta, dn.omega]
    # theta 1, omega 1, theta 2, omega 2
    t = np.arange(t0,t1,tstep)
    sol = odeint(omegadot, y0, t, args = (up.m, up.l, dn.m, dn.l))
    #sol is a tx4 arrarys that contains th1, w1, th1, w2
    up.theta = sol[-1,0]
    up.omega = sol[-1,1]
    dn.theta = sol[-1,2]
    dn.omega = sol[-1,3]

#function is used in the update function to solve for the displacement and velocity values
def omegadot(y, t, m1, l1, m2, l2):
    # must be in this form for scipy.integrate.odeint
    g = 9.81
    theta1, omega1, theta2, omega2 = y
    #y is a tuple of theta and omega
    alpha = [omega1, (-g * (2*m1 + m2) * sin(theta1) - m2 * g * sin(theta1-theta2) - 2 * sin(theta1-theta2) * m2 * (omega2**2 * l2 + omega1**2 * l1 * cos(theta1-theta2))) / (l1 * (2 * m1 + m2 - m2 * cos(2*theta1 - 2 * theta2))),omega2, (2 * sin(theta1 - theta2) * (omega1**2 * l1 * (m1+m2) + g * (m1 + m2) * cos(theta1) + omega2**2 * l2 * m2 * cos(theta1-theta2))) / (l2 * (2 * m1 + m2 - m2 * cos(2 * theta1 - 2 * theta2)))]
    #equation defining the angular acceleration of the top pendulum
    return alpha

#transforms the data to coordinates we can use in pygame
def findXY(up,dn):
    scrnsz = int(400*(top.l+bottom.l))
    middlex = int(scrnsz/2)
    up.x = middlex + int(np.round(200*(up.l * sin(up.theta))))
    up.y = middlex + int(np.round(200*(up.l * cos(up.theta))))
    dn.x = middlex + int(np.round(200*(dn.l * sin(dn.theta) + sin(up.theta) * up.l)))
    dn.y = middlex - int(np.round(200*(-dn.l * cos(dn.theta) - cos(up.theta) * up.l)))
    return

#redraws the elements on the screen
def redraw(up,dn):
    screen.fill((255,255,255))
    pg.draw.line(screen,(0,0,0),(int(200*(top.l+bottom.l)), int(200*(top.l+bottom.l))),(up.x,up.y),10)
    pg.draw.line(screen,(0,0,0),(up.x,up.y),(dn.x,dn.y),10)
    cir1 = pg.draw.circle(screen, (200,0,0), (up.x, up.y), 25)
    cir2 = pg.draw.circle(screen, (0,200,0), (dn.x, dn.y), 25)

clock = pg.time.Clock()
screen = pg.display.set_mode([int(400*(top.l+bottom.l)),int(400*(top.l+bottom.l))])

run = True
drop = False
t0 = 0
t1 = .03
tstep =  .005
screen.fill((255,255,255))

#initializes joystick, only takes the first joystick it detects
pg.joystick.init()
try:
    gamepad = pg.joystick.Joystick(0)
    gamepad.init()
except:
    print("No joystick detected, I guess you're not a gamer")
    
#main loop
while run: 
    #os.system('cls')
    #Quit when 'x' is pressed if there is a pygame window open.
    #up arrow sets both pendulums vertically
    #down arrow sets a random position
    #right arrow sets both pendulums to the right
    #left arrow sets both pendulums to the left
    #space starts/stops the simulation
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                top.omega = 0
                bottom.omega = 0
                top.theta = np.pi
                bottom.theta = np.pi - .001
            elif event.key == pg.K_DOWN:
                top.omega = 0
                bottom.omega = 0
                top.theta = random.uniform(-np.pi, np.pi)
                bottom.theta = random.uniform(-np.pi, np.pi)
            elif event.key == pg.K_LEFT:
                top.omega = 0
                bottom.omega = 0
                top.theta = -np.pi/2
                bottom.theta = -np.pi/2
            elif event.key == pg.K_RIGHT:
                top.omega = 0
                bottom.omega = 0
                top.theta = np.pi/2
                bottom.theta = np.pi/2
            elif event.key == pg.K_SPACE:
                drop = not drop
            elif event.key == pg.K_ESCAPE:
                run = False
                top.omega = 0
                bottom.omega = 0
    #right joystick moves first pendulum around
    #left joystick moves second pendulum around
    #'X' button starts/stops simulation
    try:
        if abs(gamepad.get_axis(2)) > 0.2:
            top.theta += gamepad.get_axis(2)*np.pi/20
        elif abs(gamepad.get_axis(0)) > 0.2:
            bottom.theta +=gamepad.get_axis(0)*np.pi/20
        elif gamepad.get_button(1):
            drop = not drop
    except:
        pg.display.flip()
    if drop:
        update(top, bottom,t0,t1+tstep,tstep)
    else:
        top.omega = 0
        bottom.omega = 0
    

    findXY(top,bottom)
    redraw(top,bottom)
    pg.display.flip()
    clock.tick(30) 
    time.sleep(0.03)
