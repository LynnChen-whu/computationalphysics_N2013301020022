#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
模拟勒夏特列原理的尝试
Created on Sat Mar 12 23:46:57 2016
@author: 冥凝
"""


'''import pygame
pygame.init()
screen = pygame.display.set_mode([640, 480])
'''


import matplotlib.pyplot as mp
import math

LF=[
"``'-'``             solid line style",
"``'--'``            dashed line style",
"``'-.'``            dash-dot line style",
"``':'``             dotted line style",
"``'.'``             point marker",
"``','``             pixel marker",
"``'o'``             circle marker",
"``'v'``             triangle_down marker",
"``'^'``             triangle_up marker",
"``'<'``             triangle_left marker",
"``'>'``             triangle_right marker",
"``'1'``             tri_down marker",
"``'2'``             tri_up marker",
"``'3'``             tri_left marker",
"``'4'``             tri_right marker",
"``'s'``             square marker",
"``'p'``             pentagon marker",
"``'*'``             star marker",
"``'h'``             hexagon1 marker",
"``'H'``             hexagon2 marker",
"``'+'``             plus marker",
"``'x'``             x marker",
"``'D'``             diamond marker",
"``'d'``             thin_diamond marker",
"``'|'``             vline marker",
"``'_'``             hline marker"
]

LC=[
"'b'         blue",
"'g'         green",
"'r'         red",
"'c'         cyan",
"'m'         magenta",
"'y'         yellow",
"'k'         black",
"'w'         white"
]

while(1):
    NA0=int(input('输入初始A原子数：'))
    half_TA=float(input('输入A半衰期：'))
    nA=float(input('输入单位A衰变成的B的单位数：'))
    NB0=int(input('输入初始B原子数：'))
    half_TB=float(input('输入B半衰期：'))
    nB=float(input('输入单位B衰变成的A的单位数：'))
    step=float(input('输入步长（计算精度）：'))
    TIME=float(input('输入总历时：'))
    fine=int(input('输入输出精度（x，每x步输出一次)：'))
    print('\n')
    print('以下是部分可选的绘图颜色：')
    for i in range(len(LC)):
        print(LC[i])
    print('以下是可选的绘图线型：')
    for i in range(4):
        print(LF[i])
    print('以下是可选的数据点标注：')
    for i in range(4,(len(LF))):
        print(LF[i])
    print('以下的“绘图线格式”的格式是“（颜色标识符）线型标识符（标注标识符）”。\n高计算精度时使用标注标识符会使线变得很粗。')
    lineformA=str(input('输入绘图线格式A：'))
    lineformB=str(input('输入绘图线格式B：'))
    width=float(input('输入线宽：'))
    print('\n')
    
    NA=[NA0]
    NB=[NB0]
    T=[0]

    for i in range(1,int(TIME/step+1)):
        T.append(i*step)
        TEMPA=(NA[(i-1)]+NA[(i-1)]*(math.log(0.5)/half_TA*step))
        TEMPB=(NB[(i-1)]+NB[(i-1)]*(math.log(0.5)/half_TB*step))
        NA.append((TEMPA+nB*(NB[i-1]-TEMPB)))
        NB.append((TEMPB+nA*(NA[i-1]-TEMPA)))
    
    for i in range(int(TIME/step+1)):
        if(i%fine==0):
            print(T[i],NA[i],NB[i])
    
    mp.plot(T,NA,lineformA,linewidth=width,label='A')
    mp.plot(T,NB,lineformB,linewidth=width,label='B')
    mp.xlabel('T')
    mp.ylabel('N')
    mp.title('N-T')
    mp.ylim(0,)
    mp.legend()
    mp.show()

