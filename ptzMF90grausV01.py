# Satellite Tracker
'''
Autores: 
Adalto Myiai
Guilherme Marra
Mario Baldini
Fatec-SENAI Dourados

'''


import math
import time
from datetime import datetime
import ephem
import serial
import sys
import urllib.request
import os
# generate random floating point values
#from random import seed
#from random import random

class tracking:
  #Inserir aqui as variaveis compartilhadas com todas instancias da classe
  ptz = serial.Serial('/dev/ttyUSB0', 2400, timeout=3)
  up = bytes.fromhex('FF 01 00 08 3F 00 48')
  down = bytes.fromhex('FF 01 00 10 3F 00 50')
  left = bytes.fromhex('FF 01 00 04 00 3F 44')
  right = bytes.fromhex('FF 01 00 02 00 3F 42')
  stop = bytes.fromhex('FF 01 00 00 00 00 01')
  upleft = bytes.fromhex('FF 01 00 0C 3F 3F 8B')
  upright = bytes.fromhex('FF 01 00 0A 3F 3F 89')
  downleft = bytes.fromhex('FF 01 00 14 3F 3F 93')
  downright = bytes.fromhex('FF 01 00 12 3F 3F 91')
  # Conversao Angulo-tempo do Ptz
  AZ = 37.6/355		# Calibracao tracking inicial 10-04-2019
  EL= 14.4/90		  # Calibracao tracking inicial 10-04-2019
  AZfino = 42/355		# Calibracao tracking angulos pequenos 10-04-2019
  ELfino= 15.8/90		  # Calibracao tracking angulos pequenos 10-04-2019
  spaz= 0
  spel= 0
  spaz2 = 0
  spel2 = 0
  spaz3 = 0
  spel3 = 0
  azheading = 0
  i = 0
  
  def __init__(self):
    #Inserir aqui as variaveis compartilhadas que sao unicas para cadas instanciacao
    pass

  
  def grabTLE(self):
    self.target_url = "https://www.celestrak.com/NORAD/elements/cubesat.txt"
    self.txt = urllib.request.urlopen(self.target_url).read()
    self.i=0
    self.linebytes = self.txt.splitlines()
    #print(self.linebytes)
    for self.line in self.linebytes:
      if b'42792U' in self.line:
        #print(self.line.decode())
        #foster = self.linebytes[i-1:i+1]
        #print(self.foster)
        self.title = self.linebytes[self.i-1].decode()
        self.lineone = self.linebytes[self.i].decode()
        self.linetwo = self.linebytes[self.i+1].decode()
        print(self.title)
        print(self.lineone)
        print(self.linetwo)
        #print(self.linebytes[i+1].decode())
        break
      else:
        self.title = 'SWAYAM'
        self.lineone = '1 41607U 16040J   19133.66674742  .00001786  00000-0  78310-4 0  9993'
        self.linetwo = '2 41607  97.3683 196.3816 0014355 151.8382 208.3634 15.23186187160393'
        break
      self.i+=1
    return

  def obs(self):
    self.degrees_per_radian = 180.0 / math.pi
    self.home = ephem.Observer()
    self.home.lat = '-22.2218'   # +N
    self.home.lon = '-54.8064'   # +E
    self.home.elevation = 430 	# meters
    # Automatizar a aquisicao das lines de TLE do proprio celestrak
    self.chosensat = ephem.readtle(self.title,
    self.lineone,
    self.linetwo
    )


  
  # Starts de todas as configuracoes possiveis
  def startAll(self):
    self.ptz.write(self.down)		#Nivel Zero na elevacao em 12.5s
    time.sleep(18)
    self.ptz.write(self.up)		#Nivel Zero na elevacao em 12.5s
    time.sleep(12.4)
    self.ptz.write(self.stop)
    time.sleep(1)
    if tr1.azheading >= 0 and tr1.spaz <= 180:
      self.ptz.write(self.left)
      time.sleep(40)
    if tr1.azheading < 0 and tr1.spaz > 180:
      self.ptz.write(self.right)
      time.sleep(40)
    if tr1.azheading < 0 and tr1.spaz <= 180:
      self.ptz.write(self.left)
      time.sleep(40)
      self.ptz.write(self.right)
      time.sleep(180*self.AZ)
    if tr1.azheading >= 0 and tr1.spaz > 180:
      self.ptz.write(self.right)
      time.sleep(40)
      self.ptz.write(self.right)
      time.sleep(180*self.AZ)
    self.ptz.write(self.stop)
    time.sleep(1)
    pass
  

  def startVars(self):
    #Reinicializacao Variaveis
    self.spaz= 0
    self.spel= 0
    self.spaz2 = 0
    self.spel2 = 0
    self.spaz3 = 0
    self.spel3 = 0
    self.spaz4 = 0
    self.spel4 = 0
    self.azheading = 0
    self.elheading = 0    
    self.i = 0
    return

  # Definindo funcao obter dados sat
  def getSatData(self):
    self.home.date = datetime.utcnow()
    self.chosensat.compute(self.home)
    self.spaz= self.chosensat.az*self.degrees_per_radian
    self.spel= self.chosensat.alt*self.degrees_per_radian
    #self.spaz = 130 #Para MA
    #self.spel = 30 #Para MA

  def sentidoAz(self):
    # Identificacao Sentido do Azimute (cresente ou decrescente) e Tracking Inicial
    self.i = 0
    while self.i <= 1:
      self.getSatData()
      self.azheading= self.spaz - self.azheading
      time.sleep(1)
      self.i+=1
      #self.azheading = -1 #Para malha aberta
    return self.azheading
    

  # Funcao Azimute Horario Up
  def azelTRK(self):
    #Tracking Inicial
    #os.system('clear') or None
    self.getSatData()
    print(self.title + ': Azimute %5.1f deg, Elevacao %4.1f deg' % (self.spaz, self.spel))
    print("")
    self.spaz2 = self.spaz
    self.spel2 = self.spel
    self.spaz4 = 0
    self.spel4 = 0
    if self.spel <= 90 and self.spel > 0 and self.spaz >= 0 and self.spaz < 332:	#Deixando 332 como limite de azimute
      #azup
      if self.azheading >= 0 and self.spaz <= 180:
        self.ptz.write(self.right)	#Sentido Horario Azimute Up
        time.sleep(self.spaz*self.AZ)
      #azdown
      if self.azheading < 0 and self.spaz > 180:
        self.ptz.write(self.left)	#Sentido Antihorario Azimute Down
        time.sleep((360-self.spaz-26)*self.AZ)	#Incluindo a correcao partindo de 334 graus (que eh 26 graus)
      #azhalfdown
      if self.azheading < 0 and self.spaz <= 180:
        self.ptz.write(self.left)	#Sentido Antihorario Azimute Down
        time.sleep((180-self.spaz)*self.AZ)	#Partindo de 180 graus
      #azhalfup
      if self.azheading >= 0 and self.spaz > 180:
        self.ptz.write(self.left)	#Sentido Antihorario Azimute Down
        time.sleep((self.spaz-180)*self.AZ)	#Partindo de 180 graus   
      self.ptz.write(self.down)
      time.sleep((90-self.spel)*self.EL)  #Correcao para partir de 90 graus de elev
      self.ptz.write(self.stop)   
      # Tracking Incrementos
      while self.spel <= 90 and self.spel > 0 and self.spaz >= 0 and self.spaz < 332 and self.chosensat.range <= 3000000:	#Deixando 332 como limite de azimute
        print("Rotina de incrementos rodando")
        self.elheading = self.spel
        self.spaz2 = self.spaz
        self.spel2 = self.spel
        self.getSatData()          #Atualizacao do valor em MF
        #self.spaz-=random()*5
        #self.spel+=random()*3
        self.spaz3=abs(self.spaz2-(self.spaz))
        self.spel3=abs(self.spel2-(self.spel))
        self.spaz4+=self.spaz3
        self.spel4+=self.spel3
        print(self.spaz3) #Correcao instantanea
        print(self.spel3)
        #os.system('clear') or None
        print(self.title + ': Azimute %5.1f deg, Elevacao %4.1f deg' % (self.spaz, self.spel))
        print("")
        if self.spaz4 >= 3:
          if self.azheading >= 0:
            self.ptz.write(self.right)
          if self.azheading < 0:
            self.ptz.write(self.left)
          time.sleep(self.spaz4*self.AZfino)
          self.ptz.write(self.stop)  
          print("Correcao azim acumulada: ")
          print("")
          print(self.spaz4) #Correcao acumulada
          self.spaz4 = 0
        self.elheading = self.spel-self.elheading
        if self.elheading>0 and self.spel4 >=3:
          self.ptz.write(self.up)   #Em relacao aos codes anteriores, down virou up
          time.sleep(self.spel4*self.ELfino)
          self.ptz.write(self.stop)         
          print("EL para cima")
          print("Correcao elev acumulada: ")
          print("")
          print(self.spel4) #Correcao acumulada
          self.spel4 = 0
          pass
        if self.elheading==0 and self.spel4 >=3:
          self.spel4 = 0
          print("do nothing")
          pass
        if self.elheading<0 and self.spel4 >=3:
          self.ptz.write(self.down)   #Em relacao aos codes anteriores, up virou down
          time.sleep(self.spel4*self.ELfino)
          self.ptz.write(self.stop)
          print("EL para baixo")
          print("Correcao elev acumulada: ")
          print("")
          print(self.spel4) #Correcao acumulada
          self.spel4 = 0
          pass  
        time.sleep(3)


#Corpo do Programa (Apenas uso das funcoes de classe)
# seed random number generator
#seed(1)
tr1 = tracking()
tr1 = grabTLE()
tr1.obs()
tr1.startVars()
tr1.getSatData()
tr1.sentidoAz()

while 1:
  os.system('clear')
  print("Chosen Satellite: "+tr1.title)
  print("Distancia Satelite->Observador: ")
  print(tr1.chosensat.range)
  tr1.startVars()
  tr1.getSatData()
  tr1.sentidoAz()
  if tr1.chosensat.range <= 3000000:
    tr1.startAll()
    tr1.azelTRK()
    time.sleep(2)
    if tr1.chosensat.range > 3000000:
      tr1.ptz.close
      sys.exit(0)
