# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 17:15:58 2020

@author: Admin
"""

import numpy as np
from numpy import sin
from numpy import cos
from scipy.integrate import odeint
import pygame as pg
import matplotlib.pyplot as plt

""" 
Assumptions: center point located at 0,0
x1 = l1 sin(theta1)
y1 = -l1cos(theta1)
x2 = x1 + l2 sin(theta2)
y2 = y1 - l2 cos(theta2)
alpha = ddt omega = ddt ddt theta
"""

class pend:
    def __init__(self, m, l, theta1 = 0, l1 = 0):
        self.m = m
        self.l = l
        self.theta = 0
        self.omega = 0
        self.alpha = 0
        self.x = self.l * sin(self.theta) + sin(theta1) * l1
        self.y= -self.l * cos(self.theta) - cos(theta1) * l1

top = pend(1,1)  
bottom = pend(1,1,theta1 = 0, l1 = 1)      

def update(up, dn,t0 = 0,t1 = 10,tstep = .1):
    #integrate both for the timestep
    #take in initial conditions
    y0 = [up.theta, up.omega, dn.theta, dn.omega]
    # theta 1, omega 1, theta 2, omega 2
    t = np.arange(t0, t1, tstep)
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

    
