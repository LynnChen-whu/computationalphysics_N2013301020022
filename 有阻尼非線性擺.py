#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
擺
Created on Wed May 11 09:46:29 2016

@author: 冥凝
"""

import math
import matplotlib.pyplot as mp
import easygui as eg
from mpl_toolkits.mplot3d import Axes3D as axes3d
import numpy as np
from matplotlib import animation

class Pendulum(object):
    def __init__(self,r,theta0,name,m=1,fn=0,v=0,dt=0.001): # fn量綱是“N/(m/s)”
        self.name=name
        self.m=m
        self.r=r
        self.theta0=theta0
        self.theta=[theta0]
        self.dt=dt
        self.t=[0]
        self.top_t=[0]
        self.T=[]
        self.v=v
        self.g=9.8
        self.fn=fn
    def move(self,step=10):
        if len(self.theta)<step:
            self.v=self.v+self.g*np.sin(self.theta[0])*self.dt
            self.theta.insert(0,self.theta[0]-self.v/self.r*self.dt)
            self.t.insert(0,self.t[0]+self.dt)    
        else:
            self.v=self.v+self.g*np.sin(self.theta[0])*self.dt
            self.theta.insert(0,self.theta[0]-self.v/self.r*self.dt)
            self.theta.pop
            self.t.insert(0,self.t[0]+self.dt)    
            self.t.pop
        self.v=self.v-self.v*self.fn/self.m*self.dt      
        if len(self.t)>2 and self.theta[0]<self.theta[1]>self.theta[2]:
            self.top_t.insert(0,self.t[1])
            self.T.insert(0,self.top_t[0]-self.top_t[1])
            print(self.t[1],self.name)
            
p1=Pendulum(r=10,theta0=math.pi/9,fn=0,v=0,m=10,name='p1')
p2=Pendulum(r=10,theta0=math.pi/9,fn=0.7,v=0,m=10,name='p2')


fig=mp.figure() 
#ax1=axes3d(fig)
#ax1.set_xticks([i*10 for i in range(11)]) #X轴刻度
ax1=fig.add_subplot(1,1,1,xlim=(0,100),ylim=(-7,7),xlabel='t/s',ylabel='theta/pi')
line1,=ax1.plot([],[],lw=2,c='r') 
'''下面這條線顯示週期的變化'''
line11,=ax1.plot([],[],lw=1,c='r')
line2,=ax1.plot([],[],lw=2,c='g') 
line22,=ax1.plot([],[],lw=1,c='g') 


def init():  
    line1,=ax1.plot([],[],lw=2,c='r') 
    line11,=ax1.plot([],[],lw=1,c='r') 
    line2,=ax1.plot([],[],lw=2,c='g') 
    line22,=ax1.plot([],[],lw=1,c='g') 
    return line1,line11,line2,line22
    
def animate(i):
    p1.move()   
    x1=p1.t 
    y1=np.array(p1.theta)
    y1=y1*5
    line1.set_data(x1,y1)
    x11=p1.top_t[0:-1]
    y11=np.array(p1.T)
    y11=(y11**4)/300
    line11.set_data(x11,y11)
    p2.move()   
    x2=p2.t 
    y2=np.array(p2.theta)
    y2=y2*5
    line2.set_data(x2,y2)
    x22=p2.top_t[0:-1]
    y22=np.array(p2.T)
    y22=y22**4/300
    line22.set_data(x22,y22)
    return line1,line11,line2,line22
    
anim1=animation.FuncAnimation(fig,animate,init_func=init,interval=0.1,blit=True)  
mp.show()






