# -*- coding: utf-8 -*-
"""
球体的互影響
Created on Wed May 11 09:46:29 2016

@author: 冥凝
"""

import math
import matplotlib.pyplot as mp
import easygui as eg
from mpl_toolkits.mplot3d import Axes3D as axes3d
import numpy as np

class ball(object):
    def __init__(self,m=5.965*10**24,r=6371000,p=[],v=[]):
        self.m=m
        self.r=r
        self.p=[p]
        self.v=v
        self.t=[0]
    def F(self,mass,p=[],flag=-1):
        d=0
        for i in range(3):
            d=d+(self.p[flag][i]-p[i])**2
        d=d**0.5
        F=[0,0,0]
        f=G*self.m*mass/d**2
        for i in range(3):
            F[i]=f*(self.p[flag][i]-p[i])/d
        return F
    def move(self,*fs): #所有传入的力必须全为长为3的列表 
        p_temp=[0,0,0]
        F=[0,0,0]
        a=[0,0,0]
        for i in range(3):
            p_temp[i]=self.v[i]*dt+self.p[-1][i]
        self.p.append(p_temp)
        self.t.append(self.t[-1]+dt)
        for f in fs:
            for i in range(3):
                F[i]=F[i]+f[i]
        for i in range(3):
            a[i]=F[i]/self.m
        for i in range(3):
            self.v[i]=self.v[i]+a[i]*dt
            
def light_minute(n):
    answer=n*299792458*60
    return answer
    
def earth_velocity(n):
    answer=n*30000
    return answer
    
def year(n):
    answer=int(n*365.25*24*60*60/dt)
    return answer
               
G=6.67408*10**(-11) # m**3/(kg*s**2)          
dt=0.001

a=ball(m=5.965*10**25,p=[-light_minute(0.00001),0,0],v=[earth_velocity(3)*0.5,-earth_velocity(3)*math.cos(math.pi/6),300])
b=ball(m=5.965*10**25,p=[light_minute(0.00001),0,0],v=[earth_velocity(3)*0.5,earth_velocity(3)*math.cos(math.pi/6),-600])
c=ball(m=5.965*10**25,p=[0,light_minute(0.00001)*math.cos(math.pi/6),0],v=[-earth_velocity(3),0,900])

def run():
    a.move(b.F(mass=a.m,p=a.p[-1],flag=-1),c.F(mass=a.m,p=a.p[-1],flag=-1))
    b.move(a.F(mass=b.m,p=b.p[-1],flag=-2),c.F(mass=b.m,p=b.p[-1],flag=-1))
    c.move(a.F(mass=c.m,p=c.p[-1],flag=-2),b.F(mass=c.m,p=c.p[-1],flag=-2))    
    #print(a.p[-1],b.p[-1])

def write(*ps): # 传入的数组必须全为以长度为3的列表构成的列表
    X=[[ps[0][0][0]]]
    Y=[[ps[0][0][1]]]
    Z=[[ps[0][0][2]]]
    fig=mp.figure()
    ax=axes3d(fig)
    for i in range(1,len(ps[0])):
        X[0].append(ps[0][i][0])
        Y[0].append(ps[0][i][1])
        Z[0].append(ps[0][i][2]) 
    for i in range(1,len(ps)):
        X.append([ps[i][0][0]])
        Y.append([ps[i][0][1]])
        Z.append([ps[i][0][2]])
        for j in range(1,len(ps[i])):
            X[i].append(ps[i][j][0])
            Y[i].append(ps[i][j][1])
            Z[i].append(ps[i][j][2])
    for i in range(len(X)):    
        ax.scatter(X[i],Y[i],Z[i],s=1,c=np.arctan(X[i]),alpha=0.1) 
    #ax.set_xlabel('baseline/m') #X轴标题
    #ax.set_xticks([i for i in range(-7,8)]) #X轴刻度
    #ax.set_ylabel('sideline/m')
    #ax.set_yticks([i for i in range(-15,16)])
    #ax.set_zticks([i for i in range(-1,6)])
    #mp.plot(X1,Y1,'b-.',linewidth=2,label='P=0mW')
    #mp.plot(X2,Y2,'g:',linewidth=2,label='P=0mW')
    mp.show()

    
def main():
    for i in range(10000):
        run()
    write(a.p,b.p,c.p)
    #write(b.p)
    #mp.show()
    
main()
            
        
