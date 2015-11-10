# -*- coding: utf-8 -*-
from random import randint
import sys
import time
import threading
import curses
from pantalla import pantalla

class vista(object):

    def __init__(self):
	self.stdscr = curses.initscr() # inicializar la pantall
	curses.noecho() # evitar que lo que escrives salga
	curses.cbreak() # detectar pulsaciones de teclas sin intro
	self.stdscr.keypad(1) # permitir usar las flechas y otras teclas especiales del teclado
	curses.start_color()
	if curses.can_change_color()==True:
	   curses.init_color(10,800,800,800) # blanco
	   curses.init_color(11,0,0,0) # negro
	   curses.init_color(12,500,0,0) # Rojo
	   curses.init_color(13,200,200,200) # gris oscuro
	   curses.init_pair(1, 10, 11) # objetos
	   curses.init_pair(2, 11, 11) # suelo
	   curses.init_pair(3, 10, 13) # paredes
	   curses.init_pair(4, 12, 11) # player
	   curses.init_pair(5, 13, 11) # paredes ocultas
	else:
	   curses.nocbreak(); self.stdscr.keypad(0); curses.echo()
	   curses.endwin()
	   print 'Busca otra terminal que tenga más colores'
	   exit()

    def pintar(self,p):
	    for x in range(0,p.t):
	     for y in range(0,p.t):
	         c = curses.color_pair(1)
	         if p.mundo[x][y][0] == '1':
	           c = curses.color_pair(2)
	         if p.mundo[x][y][0] == '#':
	           c = curses.color_pair(3)
	         if p.mundo[x][y][0] == '@':
	           c = curses.color_pair(4)
	         self.stdscr.addch(x,y*2,p.mundo[x][y][0],c)
	         self.stdscr.addch(x,y*2+1,' ',c)
	    self.stdscr.refresh()

    def acabar(self):
	curses.nocbreak(); self.stdscr.keypad(0); curses.echo()
	curses.endwin()
	print curses.COLORS
	print curses.can_change_color()
	print curses.COLOR_PAIRS
