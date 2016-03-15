# -*- coding: utf-8 -*-
"""
Python3程序，用于将输入的字母串变换成由‘#’号组成的字符画。
"""


letter_code={
             'A':[['  ##    '],
                  [' #  #   '],
                  ['#    #  '],
                  ['######  '],
                  ['#    #  '],
                  ['#    #  ']],
             'B':[['####    '],
                  ['#   #   '],
                  ['####    '],
                  ['#   #   '],
                  ['#    #  '],
                  ['#####   ']],
             'C':[['  ####  '],
                  [' #      '],
                  ['#       '],
                  ['#       '],
                  [' #      '],
                  ['  ####  ']],
             'E':[['######  '],
                  ['#       '],
                  ['#####   '],
                  ['#       '],
                  ['#       '],
                  ['######  ']],
             'H':[['#    #  '],
                  ['#    #  '],
                  ['######  '],
                  ['#    #  '],
                  ['#    #  '],
                  ['#    #  ']],
             'I':[[' ###    '],
                  ['  #     '],
                  ['  #     '],
                  ['  #     '],
                  ['  #     '],
                  [' ###    ']],
             'L':[['#       '],
                  ['#       '],
                  ['#       '],
                  ['#       '],
                  ['#       '],
                  ['######  ']],
             'N':[['#    #  '],
                  ['##   #  '],
                  ['# #  #  '],
                  ['#  # #  '],
                  ['#   ##  '],
                  ['#    #  ']],
             'Y':[['#    #  '],
                  ['#   #   '],
                  [' # #    '],
                  ['  #     '],
                  ['  #     '],
                  ['  #     ']]
            } 
  
  

def amplifier(st):
    m=st
    i=0
    t=[]
    b=[]
    print('\n')
    while(i<6): 
        t[:]=[]
        n=len(m)
        while(n>0):
            t=t+letter_code[m[(len(m)-n)]][i]
            n=n-1
        i=i+1
        n=len(m)-1
        b[:]=t[:]
        while(n>0):
            b[(len(m)-n)]=b[(len(m)-n-1)]+t[(len(m)-n)]
            n=n-1
        print(b[(len(m)-1)])
        

def amp_s(nst,s):   #每行字母个数为s（临时变量）
    l=len(nst)
    m=l//s
    n=l%s
    i=0
    while(i<m):
        amplifier(nst[(i*s):((i+1)*s)])
        i=i+1
    if(n>0):
        amplifier(nst[(i*s):])
        
 
def amp(nst):   #每行字母个数为sl（全局变量）
    l=len(nst)
    m=l//sl
    n=l%sl
    i=0
    while(i<m):
        amplifier(nst[(i*sl):((i+1)*sl)])
        i=i+1
    if(n>0):
        amplifier(nst[(i*sl):]) 
 


amp_s('CHENLIN',4)
        
sl=8
amp('LYNNCHEN')    






