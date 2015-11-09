# -*- coding: utf-8 -*-
from random import randint
import sys
import time
import threading
import curses

class pantalla(object):
 
 celdas = []
 direcciones = [(1,0),(-1,0),(0,1),(0,-1)]
 d_actual = 0
 puerta = []
 puntas = []
 m = 0

 def __init__(self,t,salas):
  self.t = t
  self.mundo = [[['#',0] for x in range(t)] for x in range(t)]
  exitos = 0
  self.m = salas
  for s in range(2,salas+2):
   cabe = 0
   intentos = 0
   while cabe == 0 and intentos < 1000: 
    intentos = intentos + 1
    chocan = 0
    ax = randint(1,4)*2+1
    x = randint(1,t-ax-1)
    if x%2 == 0:
     x=x-1
    ay = randint(1,4)*2+1
    y = randint(1,t-ay-1)
    if y%2 == 0:
     y=y-1
    for i in range(x-1,x+ax+1):
     for j in range(y-1,y+ay+1):
      if self.mundo[i][j][0] != '#':
       chocan = 1
    if chocan == 0:
     cabe = 1
   #  print intentos,
     exitos = exitos + 1
     for i in range(x,x+ax):
      for j in range(y,y+ay):
       self.mundo[i][j]=['.',s]
  #print exitos
 def start_maze(self):
     for i in range(1,self.t-1,2): # las y
      for j in range(1,self.t-1,2): # las x
          #self.mundo[i][j]='k'
          if self.mundo[i][j][0]=='#':
            self.actual = [i,j]
            self.m = self.m + 1
            return 0
     self.actual = 'fin'
 
 def grow_maze(self):
     x = self.actual[0]
     y = self.actual[1]
     self.mundo[x][y]=['1',self.m]
     self.celdas.append(self.actual)
     # el tema de la diección y las dirección actual
     cavado = 0 # si ya he cavado en alguna direccion
     d = self.d_actual
     if randint(0,50)<20:
         d = randint(0,4)
     for i in range(0,4):
 #        print self.direcciones[(d+i)%4]
         if x+self.direcciones[(d+i)%4][0]>0 and x+self.direcciones[(d+i)%4][0]<self.t-1 and y+self.direcciones[(d+i)%4][1]>0 and y+self.direcciones[(d+i)%4][1]< self.t-1:
          if cavado == 0 and self.mundo[x+self.direcciones[(d+i)%4][0]*2][y+self.direcciones[(d+i)%4][1]*2][0]=='#':
            self.mundo[x+self.direcciones[(d+i)%4][0]][y+self.direcciones[(d+i)%4][1]]=['1',self.m]
            self.d_actual = (d+i)%4
            self.actual = [x+self.direcciones[(d+i)%4][0]*2,y+self.direcciones[(d+i)%4][1]*2]
            cavado = 1
     #print self.celdas
     if cavado == 0:
      self.celdas.pop()
      if len(self.celdas) > 0:

          self.actual = self.celdas.pop()
      else:
          self.start_maze()
#          print 'start'
     #print '                 '
     #print str(self.actual)+" "+str(len(self.celdas))+"                      "

 def print_pantalla(self):
  for i in self.mundo:
   for j in i:
    if j[0] == '1':
     sys.stdout.write(chr(27)+"["+str(30+(j[1]%8))+"m")
    if j[0] == '.':
     sys.stdout.write(chr(27)+"["+str(j[1])+"m")
    sys.stdout.write(j[0]+' ')
    sys.stdout.write(chr(27)+"[0m")
   print ' '

 def print_pantalla_final(self,scr):
  for x in range(0,self.t):
   for y in range(0,self.t):
    c = curses.color_pair(1)
    #curses.init_pair(3+y, curses.COLOR_WHITE, y+35)
    #d = curses.color_pair(3+y)
    if self.mundo[x][y][0] == '1':
      c = curses.color_pair(2)
    if self.mundo[x][y][0] == '#':
      c = curses.color_pair(3)
    if self.mundo[x][y][0] == '@':
      c = curses.color_pair(4)
    scr.addch(x,y*2,self.mundo[x][y][0],c)
    scr.addch(x,y*2+1,' ',c)
    
 def print_pantalla_debug(self):
  for i in self.mundo:
   for j in i:
    if j[0] == '1':
     sys.stdout.write(chr(27)+"[34m")
    if j[0] == '.':
     sys.stdout.write(chr(27)+"["+str(j[1])+"m")
    sys.stdout.write(str(j[1])+' ')
    sys.stdout.write(chr(27)+"[0m")
   print ' '

 def espunta(self,i,j):
            n = 0
            if self.mundo[i-1][j][0]=='#':
               n = n+1
            if self.mundo[i+1][j][0]=='#':
               n = n+1
            if self.mundo[i][j-1][0]=='#':
               n = n+1
            if self.mundo[i][j+1][0]=='#':
               n = n+1
            return n

 
 def detectar_puntas(self):     
     for i in range(1,self.t-1,2): # las y
      for j in range(1,self.t-1,2): # las x
          if self.mundo[i][j][0]=='1':
            n = self.espunta(i,j)
            if n == 3:
               self.puntas.append([i,j])

 def borrar_punta(self,punta):
         self.mundo[punta[0]][punta[1]]=['#',0]
         i = punta[0]
         j = punta[1]
         sig = 0
         if self.mundo[i-1][j][0]=='1':
            sig = [i-1,j]
         if self.mundo[i+1][j][0]=='1':
            sig = [i+1,j] 
         if self.mundo[i][j-1][0]=='1':
            sig = [i,j-1]
         if self.mundo[i][j+1][0]=='1':
            sig = [i,j+1]
         if sig != 0:
          n = self.espunta(sig[0],sig[1])
          if n == 3:
            self.borrar_punta(sig) 
 
 def detectar_puertas(self):
     n = 0
     self.puerta = []
     for i in range(2,self.t-2,1): # las y
      for j in range(2,self.t-2,1): # las x
          #self.mundo[i][j]='k'
          if self.mundo[i][j][0]=='#':
              regiones = 0
              num = 0
              for d in self.direcciones:
                  if self.mundo[i+d[0]][j+d[1]][1] > 0: # es una region
                     if regiones == 0:
                        num = self.mundo[i+d[0]][j+d[1]][1]
                        regiones = regiones + 1
                     if regiones > 0:
                        if num != self.mundo[i+d[0]][j+d[1]][1]:
                          # self.mundo[i][j] = ['x',0]
                           self.puerta.append([i,j,num])
                           n = n +1
                           if randint(0,50)==1: # abrir puertas alternativas
                              self.mundo[i][j]=['1',num]
                        else:
                           self.mundo[i][j] = ['#',0]
     return n

 def pintar_unos(self,x,y,n):
        self.mundo[x][y]=['1',n]
        for i in range(x-1,x+2):
         for j in range(y-1,y+2):
          if self.mundo[i][j][0] != '#' and self.mundo[i][j][1] != n:
             self.pintar_unos(i,j,n)

 def resolver_puertas(self):
     primera_puerta = 0
     while self.detectar_puertas() > 0:
        p = self.puerta[randint(0,len(self.puerta)-1)]
        x = p[0]
        y = p[1]
        n = p[2]

        if primera_puerta == 0:
           primera_puerta = [x,y]

        self.pintar_unos(x,y,n) 
        #time.sleep(0.1)
        #print(chr(27)+"[s"+chr(27)+"[0;0H")
        #self.print_pantalla()
     self.pintar_unos(primera_puerta[0],primera_puerta[1],1)
 
 pos_heroe = 0

 def poner_personajes(self):
     # primero el heroe
     puesto = 0
     while puesto == 0:
       x = randint(1,self.t-1)
       y = randint(1,self.t-1)
       if self.mundo[x][y][0] == '1':
          n = self.espunta(x,y)
          if n < 2:
             puesto = 1
             self.mundo[x][y] = ['@',100,100]
             self.pos_heroe = [x,y]

 llaves = []

 def pintar_puertas(self,x,y):
     if self.mundo[x][y][0] == '1':
        self.mundo[x][y]= ['1',-1]
        if randint(0,100) == 1:
            self.mundo[x][y] = ['&',randint(0,1000)]
            self.llaves.append(self.mundo[x][y])
        else:
          if randint(0,50) == 1 and len(self.llaves)>0:
                if self.espunta(x,y)==2:
                   ll = self.llaves.pop()
                   self.mundo[x][y] = ['+',ll[1]] 
     for i in self.direcciones:
           if self.mundo[x+i[0]][y+i[1]][0] == '1' and self.mundo[x+i[0]][y+i[1]][1] != -1:
              self.pintar_puertas(x+i[0],y+i[1])
         

 def poner_puertas(self):
     # se empieza en la posicion del heroe
     self.pintar_puertas(self.pos_heroe[0],self.pos_heroe[1])

#print 'Empezamos'
p = pantalla(49,30)
#print(chr(27) + "[2J")
#print(chr(27)+"[s"+chr(27)+"[0;0H")
#p.print_pantalla()
n = 0
p.start_maze()
while p.actual != 'fin':
    n = n+1
    p.grow_maze()
#    time.sleep(0.05)
#print(chr(27)+"[s"+chr(27)+"[0;0H")
#p.print_pantalla_debug()

#time.sleep(0.5)

p.resolver_puertas()           
 
p.detectar_puntas()
while len(p.puntas)>0:
 i = p.puntas.pop()
 t = threading.Thread(target=p.borrar_punta(i))
 t.start()

#print p.puntas

p.poner_personajes() # buenos, malos, y el heroe
#p.poner_armas        # armas y otros objetos que pueden ser utiles. Entre ellos el objetivo final
p.poner_puertas()    # puertas y llaves

#print(chr(27)+"[s"+chr(27)+"[0;0H")
#p.print_pantalla_final()

# empieza el bucle del juego
# podria a usar pygame, pero quiero que sea totalmente de terminal para usar unicode y emojis 
stdscr = curses.initscr() # inicializar la pantall
curses.noecho() # evitar que lo que escrives salga
curses.cbreak() # detectar pulsaciones de teclas sin intro
stdscr.keypad(1) # permitir usar las flechas y otras teclas especiales del teclado
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
   curses.nocbreak(); stdscr.keypad(0); curses.echo()
   curses.endwin()
   print 'Busca otra terminal que tenga más colores'
   exit()
while 1:
    p.print_pantalla_final(stdscr)

    c = stdscr.getch()
    if c == ord('w'):
       p.mundo[p.pos_heroe[0]][p.pos_heroe[1]]=['1',-1]
       p.mundo[p.pos_heroe[0]-1][p.pos_heroe[1]]=['@',100]
       p.pos_heroe[0]=p.pos_heroe[0]-1
    elif c == ord('q'):
        break  # Exit the while()
    elif c == curses.KEY_HOME:
        x = y = 0
    stdscr.refresh()

curses.nocbreak(); stdscr.keypad(0); curses.echo()
curses.endwin()


print curses.COLORS
print curses.can_change_color()
print curses.COLOR_PAIRS
