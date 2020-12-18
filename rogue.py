# -*- coding: utf-8 -*-
from random import randint
import sys
import time
import threading   
import curses
from pantalla import pantalla
from vista import vista
#print 'Empezamios'

p = pantalla(49,30)
v = vista()

while 1:
    v.pintar(p)
    c = v.stdscr.getch()
    if c == ord('w'):
     if p.mundo[p.pos_heroe[0]-1][p.pos_heroe[1]][0]=='1':
       p.mundo[p.pos_heroe[0]][p.pos_heroe[1]]=['1',-1]
       p.mundo[p.pos_heroe[0]-1][p.pos_heroe[1]]=['@',100]
       p.pos_heroe[0]=p.pos_heroe[0]-1
    elif c == ord('a'):
     if p.mundo[p.pos_heroe[0]][p.pos_heroe[1]-1][0]=='1':
       p.mundo[p.pos_heroe[0]][p.pos_heroe[1]]=['1',-1]
       p.mundo[p.pos_heroe[0]][p.pos_heroe[1]-1]=['@',100]
       p.pos_heroe[1]=p.pos_heroe[1]-1
    elif c == ord('s'):
     if p.mundo[p.pos_heroe[0]+1][p.pos_heroe[1]][0]=='1':
       p.mundo[p.pos_heroe[0]][p.pos_heroe[1]]=['1',-1]
       p.mundo[p.pos_heroe[0]+1][p.pos_heroe[1]]=['@',100]
       p.pos_heroe[0]=p.pos_heroe[0]+1
    elif c == ord('d'):
     if p.mundo[p.pos_heroe[0]][p.pos_heroe[1]+1][0]=='1':
       p.mundo[p.pos_heroe[0]][p.pos_heroe[1]]=['1',-1]
       p.mundo[p.pos_heroe[0]][p.pos_heroe[1]+1]=['@',100]
       p.pos_heroe[1]=p.pos_heroe[1]+1
    elif c == ord('q'):
	break  # Exit the while()
    elif c == curses.KEY_HOME:
	x = y = 0

v.acabar()
