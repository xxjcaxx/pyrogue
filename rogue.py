# -*- coding: utf-8 -*-
from random import randint
import sys
import time

class pantalla(object):

 def __init__(self,t,salas):
  self.mundo = [['#' for x in range(t)] for x in range(t)]
  exitos = 0
  for s in range(0,salas):
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
      if self.mundo[i][j] == '.':
       chocan = 1
    if chocan == 0:
     cabe = 1
   #  print intentos,
     exitos = exitos + 1
     for i in range(x,x+ax):
      for j in range(y,y+ay):
       self.mundo[i][j]='.'
  #print exitos
 def start_maze(self):
     x = 1
     y = 1
 
 def grow_maze(self):
     self.mundo[randint(1,10)][randint(1,10)] = 'T'

 def print_pantalla(self):
  for i in self.mundo:
   for j in i:
    sys.stdout.write(j+' '),
   print ' '


print 'Empezamos'
p = pantalla(49,40)
print(chr(27) + "[2J")
print(chr(27)+"[s"+chr(27)+"[0;0H")
p.print_pantalla()
n = 0
p.start_maze()
while n < 1000:
    n = n+1
    p.grow_maze()
    time.sleep(1)
    print(chr(27)+"[s"+chr(27)+"[0;0H")
    p.print_pantalla()

