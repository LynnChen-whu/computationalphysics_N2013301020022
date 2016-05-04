#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 22:48:01 2016

@author: 冥凝
"""

import math
import matplotlib.pyplot as mp
import easygui as eg
import numpy as np

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
              'v0=',self.v,'')
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
        
def run(target):   
    i=0   
    while o.line_r[i]<=(s3.r+target) and o.line_theta[i]<3*math.pi and o.line_r[i]<=3*s3.r:
        o.line_r.append(o.line_r[i]+o.v[0]*dt)
        o.line_theta.append(o.line_theta[i]+(o.v[1]*dt/((o.line_r[i]+o.line_r[(i+1)])/2))/math.pi)
        if o.v[0]>0:
            o.v[0]=o.v[0]-s3.F(o.m,o.line_r[i])*dt/o.m-a.f(r(o.line_r[i],s3.r),o.v[0])*dt/o.m 
        elif o.v[0]<0:
            o.v[0]=o.v[0]-s3.F(o.m,o.line_r[i])*dt/o.m+a.f(r(o.line_r[i],s3.r),o.v[0])*dt/o.m
        else:
            o.v[0]=o.v[0]-s3.F(o.m,o.line_r[i])*dt/o.m
        o.v[1]=o.v[1]-a.f(r(o.line_r[i],s3.r),o.v[1])*dt/o.m
        o.line_d.append(o.line_theta[(i+1)]*s3.r*math.pi)
        o.set_V()
        o.v[1]=o.v[1]*0.5*(o.line_r[i]+o.line_r[i+1])/o.line_r[i+1] # 角动量守恒
        o.set_v0()
        t.append(i*dt)
        i=i+1
    while o.line_r[i]>(s3.r+target) and o.line_theta[i]<3*math.pi and o.line_r[i]<=3*s3.r:
        o.line_r.append(o.line_r[i]+o.v[0]*dt)
        o.line_theta.append(o.line_theta[i]+(o.v[1]*dt/((o.line_r[i]+o.line_r[(i+1)])/2))/math.pi)
        if o.v[0]>0:
            o.v[0]=o.v[0]-s3.F(o.m,o.line_r[i])*dt/o.m-a.f(r(o.line_r[i],s3.r),o.v[0])*dt/o.m 
        elif o.v[0]<0:
            o.v[0]=o.v[0]-s3.F(o.m,o.line_r[i])*dt/o.m+a.f(r(o.line_r[i],s3.r),o.v[0])*dt/o.m
        else:
            o.v[0]=o.v[0]-s3.F(o.m,o.line_r[i])*dt/o.m
        o.v[1]=o.v[1]-a.f(r(o.line_r[i],s3.r),o.v[1])*dt/o.m
        o.line_d.append(o.line_theta[(i+1)]*s3.r*math.pi)
        o.set_V()
        o.v[1]=o.v[1]*0.5*(o.line_r[i]+o.line_r[i+1])/o.line_r[i+1] # 角动量守恒
        o.set_v0()
        t.append(i*dt)
        i=i+1
        #print(o.v,o.line_r[i],o.line_theta[i])
    print('v_end=',o.v,'\n',
          'r_end=',o.line_r[i],'m\n',
          'theta_end=',o.line_theta[i],'pi\n',
          'd_end=',o.line_d[i],'m\n') #输出炮弹的末状态   
          
def compare_d(now,need):
    δ=need/100000
    if δ>2:
        δ=3
    elif δ<0.25:
        δ=0.25
    if (now-need)**2>δ:
        if now>need:
            answer=1
        else:
            if (need<=10*now):
                answer=-1
            elif (10*now<need<=100*now):
                answer=-2
            else:
                answer=-3
    else:
        answer=0
    return answer

def compare_r(now,need):
    if now-need>0:
        answer=1
    else:
        answer=0
    return answer
  
def adjust(now,drag_d,drag_r):
    global v_temp
    global v_high
    global v_low
    global theta_temp
    if drag_d>0:
        if drag_r==0:
            v_high=v_temp
            o.__init__(m,(now-v_low)*0.618+v_low,theta_temp,s3.r+beginning_altitude)
            v_temp=o.v[2]
        else:
            v_high=v_temp
            o.__init__(m,now*0.618,theta_temp,s3.r+beginning_altitude)
            v_temp=o.v[2]
    elif drag_d<0:
        if drag_r==0:
            v_low=v_temp
            if v_low>=v_high:
                theta_temp=theta_temp*0.618
                o.__init__(m,now/0.618/10**(drag_d+1),theta_temp,s3.r+beginning_altitude)
            else:
                o.__init__(m,(v_high-now)*0.618+now,theta_temp,s3.r+beginning_altitude)
            v_temp=o.v[2]
        else:
            v_high=v_temp
            theta_temp=theta_temp*0.618
            o.__init__(m,now*0.5,theta_temp,s3.r+beginning_altitude)
            v_temp=o.v[2]
               
def r(rr,r0):
    r=rr-r0
    return r

'''variable'''
G=6.67408*10**(-11) # m**3/(kg*s**2)
v_temp=0   
v_high=0
v_low=0     
theta_temp=math.pi*0.25
dt=0.002
t=[0]

beginning_altitude=float(eg.enterbox("input the beginning altitude (m)"))
m=float(eg.enterbox("input the mass (kg)"))

'''object'''    
s3=earth(6371000,5.965*10**24)

a=air(1.1691,298.15,0.0001) # 0℃，1atm时密度为1.29kg/m**3
target=[float(eg.enterbox("input the range (m)")),float(eg.enterbox("input the end altitude (m)"))]
o=cannonball(m,(9.8*target[0])**0.5,theta_temp,s3.r+beginning_altitude)

'''main'''
v_temp=o.v[2]
run(target[1])
while compare_d(o.line_d[-1],target[0])!=0 or compare_r(o.line_r[-1],(target[1]+s3.r))!=0:      
    adjust(v_temp,compare_d(o.line_d[-1],target[0]),compare_r(o.line_r[-1],(target[1]+s3.r)))
    t=[0]
    run(target[1])

'''show'''
'''以下对炮弹的位置数组作变换整理'''
o_Y=[o.line_r[0]*math.sin(o.line_theta[0]*math.pi)]
o_Z=[o.line_r[0]*math.cos(o.line_theta[0]*math.pi)]
o.line_r[0]=o.line_r[0]-s3.r
for i in range(1,len(o.line_r)):
    o_Y.append(o.line_r[i]*math.sin(o.line_theta[i]))
    o_Z.append(o.line_r[i]*math.cos(o.line_theta[i]))
    o.line_r[i]=o.line_r[i]-s3.r # 把列表值换成到地表的距离  
         
'''以下制作一个地球的表面数组'''
phi=[theta*math.pi for theta in o.line_theta]
s3_x=[math.sin(i)*s3.r for i in phi]
s3_y=[math.cos(i)*s3.r for i in phi]

mp.plot(s3_x,s3_y)
mp.plot(o_Y,o_Z)
mp.ylabel('r/m')
mp.show()    
mp.plot(o.line_d,o.line_r)
mp.title('r-R——d')
mp.xlabel('d/m')
mp.ylabel('r/m')
mp.ylim(0,)
mp.show()
mp.plot(t,o.line_r)
mp.title('r-R——t')
mp.xlabel('d/m')
mp.ylabel('t/s')
mp.ylim(0,)
mp.show()