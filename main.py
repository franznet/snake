# Laboratorio: Busqueda informada
# Implementar un algoritmo de búsqueda inteligente (Busqueda Informada) que
# permita mantener vivo al gusano para obtener el máximo de puntaje.


# Original Source
# Simple Snake Game in Python 3 for Beginners
# By @Franz

import turtle
import time
import random
from collections import deque
from datetime import datetime
import sys

class TPunto():
  def __init__(self, x, y):
    self.x=x
    self.y=y
  def __eq__(self, pPunto):
    return (self.__class__ == pPunto.__class__ and self.x == pPunto.x and self.y == pPunto.y)
  def DistanceM(self, pPunto):  # Distancia Manhattan de dos puntos
    return (abs(self.x - pPunto.x) +  abs(self.y - pPunto.y))
  def Distance(self, pPunto):   # Distancia Euclidiana de dos puntos
    return ( ((self.x - pPunto.x) ** 2) + ((self.y - pPunto.y) ** 2) ) ** 0.5  # fast sqrt
  def toString(self): return '('+str(self.x)+','+str(self.y)+')'

class TFood:
  def __init__(self, pPunto: TPunto):
    self.food = turtle.Turtle()
    self.food.speed(0)
    self.food.shape("circle")
    self.food.color("red")
    self.food.penup()
    self.punto = pPunto
    self.goto(self.punto)

  def randomLocation(self, iMinimo, iMaximo):
    self.punto.x = random.randint(iMinimo, iMaximo)
    self.punto.y = random.randint(iMinimo, iMaximo)
    self.goto(self.punto)

  def goto(self, pPunto: TPunto):
    self.punto = pPunto
    self.food.goto(self.punto.x*20, self.punto.y*20)

  def getPunto(self):
    return self.punto

class TSnake():
  def __init__(self, pPunto: TPunto):
    self.head = turtle.Turtle()
    self.head.speed(0)
    self.head.shape("square")
    self.head.color("black")
    self.head.penup()
    self.direction = "stop"
    self.segments = []
    self.punto=pPunto
    self.goto(self.punto)
    self.detener=False

  def goto(self, pPunto: TPunto):
    self.punto = pPunto
    self.head.direction = "stop"
    self.head.goto(self.punto.x*20, self.punto.y*20)

  def move_up(self):
    self.punto.y+=1
    self.goto(self.punto)

  def move_down(self):
    self.punto.y-=1
    self.goto(self.punto)

  def move_right(self):
    self.punto.x+=1
    self.goto(self.punto)

  def move_left(self):
    self.punto.x-=1
    self.goto(self.punto)

  # Dirección
  def go_up(self):
    if self.direction != "down":
      self.direction = "up"
  def go_down(self):
    if self.direction != "up":
      self.direction = "down"
  def go_left(self):
    if self.direction != "right":
      self.direction = "left"
  def go_right(self):
    if self.direction != "left":
      self.direction = "right"
  def go_pause(self, x, y):
    if self.direction != "pause":
      self.direction="pause"
    else:
      self.direction="stop"

  def move(self):
    if self.direction == "pause": return

    self.mover_segmentos()
    if self.direction == "up":    self.move_up()
    if self.direction == "down":  self.move_down()
    if self.direction == "left":  self.move_left()
    if self.direction == "right": self.move_right()

  def segmentos_clear(self):
    # Mostrarlos lejos
    for segment in self.segments:
      segment.goto(1000,1000)
    self.segments.clear()

  def mover_segmentos(self):
    # Mover al final los primeros segmentos en orden inverso
    for i in range(len(self.segments)-1, 0, -1):
      x, y = self.segments[i-1].punto.x, self.segments[i-1].punto.y
      self.segments[i].punto.x, self.segments[i].punto.y = x, y
      self.segments[i].goto(x*20, y*20)

    # Mover segmento 0 donde la cabeza esta
    if len(self.segments) > 0:
      x, y = self.punto.x, self.punto.y
      self.segments[0].punto.x, self.segments[0].punto.y = x, y
      self.segments[0].goto(x*20,y*20)

  def new_segment(self):
    new_segment = turtle.Turtle()
    new_segment.speed(0)
    new_segment.shape("square")
    new_segment.color("grey")
    new_segment.penup()
    new_segment.punto=TPunto(5, 5)
    self.segments.append(new_segment)

  def segmento_colision(self):
    for segment in self.segments:
      if segment.punto==self.punto:
        return True
    return False

  def punto_en_segmento(self, pPunto):
    for segment in self.segments:
      if segment.punto==pPunto:
        return True
    return False

  def reinicio(self):
    # Eliminar segmentos
    self.segmentos_clear()
    # Ir a primera posicion
    self.goto(TPunto(0,0))
    # Direccion
    self.direction = "stop"

  def cerrar(self):
    self.detener = True

class TCosto():
  def __init__(self, f, g, h):
    self.f=f  # Costo total
    self.g=g  # Costo de alcanzar el nodo(1 en este caso)
    self.h=h  # Costo heuristico(distcancia euclidiana)
  def toString(self, nDecimales=None):
    if nDecimales==None:
      return '('+str(self.f)+','+str(self.g)+','+str(self.h)+')'
    else:
      return '(f='+str(round(self.f,nDecimales))+',g='+str(round(self.g,nDecimales))+',h='+str(round(self.h,nDecimales))+')'

#######################################
# IMPLEMENTACION DEL LABORATORIO:
# Calcular movimiento inteligente
#######################################
class TNodo():
  def __init__(self, punto:TPunto, regla:str, costo:TCosto, estado_padre:'TNodo'):
    self.estado = punto
    self.regla = regla
    self.costo=costo
    self.estado_padre = estado_padre
  def __eq__(self, nNodo):
    return (self.__class__ == nNodo.__class__ and self.estado == nNodo.estado)
  def x(self): return self.estado.x
  def y(self): return self.estado.y
  def f(self): return self.costo.f
  def g(self): return self.costo.g
  def h(self): return self.costo.h

class TLista():
  def __init__(self):
    self.items=[]
  def add(self, nodo:TNodo):
    self.items.append(nodo)
  def visitado(self, nodo:TNodo):
    for n_cerrado in self.items:
      if n_cerrado.estado == nodo.estado:
        return True
    return False
  def len(self):
    return len(self.items)

class TCola():
  def __init__(self):
    self.items=deque()
  def add(self, nodo:TNodo):
    self.items.append(nodo)
  def get(self):
    return self.items.popleft() #Cola
    #return self.items.pop()     #Pila
  def len(self):
    return len(self.items)
  def clear(self):
    self.items.clear()
  def print(self):
    sCadena=''
    for nodo in self.items:
      sCadena+='('+str(nodo.estado[0])+','+str(nodo.estado[1])+','+nodo.estado[2]+')'
    return sCadena
  def clear(self):
    self.items.clear()

class TPila():
  def __init__(self):
    self.items=[]
  def add(self, nodo:TNodo):
    self.items.append(nodo)
  def get(self):
    return self.items.pop()
  def len(self):
    return len(self.items)
  def clear(self):
    self.items.clear()
  def print(self):
    sCadena=''
    for nodo in self.items:
      sCadena+='('+str(nodo.estado[0])+','+str(nodo.estado[1])+','+nodo.estado[2]+')'
    return sCadena

class TGame():
  def __init__(self):
    # Set up the screen
    self.wn = turtle.Screen()
    self.wn.title("Juego de la Serpiente: Búsqueda A* - ")
    self.wn.bgcolor("blue")
    self.wn.setup(width=600, height=600)
    self.wn.tracer(0) # Turns off the screen updates

    #Mensaje de Score
    self.pen = turtle.Turtle()
    self.pen.speed(0)
    self.pen.shape("square")
    self.pen.color("white")
    self.pen.penup()
    self.pen.hideturtle()
    self.pen.goto(0, 260)
    self.pen.write("Puntaje: 0  Puntaje Máximo: 0", align="center", font=("Courier", 18, "normal"))

    # Score
    self.score = 0
    self.high_score = 0
    self.delay = 0.01

    # Snake head
    self.sSnake=TSnake(TPunto(0,0))

    # Snake food
    self.fComida=TFood(TPunto(0,5))

    # Keyboard bindings
    self.wn.listen()
    self.wn.onkeypress(self.sSnake.go_up, "w")
    self.wn.onkeypress(self.sSnake.go_down, "s")
    self.wn.onkeypress(self.sSnake.go_left, "a")
    self.wn.onkeypress(self.sSnake.go_right, "d")
    self.wn.onscreenclick(self.sSnake.go_pause)
    self.wn.onkeypress(self.sSnake.cerrar, "Escape")

  def sHora(Self):
    now = datetime.now()
    return now.strftime("%H:%M:%S")

  def puntaje(self, iScore):
    if iScore==0:
      # Reset the score
      self.score = 0

    else:
      # Increase the score
      self.score = iScore

      if self.score > self.high_score:
        self.high_score = self.score

    # Update the score display
    self.pen.clear()
    self.pen.write("Puntaje: {}  Puntaje Máx.: {}".format(self.score, self.high_score), align="center", font=("Courier", 18, "normal"))

  def titulo(self, sCadena):
    self.wn.title("Juego de la Serpiente: Búsqueda A* - {}".format(sCadena))
  def jugar(self):
    # Main game loop
    while not self.sSnake.detener:
      self.wn.update()

      if self.sSnake.direction=="pause":
        continue

      # Check for a collision with the border
      if self.sSnake.punto.x>14 or self.sSnake.punto.x<-14 or self.sSnake.punto.y>14 or self.sSnake.punto.y<-14:
        time.sleep(1)

        # Reinicio de snake
        self.sSnake.reinicio()

      # Check for a collision with the food
      if self.sSnake.punto==self.fComida.punto:
        # Move the food to a random spot
        while True:
          # Move the food to a random spot
          self.fComida.randomLocation(-14,14)
          self.wn.update()
          print("Verificando comida1")
          #Verificar si no es igual a la cabeza
          if self.sSnake.punto==self.fComida.punto:
            print("Comida en cabeza")
            continue
          print("Verificando comida2")
          #Verificar si no es parte de segmento
          if self.sSnake.punto_en_segmento(self.fComida.punto):
            print("Comida en cola")
            continue
          print("Verificando comida3")
          break

        # Add a segment
        self.sSnake.new_segment()

        # Score
        self.score += 10
        self.puntaje(self.score)

      #######################################
      # CALCULAR NUEVO MOVIMIENTO
      #######################################
      self.smart_move()
      time.sleep(0.1)

      # Mover SNAKE
      self.sSnake.move()

      # Verifica si cabeza colisiono con segmentos del cuerpo
      if self.sSnake.segmento_colision():
          time.sleep(1)

          # Reinicio de juego
          self.sSnake.reinicio()
      time.sleep(self.delay)
    #wn.mainloop()

  # Calcula la nueva posicion de avance para la serpiente utilizado  un algoritmo de búsqueda en anchura.
  def smart_move(self):
    # Estado inicial
    nInicio =  TNodo(self.sSnake.punto, None, TCosto(self.sSnake.punto.Distance(self.fComida.punto), 0, self.sSnake.punto.Distance(self.fComida.punto)), None)
    nFin = TNodo(self.fComida.punto, None, None, None)
    # Agrego estado inicial a abiertos
    cAbierto=TCola()
    cAbierto.add(nInicio)
    # Defino lista de visitados
    lCerrado=TLista()
    # Arreglo de Movimientos
    cMovimiento = TPila()

    while cAbierto.len() != 0:
      # Saco el primer elemento de la cola
      nActual = cAbierto.get()
      # Es solucion?
      if nActual==nFin:
        # Buscar camino recorrido
        print('REGLAS {} \n==================='.format(self.sHora()))
        nRuta = nActual
        while nRuta.estado_padre != None:
          print(nRuta.estado.toString(), '<--- (regla)', nRuta.regla, '--- Costo'+nRuta.costo.toString(1))
          if nRuta.regla!=None:
            cMovimiento.add(nRuta.regla)
          nRuta = nRuta.estado_padre
        print(nRuta.estado.toString(), '<--- (regla)', nRuta.regla)
        if nRuta.regla!=None:
          cMovimiento.add(nRuta.regla)
        print('FIN: ')
        #Seleccionar movimiento
        mov = cMovimiento.get()
        if mov=='U':  self.sSnake.go_up()
        if mov=='D':  self.sSnake.go_down()
        if mov=='R':  self.sSnake.go_right()
        if mov=='L':  self.sSnake.go_left()
        # Mostrar en titulo de ventana
        self.titulo("F[{},{}] H[{},{}]".format(self.fComida.punto.x, self.fComida.punto.y, self.sSnake.punto.x, self.sSnake.punto.y ))
        return
      else:
        # No es solucion, pero ha sido probado antes
        if not lCerrado.visitado(nActual):
          lCerrado.add(nActual)

      # Calcular nuevo movimiento(x,y), regla y  costos(f,g,h)
      mov_posibles = [(TPunto(nActual.x()+1, nActual.y()),  'R', TPunto(nActual.x()+1, nActual.y()  ).Distance(self.fComida.punto)+nActual.g()+1, nActual.g()+1, TPunto(nActual.x()+1, nActual.y()  ).Distance(self.fComida.punto)),
                      (TPunto(nActual.x(),   nActual.y()+1),'U', TPunto(nActual.x(),   nActual.y()+1).Distance(self.fComida.punto)+nActual.g()+1, nActual.g()+1, TPunto(nActual.x(),   nActual.y()+1).Distance(self.fComida.punto)),
                      (TPunto(nActual.x(),   nActual.y()-1),'D', TPunto(nActual.x(),   nActual.y()-1).Distance(self.fComida.punto)+nActual.g()+1, nActual.g()+1, TPunto(nActual.x(),   nActual.y()-1).Distance(self.fComida.punto)),
                      (TPunto(nActual.x()-1, nActual.y()),  'L', TPunto(nActual.x()-1, nActual.y()  ).Distance(self.fComida.punto)+nActual.g()+1, nActual.g()+1, TPunto(nActual.x()-1, nActual.y()  ).Distance(self.fComida.punto))
                    ]

      # Eliminar las posiciones invalidas de retroceso
      if nActual.regla=='U': mov_posibles = [x for x in mov_posibles if x[1]!='D']
      if nActual.regla=='D': mov_posibles = [x for x in mov_posibles if x[1]!='U']
      if nActual.regla=='L': mov_posibles = [x for x in mov_posibles if x[1]!='R']
      if nActual.regla=='R': mov_posibles = [x for x in mov_posibles if x[1]!='L']

      # Elimina movimientos de posiciones que estan fuera de los límites del espacio
      for nodo in mov_posibles:
        if nodo[0].x>14 or nodo[0].x<-14 or nodo[0].y>14 or nodo[0].y<-14:
          mov_posibles = [x for x in mov_posibles if x[1]!=nodo[1]]

      # Elimina movimientos de posiciones de segmento(cola)
      for nodo in mov_posibles:
        if self.sSnake.punto_en_segmento(nodo[0]):
          mov_posibles = [x for x in mov_posibles if x[1]!=nodo[1]]

      # Hallamos el minimo costo de los nodos restantes
      if len(mov_posibles)>0:
        mov_optimo = min(mov_posibles, key = lambda i:i[2])
        cAbierto.add(TNodo(mov_optimo[0], mov_optimo[1], TCosto(mov_optimo[2], mov_optimo[3], mov_optimo[4]), nActual))
      else:
        print('No existen nodos posibles')
        time.sleep(100000)

      print("ABIERTOS({}) CERRADOS({}) - F[{},{}] H[{},{}]".format(cAbierto.len(), lCerrado.len(), self.fComida.punto.x, self.fComida.punto.y, self.sSnake.punto.x, self.sSnake.punto.y) )
      #print('ABIERTOS: ', cAbierto.len())
      #print(cAbierto.print())

juego=TGame()
juego.jugar()
sys.exit() # if you want to exit the entire thing