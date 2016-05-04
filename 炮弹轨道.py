#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 22:48:01 2016

@author: 冥凝
"""

import math
import matplotlib.pyplot as mp
import easygui as eg

G=6.67408*10**(-11) # m**3/(kg*s**2)

class earth(object):
    def __init__(self,r,m):
        self.r=r
        self.m=m
    def F(self,m,r):
        F=G*self.m*m/r**2
        return F
        
class cannonball(object):
    def __init__(self,m,v,theta,r): # theta为弧度制，r是加上了地球半径的
        self.m=m
        self.v=[v*math.sin(theta),v*math.cos(theta),v] # Vr,Vtheta,|v|,theta
        self.line_r=[r] # 列表中的r值是到地心的距离
        self.line_theta=[0]
        self.line_d=[0]
        print('m=',self.m,'kg\n',
              '|v|0=',v,'m/s\n',
              'firing angle=',(theta/math.pi),'pi\n',
              'beginning altitude=',r-s3.r,'m\n', # 这里输出的值是以地面为基准的海拔
              'v0=',self.v,'\n')
    def set_v0(self):
        if self.v[0]>0:
            self.v[0]=((self.v[2]**2-self.v[1]**2)**0.5).real
        else:
            self.v[0]=-((self.v[2]**2-self.v[1]**2)**0.5).real
        #print('v0',self.v)
    def set_v1(self):
        self.v[1]=((self.v[2]**2-self.v[0]**2)**0.5).real
    def set_V(self):
        #print(self.v)
        self.v[2]=((self.v[0]**2+self.v[1]**2)**0.5).real
        #print(self.v)
         
class air(object):
    def __init__(self,rho0,T0,B):
        self.rho0=rho0
        self.T0=T0
        self.B=B
        self.a=6.5*10**(-3) # K/m
        self.alpha=2.5
    def rho(self,r):
        rho=self.rho0*((1-(self.a*r/self.T0))**self.alpha).real
        return rho
    def f(self,r,v):
        f=(self.rho(r)/self.rho0)*self.B*v**2
        return f
        
def run():   
    i=0   
    while o.line_r[i]>=s3.r and o.line_theta[i]<3*math.pi and o.line_r[i]<=3*s3.r:
        o.line_r.append(o.line_r[i]+o.v[0]*dt)
        o.line_theta.append(o.line_theta[i]+(o.v[1]*dt/((o.line_r[i]+o.line_r[(i+1)])/2))/math.pi)
        if o.v[0]>0:
            o.v[0]=o.v[0]-s3.F(o.m,o.line_r[i])*dt/o.m-a.f(r(o.line_r[i],s3.r),o.v[0])*dt/o.m 
        elif o.v[0]<0:
            o.v[0]=o.v[0]-s3.F(o.m,o.line_r[i])*dt/o.m+a.f(r(o.line_r[i],s3.r),o.v[0])*dt/o.m
        else:
            o.v[0]=o.v[0]-s3.F(o.m,o.line_r[i])*dt/o.m
        o.v[1]=o.v[1]-a.f(r(o.line_r[i],s3.r),o.v[1])*dt/o.m
        o.line_d.append(o.line_theta[(i+1)]*s3.r)
        o.set_V()
        o.v[1]=o.v[1]*0.5*(o.line_r[i]+o.line_r[i+1])/o.line_r[i+1] # 角动量守恒
        o.set_v0()
        t.append(i*dt)
        i=i+1
        #print(o.v,o.line_r[i],o.line_theta[i])
    print('v_end=',o.v,'\n',
          'r_end=',o.line_r[i],'m\n',
          'theta_end=',o.line_theta[i],'pi\n',
          'd_end=',o.line_d[i],'m') #输出炮弹的末状态   
        
def r(rr,r0):
    r=rr-r0
    return r
    
dt=0.001
t=[0]
    
s3=earth(6371000,5.965*10**24)
o=cannonball(float(eg.enterbox("input the cannonball's mass (kg)")),
             float(eg.enterbox("input the cannonball's speed (m/s)")),
             math.pi*float(eg.enterbox("input the firing angle (write in a multiple of pi)")),
             s3.r+float(eg.enterbox("input the beginning altitude (m)")))
a=air(1.1691,298.15,0.00001) # 0℃，1atm时密度为1.29kg/m**3

run()

for i in range(len(o.line_r)):
    o.line_r[i]=o.line_r[i]-s3.r # 把列表值换成到地表的距离   
mp.plot(o.line_theta,o.line_r)
mp.ylim(0,)
mp.show()
mp.plot(o.line_d,o.line_r)
mp.ylim(0,)
mp.show()
mp.plot(t,o.line_r)
mp.ylim(0,)
mp.show()