
import os
import numpy as np
import time
from numpy import sin
from numpy import cos
from scipy.integrate import odeint
import pygame as pg
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

""" 
Assumptions: center point located at 0,0
x1 = l1 sin(theta1)
y1 = -l1cos(theta1)
x2 = x1 + l2 sin(theta2)
y2 = y1 - l2 cos(theta2)
alpha = ddt omega = ddt ddt theta
"""
pg.init()
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

def update(up, dn,t0,t1,tstep):
    #integrate both for the timestep
    #take in initial conditions
    y0 = [up.theta, up.omega, dn.theta, dn.omega]
    # theta 1, omega 1, theta 2, omega 2
    t = np.arange(t0,t1,tstep)
    sol = odeint(omegadot, y0, t, args = (up.m, up.l, dn.m, dn.l))
    #sol is a tx4 arrarys that contains th1, w1, th1, w2
    plt.plot(t, sol[:,0], 'b', label = 'theta(t)')

def omegadot(y, t, m1, l1, m2, l2):
    # must be in this form for scipy.integrate.odeint
    g = 9.81
    theta1, omega1, theta2, omega2 = y
    #y is a tuple of theta and omega
    alpha = [omega1, (-g * (2*m1 + m2) * sin(theta1) - m2 * g * sin(theta1-theta2) - 2 * sin(theta1-theta2) * m2 * (omega2**2 * l2 + omega1**2 * l1 * cos(theta1-theta2))) / (l1 * (2 * m1 + m2 - m2 * cos(2*theta1 - 2 * theta2))),omega2, (2 * sin(theta1 - theta2) * (omega1**2 * l1 * (m1+m2) + g * (m1 + m2) * cos(theta1) + omega2**2 * l2 * m2 * cos(theta1-theta2))) / (l2 * (2 * m1 + m2 - m2 * cos(2 * theta1 - 2 * theta2)))]
    #equation defining the angular acceleration of the top pendulum
    return alpha

def findXY(up,dn):
    up.x = up.l * sin(up.theta)
    up.y = -up.l * cos(up.theta)
    dn.x = dn.l * sin(dn.theta) + sin(up.theta) * up.l
    dn.y = -dn.l * cos(dn.theta) - cos(up.theta) * up.l
    return

def redraw(up,dn):
    ln1 = ax.plot((0,up.x),(0,up.y),lw=4)
    ln2 = ax.plot((up.x,dn.x),(up.y,dn.y),lw=4)
    cir1 = Circle((up.x,up.y),.15,fc = 'b', zorder = 10)
    cir2 = Circle((dn.x,dn.y),.15,fc = 'r', zorder = 10)
    ax.add_patch(cir1)
    ax.add_patch(cir2)
    plt.show()
clock = pg.time.Clock()
fig, ax = plt.subplots()
ax.set_xlim(-1.5*(top.l+bottom.l),1.5*(top.l+bottom.l))
ax.set_ylim(-1.5*(top.l+bottom.l),1.5*(top.l+bottom.l))
ax.set_aspect('equal', adjustable='box')
plt.axis('off')

run = True
drop = False
t0 = 0
t1 = .03
inc = .03
tstep =  .005
screen = pg.display.set_mode([600,600])
while run: 
    #os.system('cls')
    print(top.theta)
    #Quit when 'x' is pressed if there is a pygame window open.
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                top.theta = np.pi
                bottom.theta = np.pi
            elif event.key == pg.K_DOWN:
                top.theta = np.random.rand(-np.pi,np.pi)
                bottom.theta = np.random.rand(-np.pi,np.pi)
            elif event.key == pg.K_LEFT:
                top.theta = -np.pi/2
                bottom.theta = -np.pi/2
            elif event.key == pg.K_RIGHT:
                top.theta = np.pi/2
                bottom.theta = np.pi/2
            elif event.key == pg.K_SPACE:
                drop = True
            elif event.key == pg.K_ESCAPE:
                run = False
    if drop:
        update(top, bottom,t0,t1+tstep,tstep)
        t0,t1 = t1,t1+inc
    findXY(top,bottom)
    redraw(top,bottom)
    clock.tick(30) 
    time.sleep(0.03)
