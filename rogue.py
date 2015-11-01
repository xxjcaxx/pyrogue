# -*- coding: utf-8 -*-
from random import randint
import sys
import time
import threading

class pantalla(object):
 
 celdas = []
 direcciones = [(1,0),(-1,0),(0,1),(0,-1)]
 d_actual = 0
 puerta = []

 puntas = []

 def __init__(self,t,salas):
  self.t = t
  self.mundo = [['#' for x in range(t)] for x in range(t)]
  exitos = 0
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
      if self.mundo[i][j] != '#':
       chocan = 1
    if chocan == 0:
     cabe = 1
   #  print intentos,
     exitos = exitos + 1
     for i in range(x,x+ax):
      for j in range(y,y+ay):
       self.mundo[i][j]=str(s)
  #print exitos
 def start_maze(self):
     for i in range(1,self.t-1,2): # las y
      for j in range(1,self.t-1,2): # las x
          #self.mundo[i][j]='k'
          if self.mundo[i][j]=='#':
            self.actual = [i,j]
            return 0
     self.actual = 'fin'
 
 def grow_maze(self):
     x = self.actual[0]
     y = self.actual[1]
     self.mundo[x][y]='1'
     self.celdas.append(self.actual)
     # el tema de la diección y las dirección actual
     cavado = 0 # si ya he cavado en alguna direccion
     d = self.d_actual
     if randint(0,50)<20:
         d = randint(0,4)
     for i in range(0,4):
 #        print self.direcciones[(d+i)%4]
         if x+self.direcciones[(d+i)%4][0]>0 and x+self.direcciones[(d+i)%4][0]<self.t-1 and y+self.direcciones[(d+i)%4][1]>0 and y+self.direcciones[(d+i)%4][1]< self.t-1:
          if cavado == 0 and self.mundo[x+self.direcciones[(d+i)%4][0]*2][y+self.direcciones[(d+i)%4][1]*2]=='#':
            self.mundo[x+self.direcciones[(d+i)%4][0]][y+self.direcciones[(d+i)%4][1]]='1'
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
    if j == '1':
     sys.stdout.write(chr(27)+"[34m")
    sys.stdout.write(j+' ')
    sys.stdout.write(chr(27)+"[0m")
   print ' '

 def espunta(self,i,j):
            n = 0
            if self.mundo[i-1][j]=='#':
               n = n+1
            if self.mundo[i+1][j]=='#':
               n = n+1
            if self.mundo[i][j-1]=='#':
               n = n+1
            if self.mundo[i][j+1]=='#':
               n = n+1
            return n

 
 def detectar_puntas(self):     
     for i in range(1,self.t-1,2): # las y
      for j in range(1,self.t-1,2): # las x
          if self.mundo[i][j]=='1':
            n = self.espunta(i,j)
            if n == 3:
               self.puntas.append([i,j])

 def borrar_punta(self,punta):
         self.mundo[punta[0]][punta[1]]='#'
         i = punta[0]
         j = punta[1]
         sig = 0
         if self.mundo[i-1][j]=='1':
            sig = [i-1,j]
         if self.mundo[i+1][j]=='1':
            sig = [i+1,j] 
         if self.mundo[i][j-1]=='1':
            sig = [i,j-1]
         if self.mundo[i][j+1]=='1':
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
          if self.mundo[i][j]=='#' or self.mundo[i][j]=='x':
             unos = 0
             puntos = 0
             for d in self.direcciones:
                 if self.mundo[i+d[0]][j+d[1]] == '1':
                    unos = unos + 1
                 if self.mundo[i+d[0]][j+d[1]] not in  ['1','#','x']:
                    puntos = puntos + 1
             if (unos == 1 and puntos == 1) or puntos == 2 :
                 self.mundo[i][j] = 'x'
                 self.puerta.append([i,j])
                 n = n + 1 
             else: 
                 self.mundo[i][j] = '#'
     return n

 def pintar_unos(self,x,y):
        self.mundo[x][y]='1'
        for i in range(x-1,x+2):
         for j in range(y-1,y+2):
          if self.mundo[i][j] not in ['1','#','x']:
             self.pintar_unos(i,j)

 def resolver_puertas(self):
     while self.detectar_puertas() > 0:
        p = self.puerta[randint(0,len(self.puerta)-1)]
        x = p[0]
        y = p[1]
        self.pintar_unos(x,y) 
        time.sleep(0.5)
        print(chr(27)+"[s"+chr(27)+"[0;0H")
        self.print_pantalla()

print 'Empezamos'
p = pantalla(51,50)
print(chr(27) + "[2J")
print(chr(27)+"[s"+chr(27)+"[0;0H")
p.print_pantalla()
n = 0
p.start_maze()
while p.actual != 'fin':
    n = n+1
    p.grow_maze()
#    time.sleep(0.05)
print(chr(27)+"[s"+chr(27)+"[0;0H")
p.print_pantalla()

time.sleep(0.5)

p.resolver_puertas()   # no pinta los extremos y detecta dos puertas a veces          
 
p.detectar_puntas()
while len(p.puntas)>0:
 i = p.puntas.pop()
 t = threading.Thread(target=p.borrar_punta(i))
 t.start()

#print p.puntas

print(chr(27)+"[s"+chr(27)+"[0;0H")
p.print_pantalla()
