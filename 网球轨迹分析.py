#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
网球轨迹分析
Created on Sat Apr 30 00:09:00 2016

@author: 冥凝
"""

import math
import matplotlib.pyplot as mp
import easygui as eg
from mpl_toolkits.mplot3d import Axes3D

'''定义的所有函数形参形式为'x=[]'时要求x是一个长度为3的实数列表'''

def cross_product(a=[],b=[]): #叉乘
    c=[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
    return c
    
class court(object):
    def __init__(self,length=23.77,width=8.23,net=0.92,serviceline=6.4):
        self.length=length
        self.width=width
        self.serviceline=serviceline
        self.net=net
    '''每一分球从y的负半轴开始'''
    def refree(self,hit_times,p=[]):
        if p[2]**2<0.001:
            if hit_times%2==1:
                if -0.5*self.width<=p[0]<=0.5*self.width and 0<=p[1]<=0.5*self.length:
                    answer='in'
                else:
                    answer='out'
            elif hit_times%2==0:
                if -0.5*self.width<=p[0]<=0.5*self.width and -0.5*self.length<=p[1]<=0:
                    answer='in'
                else:
                    answer='out'
        else:
            answer='false'
        return answer
    def service_refree(self,serve_area,p=[]):
        if p[2]**2<0.001:
            if serve_area==1:
                if -0.5*self.width<=p[0]<=0 and 0<=p[1]<=0.5*self.serviceline:
                    answer='in'
                else:
                    answer='out'
            elif serve_area==2:
                if 0<=p[0]<=0.5*self.width and 0<=p[1]<=0.5*self.serviceline:
                    answer='in'
                else:
                    answer='out'
        else:
            answer='false'
        return answer
    def net_refree(self,p=[]):
        if p[1]**2<0.0009:
            if p[2]<self.net:
                answer='fault'
            else:
                answer='success'
        else:
            answer='false'
        return answer
    
class tennis_ball(object):
    def __init__(self,v=[0,0,0],p=[0,-0.5*23.77,0.92],spin=[0,0,0],mass=0.057,radius=0.0335,dt=0.01): # 输入转速的单位是转每秒
        self.mass=mass
        self.radius=radius
        self.v=v
        self.p=[p]
        self.spin=[0,0,0]
        for i in range(3):
            self.spin[i]=2*math.pi*spin[i] # 使用转速的单位是
        self.dt=dt
        self.t=[0]
    def move(self,*fs): #所有传入的力必须全为长为3的列表 
        p_temp=[0,0,0]
        F=[0,0,0]
        a=[0,0,0]
        for i in range(3):
            p_temp[i]=self.v[i]*self.dt+self.p[-1][i]
        self.p.append(p_temp)
        self.t.append(self.t[-1]+self.dt)
        for f in fs:
            for i in range(3):
                F[i]=F[i]+f[i]
        for i in range(3):
            a[i]=F[i]/self.mass
        for i in range(3):
            self.v[i]=self.v[i]+a[i]*self.dt
            
class air(object):
    def __init__(self,rho0=1.1691,Temperature0=298.15,B=0.0001,S=6.109*10**(-5)):
        self.rho0=rho0
        self.Temperature=Temperature0
        self.B=B
        self.a=6.5*10**(-3) # K/m
        self.alpha=2.5
        self.S=S
    def rho(self,z):
        rho=self.rho0*((1-(self.a*z/self.Temperature))**self.alpha).real
        return rho
    def f_drag(self,z,v=[]):
        f=[0,0,0]
        for i in range(3):
            if v[i]!=0:
                f[i]=-(self.rho(z)/self.rho0)*self.B*v[i]**2*v[i]/abs(v[i])
            else:
                f[i]=0
        return f
    def f_bernoulli(self,z,v=[],spin=[]):
        f=cross_product(spin,v)
        for i in range(3):
            f[i]=self.S*f[i]
        return f
             
G=6.67408*10**(-11) # m**3/(kg*s**2)
class earth(object):
    def __init__(self,radius=6371000,mass=5.965*10**24):
        self.radius=radius
        self.mass=mass
    def F(self,mass,z):
        F=[0,0,0]
        F[2]=-G*self.mass*mass/(self.radius+z)**2
        return F

'''对象'''
single_court=court()     
a=tennis_ball(v=[float(eg.enterbox("input the Vx (m/s)")),
                 float(eg.enterbox("input the Vy (m/s)")),
                 float(eg.enterbox("input the Vz (m/s)"))],
              p=[float(eg.enterbox("input the position_x (m)")),
                 -0.5*single_court.length+float(eg.enterbox("input the position_y (set the baseline is zero) (m)")),
                 float(eg.enterbox("input the position_z (m)"))],
              spin=[float(eg.enterbox("input the ωx (r/s)")),
                    float(eg.enterbox("input the ωy (r/s)")),
                    float(eg.enterbox("input the ωz (r/s)"))])
s3=earth()
atmosphere=air()

def baseline_ball():
    while single_court.refree(hit_times=1,p=a.p[-1])=='false' and single_court.net_refree(a.p[-1])!='fault' and a.p[-1][2]>=0:
        a.move(s3.F(mass=a.mass,z=a.p[-1][2]),atmosphere.f_drag(z=a.p[-1][2],v=a.v),atmosphere.f_bernoulli(z=a.p[-1][2],v=a.v,spin=a.spin))
    if single_court.net_refree(a.p[-1])=='fault':
        print('fault')
    if single_court.refree(hit_times=1,p=a.p[-1])!='false':
        print(single_court.refree(hit_times=1,p=a.p[-1]))
    elif single_court.refree(hit_times=1,p=a.p[-1])=='false' and a.p[-1][2]<0:
        print('false')

def write(p=[]):
    X=[p[0][0]]
    Y=[p[0][1]]
    Z=[p[0][2]]
    fig=mp.figure()
    ax=Axes3D(fig)
    for i in range(1,len(p)):
        X.append(p[i][0])
        Y.append(p[i][1])
        Z.append(p[i][2])      
    ax.scatter(X,Y,Z)
    
        
baseline_ball()
write(a.p)
mp.show()    
    
    