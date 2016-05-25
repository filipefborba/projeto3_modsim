# -*- coding: utf-8 -*-
"""
Created on Sun May 15 22:00:46 2016

@author: paulinaachurra
"""

import matplotlib.pyplot as plt
from scipy.integrate import odeint
from numpy import linspace 
from math import cos, sin


V0 = [10*cos(1), 10*sin(1)]
R0 = [0,0]
Z0 = [R0[0], R0[1], V0[0], V0[1]]
Tempo = linspace(0,1.7,18)

# Z=[x,y,vx,vy]
def func2(Z,t):
    dxdt = Z[2]
    dydt = Z[3]
    dvxdt = 0
    dvydt = -9.8
    return [dxdt,dydt,dvxdt,dvydt]
        
A = odeint(func2,Z0,Tempo)

plt.plot(A[:,0], A[:,1])
plt.ylabel('y [m]')
plt.xlabel('x [m]')
plt.show()

plt.plot(Tempo, A[:,2])
plt.plot(Tempo, A[:,3])
plt.ylabel('vx, vy [m/s]')
plt.xlabel('Tempo [s]')
plt.show()