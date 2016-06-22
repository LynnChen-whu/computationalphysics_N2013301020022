#!/usr/bin/python
#-*- coding: utf-8 -*_
'''
帶電粒子的庫侖力作用
by 潘俊霖 陳林
'''

import numpy as np
from numpy import *
import math
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
from mpl_toolkits.mplot3d import Axes3D as ax
from matplotlib import animation

class Particle(object):
    #单位: 质量 - g dt(时间间隔) - s  电量 - C 位置 - m 速度 - m/s 加速度 - m/s^2 邊界 m,m,m
    def __init__(self, mass, dt, electricity, position = [0, 0, 0], velocity = [0, 0, 0], acceleration = [0, 0, 0],boundry=[2.5,2.5,2.5]):
        self.__mass = mass
        self.__position = position
        self.__velocity = np.array(velocity)
        self.__electricity = electricity
        self.__acceleration = np.array(acceleration);
        self.__dt = dt
        self.__force = np.array([0, 0, 0])
        self.__boundry=np.array(boundry)
    
    def move(self):
        #print "force :",self.__force
        self.__acceleration = self.__force / self.__mass
        dx = self.__velocity * self.__dt + self.__acceleration * self.__dt * self.__dt / 2
        self.__velocity = self.__velocity + self.__acceleration * self.__dt
        #print "dx : ", dx
        #print "self.__position : ", self.__position()
        self.__position = self.__position + dx
        self.guard()
        
    def guard(self):
        for i in range(len(self.__position)):
            if ((self.__position[i])**2-(self.__boundry[i])**2)**2<=0.001:
                self.__velocity[i]=-self.__velocity[i]
        
    def setForce(self, force = np.array([0, 0, 0])):
        self.__force = force
    
    def addForce(self, force = np.array([0, 0, 0])):
        self.__force = self.__force + force
        
    def getPosition(self):
        return self.__position
    
    def getElectricity(self):
        return self.__electricity
        
        
class System(object):
    def __init__(self, times):
        self.__particles = [];
        self.__times = times
        self.__e = 1.60 * 10 ** -19
        self.__k = 9.0 * 10 ** 9
    
    def countForce(self, particle1, particle2):
        position1 = np.array(particle1.getPosition())
        position2 = np.array(particle2.getPosition())
        #print "position 1 ", position1
        #print "position 2 ", position2
        betaX = position2 - position1
        distance =  math.sqrt(betaX.dot(betaX.T))
        
        f = -self.__k * particle1.getElectricity() * self.__e * particle2.getElectricity() * self.__e / distance / distance
        #print distance
        #print betaX
        cosTheta = betaX / distance
        
        F = f * cosTheta
        return F
        
    def addParticles(self, particles):
        self.__particles.append(particles)
        
    def setForceForeachParticle(self):
        for i in range(0,len(self.__particles) - 1) :
            #print "i : ", i
            for j in range(i + 1, len(self.__particles)):
                #print "j : ", j
                force = self.countForce(self.__particles[i], self.__particles[j])
                #print force
                self.__particles[i].addForce(force);
                self.__particles[j].addForce(-force);
                
    def start(self):
        #axs = ax(plt.figure())
        a=[]
        #b包含每一個粒子的三個坐標按時間順序排列的數組
        b=[[[] for j in range(3)] for k in range(len(self.__particles))]
        for i in range(self.__times):
            self.setForceForeachParticle();
            #打印位置
            for j in range(len(self.__particles)):
                a=[k for k in self.__particles[j].getPosition()]
                for l in range(len(a)):
                    b[j][l].append(a[l])
                a.clear
                self.__particles[j].move();                
                #重置粒子的受力
                self.__particles[j].setForce();
        '''for i in range(len(self.__particles)):
            axs.plot(b[i][0], b[i][1], b[i][2])#, c = 'blue')
        plt.show()'''
        return b
             
'''動畫模塊'''
fig=plt.figure()
axs=ax(fig)            

def init():  
    line1,=axs.plot([],[],[],lw=1,c='r')
    line2,=axs.plot([],[],[],lw=1,c='b')
    line3,=axs.plot([],[],[],lw=1,c='g')
    line4,=axs.plot([],[],[],lw=1,c='y')
    line5,=axs.plot([],[],[],lw=1,c='c')
    line6,=axs.plot([],[],[],lw=1,c='k')
    line7,=axs.plot([],[],[],lw=1,c='m')
    return line1,line2,line3,line4,line5,line6,line7
    
def animate(i): 
    TEMP=system.start()
    X,Y,Z=[],[],[]
    for i in range(len(TEMP)):
        X.append(TEMP[i][0])
        Y.append(TEMP[i][1])
        Z.append(TEMP[i][2])
    line1,=axs.plot(X[0],Y[0],Z[0],lw=2,c='r')
    line2,=axs.plot(X[1],Y[1],Z[1],lw=2,c='b')
    line3,=axs.plot(X[2],Y[2],Z[2],lw=2,c='g')
    line4,=axs.plot(X[3],Y[3],Z[3],lw=2,c='y')
    line5,=axs.plot(X[4],Y[3],Z[4],lw=2,c='c')
    line6,=axs.plot(X[5],Y[3],Z[5],lw=2,c='k')
    line7,=axs.plot(X[6],Y[3],Z[6],lw=2,c='m')
    return line1,line2,line3,line4,line5,line6,line7
                   
            
interval = 0.0001
mass = 9 * 10e-31
part1 = Particle(mass, interval, 1, [1.0, 0.0, 0.0],velocity = [0, 1, 0])
part2 = Particle(mass, interval, -1, [-1.0, 0.0, 0.0],velocity = [0, -1, 0])
part3 = Particle(mass, interval, 1, [0.0, 1.0, 0.0],velocity = [-1, 0, 0])
part4 = Particle(mass, interval, -1, [0.0, -1.0, 0.0],velocity = [1, 0, 0])
part5 = Particle(mass, interval, 1, [0.0, 0.0, 1.0],velocity = [0.5, -0.5, 0])
part6 = Particle(mass, interval, -1, [0.0, 0.0, -1.0],velocity = [-0.5, 0.5, 0])
part7 = Particle(mass, interval, 1, [0.0, 0.0, 0.0],velocity = [0, 0, 0])
system = System(100)
system.addParticles(part1)
system.addParticles(part2)
system.addParticles(part3)
system.addParticles(part4)
system.addParticles(part5)
system.addParticles(part6)
system.addParticles(part7)
     
'''使用blit=Ture時只繪製最近的部分軌跡'''
anim1=animation.FuncAnimation(fig,animate,init_func=init,interval=0.1,blit=True) 
plt.show()            
            
            
            
            
            
            
            
            
            
            
            
        