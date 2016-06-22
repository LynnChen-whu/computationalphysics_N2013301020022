# -*- coding: utf-8 -*-
"""
蟲口模型
Created on Wed Jun 22 10:03:49 2016

@author: 冥凝
"""

import math
import matplotlib.pyplot as mp
import easygui as eg
from mpl_toolkits.mplot3d import Axes3D as axes3d
import numpy as np
from matplotlib import animation

class system(object):
    def __init__(self,x0,miu):        
        self.t=[0]
        self.x=[x0]
        self.miu=miu
    def run(self,steps=1):
        for i in range(steps):
            self.t.append(self.t[-1]+1)
            self.x.append(self.x[-1]*self.miu*(1-self.x[-1]))
    def gett(self):
        return self.t
    def getx(self):
        return self.x

sys1=system(0.3,3.8)
sys2=system(0.6,3.8)
sys3=system(0.9,3.8)

fig=mp.figure()
ax=fig.add_subplot(1,1,1,xlim=(0, 100), ylim=(0, 1))
#ax.set_xticks([i for i in range(-7,8)]) #X轴刻度
line1,=ax.plot([],[])
line2,=ax.plot([],[])
line3,=ax.plot([],[])

def init(): 
    line1.set_data(sys1.t,sys1.x)#,[],lw=2,c='r')
    line2.set_data(sys2.t,sys2.x)
    line3.set_data(sys3.t,sys3.x)
    #line3,=ax.plot([],[],[],lw=2,c='g')
    return line1,line2,line3
    
def animate(i):
    sys1.run()  
    sys2.run()
    sys3.run()
    '''TEMP=write(a.p,b.p,c.p)
    X,Y,Z=[],[],[]
    for i in range(3):
        X.append(TEMP[0][i])
        Y.append(TEMP[1][i])
        Z.append(TEMP[2][i])'''
    #print(sys.gett())
    line1.set_data(sys1.t,sys1.x)#,[],lw=2,c='r')
    line2.set_data(sys2.t,sys2.x)
    line3.set_data(sys3.t,sys3.x)
    #line3,=ax.plot(X[2],Y[2],Z[2],lw=2,c='g')
    return line1,line2,line3

anim1=animation.FuncAnimation(fig,animate,init_func=init,interval=100,blit=True) 
mp.show()   