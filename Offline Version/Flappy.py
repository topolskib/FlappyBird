#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pyglet
from PyQt4 import QtGui, QtCore

pyglet.options['audio'] = ('openal', 'pulse', 'silent')

def doRectanglesCross(x1,y1,xl1,yl1,x2,y2,xl2,yl2):
    """
    Funkcja sprawdza czy prostokaty o wierzcholkach (x1,y1) i (x2,y2) oraz
    dlugosciach bokow (xl1,yl1) i (xl2,yl2) sie przecinaja.
    """
    noOverlap = ((x1>x2+xl2) or (x2>x1+xl1) or (y1+yl1<y2) or (y2+yl2<y1))
    return not noOverlap

class Player():
    def __init__(self,xDef,yDef):
        """
        Konstruktor klasy Player.
        """
        self.x = xDef
        self.y = yDef
        self.location = QtCore.QPoint(self.x,self.y)
    def updateLocation(self):
        """
        Metoda, która uaktualnia atrybuty zmiennej location.
        """
        self.location.setX(self.x)
        self.location.setY(self.y)
class Obstacles():
    def __init__(self,xDef,hDef, areMoving, movingSpeed, parent):
        """
        Konstruktor klasy Obstacles. 
        """
        self.x = xDef
        self.h = hDef
        self.areMoving = areMoving
        self.speed = [-movingSpeed,movingSpeed,-movingSpeed]
        self.parent = parent
    def updatePosition(self, heightModifier):
        """
        Metoda, która uaktualnia położenie przeszkód w poziomie, jeśli właczony jest ich ruch.        
        """
        if self.areMoving == 0:
            return
        for i in range(0,3):
            if (self.h[i]>50 + heightModifier) and (self.h[i]<450 - heightModifier):
                self.h[i] += self.speed[i]*self.parent.ratio
            else:
                self.speed[i] = -self.speed[i]
                self.h[i] += self.speed[i]*self.parent.ratio
                
class BestScores(QtGui.QMainWindow):
    levelLabels={
        '0':'Niezdefiniowany',
        '1':'Latwy',
        '3':'Normalny',
        '5':'Trudny',
        '7':'Zginiesz'}
        
    def __init__(self, parent):
        """
        Konstruktor klasy BestScores. 
        """
        super(BestScores, self).__init__()            
        self.parent = parent  
        self.initUI()
    def initUI(self):
        """
        Metoda tworzaca okno BestScores oraz ustalajaca jego własnosci. 
        """
        qbtn = QtGui.QPushButton('Zamknij', self)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(60, 190)        
        qbtn.clicked.connect(self.close)
        rsbtn = QtGui.QPushButton('Resetuj', self)
        rsbtn.resize(rsbtn.sizeHint())
        rsbtn.move(60, 220)        
        rsbtn.clicked.connect(self.resetScores)
        self.setFixedSize(200,260)
        self.setWindowTitle('Hall of Fame') 
        self.readScores() 
        self.showScores()
        self.center()

    def readScores(self):
        """
        Metoda, ktora czyta najlepsze wyniki zapisane w pliku bestScores_x.txt.
        """
        f = open("./resources/bestScores_" + str(self.parent.difficulty) + ".txt", "r")
        self.names = ["","","","",""]
        self.values = [0,0,0,0,0]
        i=0
        for line in f:
            words = line.split(",")
            self.names[i] = words[0]
            self.values[i] = int(words[1])
            i+=1
        f.close()
    def showScores(self):
        """
        Metoda, ktora wyswietla najlepsze wyniki.
        """    
        self.nameLabels = []
        self.scoreLabels = []
        self.level = QtGui.QLabel("Poziom trudnosci: \n" + self.levelLabels[str(self.parent.difficulty)], self)
        self.level.move(0, 9)
        self.level.resize(200,40)
        self.level.setAlignment(QtCore.Qt.AlignHCenter)
        for i in range(0,5):
            self.nameLabels.append(QtGui.QLabel(self.names[i], self))
            self.scoreLabels.append(QtGui.QLabel(str(self.values[i]), self))
            self.nameLabels[i].move(50, 40+30*i)
            self.scoreLabels[i].move(140, 40+30*i)
    
    def updateScoresDiffChange(self):
        """
        Metoda ktora uaktualnia najlepsze wyniki po zmianie poziomu trudnosci
        """

        self.readScores()
        for i in range(0,5):
            self.nameLabels[i].setText(self.names[i])
            self.scoreLabels[i].setText(str(self.values[i]))
        self.level.setText("Poziom trudnosci: \n" + self.levelLabels[str(self.parent.difficulty)])
        #self.show()  
    def resetScores(self):
        f = open("./resources/bestScores_" + str(self.parent.difficulty) + ".txt", "w")
        fr = open("./resources/bestScores_reset.txt" , "r")
        for i in range(0,5):
            line = fr.readline()
            f.write(line)
        f.close()
        fr.close()
        self.updateScoresDiffChange()
    def updateScores(self, name, score):
        """
        Metoda, ktora uaktualnia najlepsze wyniki o wynik dany na wejsciu, oraz zapisuje je do pliku.
        """
        self.readScores()
        for i in range(0,5):
            if self.values[i]< score:
                for j in range(4,i, -1):
                    self.values[j] = self.values[j-1]
                    self.names[j] = self.names[j-1]
                self.values[i] = score
                self.names[i] = name
                break
        f = open("./resources/bestScores_" + str(self.parent.difficulty) + ".txt", "w")
        for i in range(0,5):
            line = self.names[i] + "," + str( self.values[i]) + "\n"
            f.write(line)
        f.close()
        self.readScores()
        for i in range(0,5):
            self.nameLabels[i].setText(self.names[i])
            self.scoreLabels[i].setText(str(self.values[i]))        
        self.level.setText("Poziom trudnosci: \n" + self.levelLabels[str(self.parent.difficulty)])
        self.show()
    def center(self):
        """
        Metoda, ktora centruje okno.
        """    
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())        
            
            
class FlappyOptions(QtGui.QMainWindow):
    def __init__(self, parent):
        """
        Konstruktor klasy FlappyOptions.
        """
        super(FlappyOptions, self).__init__()        
        self.initUI()
        self.parent = parent
    def initUI(self):
        """
        Metoda, ktora tworzy okno opcji, oraz ustala jego parametry.
        """
        qbtn = QtGui.QPushButton('Zamknij', self)
        qbtn.clicked.connect(self.close)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(520, 50)
        self.setFixedSize(700, 700)
        self.setWindowTitle('Opcje')  
        self.center()
        #self.show()
    def initSliders(self):
        """
        Metoda, ktora tworzy suwaki oraz przyciski odpowiadajace za poszczegolne opcje.
        """
        self.timeBetweenSliderLabel = QtGui.QLabel("Czas miedzy przeszkodami", self)
        self.timeBetweenSliderLabel.move(42,275)
        self.timeBetweenSliderLabel.resize(300,30)
        self.timeBetweenSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.timeBetweenSlider.move(50,300)
        self.timeBetweenSlider.setRange(1000,1500)
        self.timeBetweenSlider.setValue(self.parent.obstacleTimeBetween)
        self.timeBetweenSlider.resize(400,20)
        self.timeBetweenSlider.setTickInterval(100)
        self.timeBetweenSlider.setTickPosition(2)
        self.timeBetweenSliderFirst = QtGui.QLabel("1000", self)
        self.timeBetweenSliderLast = QtGui.QLabel("1500", self)
        self.timeBetweenSliderFirst.move(42,315)
        self.timeBetweenSliderLast.move(428,315)        
        self.timeBetweenSlider.sliderReleased.connect(self.setTimeBetween)        
        self.timeBetweenSliderDisplay = QtGui.QLCDNumber(self)
        self.timeBetweenSliderDisplay.display(self.parent.obstacleTimeBetween)
        self.timeBetweenSlider.valueChanged.connect(self.timeBetweenSliderDisplay.display)
        self.timeBetweenSliderDisplay.move(500,300)
        self.timeBetweenSlider.setToolTip("Ustala czas do pojawienia sie nastepnej przeszkody (ms)")
        
        self.obstacleHeightModifierLabel = QtGui.QLabel("Modyfikator zasiegu przeszkod", self)
        self.obstacleHeightModifierLabel.move(42,355)
        self.obstacleHeightModifierLabel.resize(300,30)
        self.obstacleHeightModifierSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.obstacleHeightModifierSlider.move(50,380)
        self.obstacleHeightModifierSlider.setRange(0,120)
        self.obstacleHeightModifierSlider.setValue(self.parent.obstacleHeightModifier)
        self.obstacleHeightModifierSlider.resize(400,20)
        self.obstacleHeightModifierSlider.setTickInterval(20)
        self.obstacleHeightModifierSlider.setTickPosition(2)
        self.obstacleHeightModifierFirst = QtGui.QLabel("0", self)
        self.obstacleHeightModifierLast = QtGui.QLabel("120", self)
        self.obstacleHeightModifierFirst.move(42,395)
        self.obstacleHeightModifierLast.move(428,395)        
        self.obstacleHeightModifierSlider.sliderReleased.connect(self.setObstacleHeightModifier)        
        self.obstacleHeightModifierDisplay = QtGui.QLCDNumber(self)
        self.obstacleHeightModifierDisplay.display(self.parent.obstacleHeightModifier)
        self.obstacleHeightModifierSlider.valueChanged.connect(self.obstacleHeightModifierDisplay.display)
        self.obstacleHeightModifierDisplay.move(500,380)
        self.obstacleHeightModifierSlider.setToolTip("Zwiekszenie wartosci powoduje zmniejszenie zasiegu mozliwych wartosci wysokosci przeszkod ")
        
        self.obstacleMovingSpeedLabel = QtGui.QLabel("Predkosc ruchu przeszkod", self)
        self.obstacleMovingSpeedLabel.move(42,475)
        self.obstacleMovingSpeedLabel.resize(300,30)
        self.obstacleMovingSpeedSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.obstacleMovingSpeedSlider.move(50,500)
        self.obstacleMovingSpeedSlider.setRange(0,4)
        self.obstacleMovingSpeedSlider.setValue(self.parent.obstacleMovingSpeed)
        self.obstacleMovingSpeedSlider.resize(400,20)
        self.obstacleMovingSpeedSlider.setTickInterval(1)
        self.obstacleMovingSpeedSlider.setTickPosition(2)
        self.obstacleMovingSpeedFirst = QtGui.QLabel("0", self)
        self.obstacleMovingSpeedLast = QtGui.QLabel("4", self)
        self.obstacleMovingSpeedFirst.move(42,515)
        self.obstacleMovingSpeedLast.move(428,515)        
        self.obstacleMovingSpeedSlider.sliderReleased.connect(self.setObstacleMovingSpeed)        
        self.obstacleMovingSpeedDisplay = QtGui.QLCDNumber(self)
        self.obstacleMovingSpeedDisplay.display(self.parent.obstacleMovingSpeed)
        self.obstacleMovingSpeedSlider.valueChanged.connect(self.obstacleMovingSpeedDisplay.display)
        self.obstacleMovingSpeedDisplay.move(500,500)
        self.obstacleMovingSpeedSlider.setToolTip("Zwiekszenie wartosci powoduje zwiekszenie szybkosci, z jaka poruszaja sie przeszkody")
        self.obstacleMovingSpeedSlider.setSingleStep(0.25)
        self.obstacleMovingSpeedSlider.setEnabled(False)
        
        self.obstaclesAreMovingBox = QtGui.QCheckBox("Ruchome przeszkody", self)
        self.obstaclesAreMovingBox.move(42,435)
        self.obstaclesAreMovingBox.resize(180,30)
        self.obstaclesAreMovingBox.setToolTip("Zaznaczenie sprawia, ze przeszkody poruszaja sie w gore i w dol")
        self.obstaclesAreMovingBox.released.connect(self.setObstaclesAreMoving)
        if self.parent.obstaclesAreMoving == 1:
            self.obstaclesAreMovingBox.setChecked(True)
            
        self.audioPlayback = QtGui.QCheckBox("Dzwieki", self)
        self.audioPlayback.move(42,230)
        self.audioPlayback.resize(180,30)
        self.audioPlayback.setToolTip("Wlacza lub wylacza dzwiek")
        self.audioPlayback.released.connect(self.setAudioPlayback)
        if self.parent.audioPlayback == 1:
            self.audioPlayback.setChecked(True)
            
        self.graphicOptionsLabel = QtGui.QLabel("Ustawienia graficzne:", self)
        self.graphicOptionsLabel.move(42,555)    
        self.graphicOptionsLabel.resize(220,30)
        self.graphicOptionLow = QtGui.QRadioButton("Dirty console peasant", self)
        self.graphicOptionLow.move(42, 585)
        self.graphicOptionLow.resize(200,30)
        self.graphicOptionHigh = QtGui.QRadioButton("Glorious PC Master Race", self)
        self.graphicOptionHigh.move(42, 615)
        self.graphicOptionHigh.resize(200,30)
        self.graphicOptionHigh.setChecked(True)
        self.graphicOptions = QtGui.QButtonGroup(self)
        self.graphicOptions.addButton(self.graphicOptionLow,1)
        self.graphicOptions.addButton(self.graphicOptionHigh,2)
        self.graphicOptionLow.clicked.connect(self.setGraphicOptions)
        self.graphicOptionHigh.clicked.connect(self.setGraphicOptions)
        
        self.difficultyOptionsLabel = QtGui.QLabel("Poziom trudnosci:", self)
        self.difficultyOptionsLabel.move(42,50)    
        self.difficultyOptionsLabel.resize(220,30)
        self.difficultyOptionEasy = QtGui.QRadioButton("Latwy", self)
        self.difficultyOptionMedium = QtGui.QRadioButton("Normalny", self)
        self.difficultyOptionHard = QtGui.QRadioButton("Trudny", self)
        self.difficultyOptionExtreme = QtGui.QRadioButton("Zginiesz", self)
        self.difficultyOptionCustom = QtGui.QRadioButton("Niezdefiniowany", self)
        self.difficultyOptionEasy.move(42,80)
        self.difficultyOptionMedium.move(42,110)
        self.difficultyOptionHard.move(42,140)
        self.difficultyOptionExtreme.move(42,170)
        self.difficultyOptionCustom.move(42,200)
        self.difficultyOptionCustom.resize(140,25)
        self.difficultyOptions = QtGui.QButtonGroup(self)
        self.difficultyOptions.addButton(self.difficultyOptionEasy, 1)
        self.difficultyOptions.addButton(self.difficultyOptionMedium, 3)
        self.difficultyOptions.addButton(self.difficultyOptionHard, 5)
        self.difficultyOptions.addButton(self.difficultyOptionExtreme, 7)
        self.difficultyOptions.addButton(self.difficultyOptionCustom, 0)
        self.difficultyOptionMedium.setChecked(True)
        self.difficultyOptionEasy.clicked.connect(self.setDifficultyOptions)
        self.difficultyOptionMedium.clicked.connect(self.setDifficultyOptions)
        self.difficultyOptionHard.clicked.connect(self.setDifficultyOptions)
        self.difficultyOptionExtreme.clicked.connect(self.setDifficultyOptions)
        self.difficultyOptionCustom.clicked.connect(self.setDifficultyOptions)
        
    def setDifficultyOptions(self):
        """
        Metoda, ktora uaktualnia opcje zwiazane z poziomem trudnosci.
        """
        self.parent.difficulty = self.difficultyOptions.checkedId()
        self.parent.initGame()
        self.timeBetweenSlider.setValue(self.parent.obstacleTimeBetween)
        self.timeBetweenSliderDisplay.display(self.parent.obstacleTimeBetween)
        self.obstacleHeightModifierSlider.setValue(self.parent.obstacleHeightModifier)
        self.obstacleHeightModifierDisplay.display(self.parent.obstacleHeightModifier)
        self.obstacleMovingSpeedDisplay.display(self.parent.obstacleMovingSpeed)
        self.obstacleMovingSpeedSlider.setValue(self.parent.obstacleMovingSpeed)
        if self.parent.obstaclesAreMoving == 1:
            self.obstaclesAreMovingBox.setChecked(True)
            self.obstacleMovingSpeedSlider.setEnabled(True)
        if self.parent.obstaclesAreMoving == 0:
            self.obstaclesAreMovingBox.setChecked(False)
            self.obstacleMovingSpeedSlider.setEnabled(False)
        self.parent.difficulty = self.difficultyOptions.checkedId() 
        self.parent.bestScores.updateScoresDiffChange()
        
    def setGraphicOptions(self):
        """
        Metoda, ktora uaktualnia opcje graficzne.
        """
        self.parent.options = self.graphicOptions.checkedId()
        self.parent.setGameOptions(self.parent.options)
        self.parent.setDifficulty(self.parent.difficulty)
        
    def setAudioPlayback(self):
        self.parent.audioPlayback = self.audioPlayback.isChecked()
        
    def setObstacleMovingSpeed(self):
        """
        Metoda, ktora uaktualnia predkosc poruszania sie przeszkod.
        """
        self.parent.obstacleMovingSpeed = self.obstacleMovingSpeedSlider.value()*self.parent.ratio
        self.parent.difficulty = 0
        self.difficultyOptionCustom.setChecked(True)
        
    def setObstaclesAreMoving(self):
        """
        Metoda, ktora uaktualnia czy przeszkody ruszaja sie, czy nie.
        """
        if self.obstaclesAreMovingBox.isChecked():
            self.parent.obstaclesAreMoving = 1
            self.parent.obstacles.areMoving = 1
            self.obstacleMovingSpeedSlider.setEnabled(True)
        else:
            self.parent.obstaclesAreMoving = 0
            self.parent.obstacles.areMoving = 0
            self.obstacleMovingSpeedSlider.setEnabled(False)
        self.parent.difficulty = 0
        self.difficultyOptionCustom.setChecked(True)
        
    def setObstacleHeightModifier(self):  
        """
        Metoda, ktora uaktualnia modyfikator wysokosci przeszkod.
        """
        self.parent.obstacleHeightModifier = self.obstacleHeightModifierSlider.value()
        self.parent.difficulty = 0
        self.difficultyOptionCustom.setChecked(True)
        
    def setTimeBetween(self):
        """
        Metoda, ktora uaktualnia czas miedzy pojawieniem sie kolejnych przeszkod.
        """
        self.parent.obstacleTimeBetween = self.timeBetweenSlider.value()
        self.parent.difficulty = 0
        self.difficultyOptionCustom.setChecked(True)
        
    def center(self):  
        """
        Metoda, ktora centruje okno.
        """    
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class FlappyGame(QtGui.QMainWindow):
    
    #defaults
    speed = 0 
    options = 2
    difficulty = 3    
    audioPlayback = True     
    def __init__(self):
        """
        Konstruktor klasy FlappyGame.
        """
        super(FlappyGame, self).__init__()
        self.initGraphics()         
        self.initGame()  
        self.optionsWindow = FlappyOptions(self)           
        self.bestScores = BestScores(self)   
        self.initUI()
        self.optionsWindow.initSliders()
        self.initSounds()
        
    def setGameOptions(self, sett):
        """
        Metoda, ktora uaktualnia wszystkie opcje zwiazane z danym ustawieniem graficznym.
        """
        if sett ==2:
            self.fps = 60
            self.ratio = 60/self.fps
            self.acc=0.7 * self.ratio**2            
            self.backgroundSpeed = -3* self.ratio
            self.background = self.background_high
            self.pipe = self.pipe_high
            self.pipeReversed = self.pipeReversed_high
            self.playerIconNormal = self.playerIconNormal_high
            self.playerIconAngled = self.playerIconAngled_high
            self.playerIconReversed = self.playerIconReversed_high
            if self.playerIcon == self.playerIconNormal_low:
                self.playerIcon = self.playerIconNormal_high
            if self.playerIcon == self.playerIconAngled_low:
                self.playerIcon = self.playerIconAngled_high
            if self.playerIcon == self.playerIconReversed_low:
                self.playerIcon = self.playerIconReversed_high
            self.repaint()
            
        if sett==1:
            self.fps = 30.00
            self.ratio = 60/self.fps
            self.acc=0.7 * self.ratio**2             
            self.backgroundSpeed = -3 * self.ratio   
            self.backgroundSpeed = -3* self.ratio
            self.background = self.background_low
            self.pipe = self.pipe_low
            self.pipeReversed = self.pipeReversed_low
            self.playerIconNormal = self.playerIconNormal_low
            self.playerIconAngled = self.playerIconAngled_low
            self.playerIconReversed = self.playerIconReversed_low 
            if self.playerIcon == self.playerIconNormal_high:
                self.playerIcon = self.playerIconNormal_low
            if self.playerIcon == self.playerIconAngled_high:
                self.playerIcon = self.playerIconAngled_low
            if self.playerIcon == self.playerIconReversed_high:
                self.playerIcon = self.playerIconReversed_low   
            self.repaint()
            
    def setDifficulty(self, diff):
        """
        Metoda, ktora uaktualnia wszystkie opcje zwiazane z danym ustawieniem trudnosci.
        """
        self.obstacleSpeed = 4*self.ratio
        if diff == 7:
            self.obstacleTimeBetween = 1000
            self.obstacleHeightModifier = 0
            self.obstaclesAreMoving = 1
            self.obstacleMovingSpeed = 3 * self.ratio           
        if diff == 5:
            self.obstacleTimeBetween = 1100
            self.obstacleHeightModifier = 25
            self.obstaclesAreMoving = 1
            self.obstacleMovingSpeed = 2* self.ratio
        if diff == 3:
            self.obstacleTimeBetween = 1200
            self.obstacleHeightModifier = 50  
            self.obstaclesAreMoving = 0  
            self.obstacleMovingSpeed = 0
        if diff == 1:
            self.obstacleTimeBetween = 1300
            self.obstacleHeightModifier = 80   
            self.obstaclesAreMoving = 0 
            self.obstacleMovingSpeed = 0      
    
    def paintEvent(self,event):
        """
        Metoda, ktora rysuje elementy oparte na plikach graficznych - gracza, tlo, przeszkody i licznik punktow. 
        """
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.drawImage( self.backgroundPosition, self.background)
        for i in range(0,3):
            h = self.obstacles.h[i]
            x = self.obstacles.x[i]
            self.pipePosition.setX(x-3)
            self.pipePosition.setY(h-840)
            painter.drawImage(self.pipePosition, self.pipeReversed)
            self.pipePosition.setY(h+160)
            painter.drawImage(self.pipePosition, self.pipe)
        painter.drawImage( self.player.location, self.playerIcon)   
        
        if self.score<10:            
            painter.drawImage( self.scorePositionSingle, self.digits[self.score])
        if self.score>=10:
            painter.drawImage( self.scorePositionDouble1, self.digits[int(self.score/10)])
            painter.drawImage( self.scorePositionDouble2, self.digits[self.score %10])
        painter.end()
        
    def deadAnimation1(self):
        """
        Metoda, ktora uaktywnia pierwsza czesc animacji po smierci.
        """
        if self.audioPlayback:
            self.hitSound.play()
        self.speed = -10
        self.obstacleSpeed = 0
        self.backgroundSpeed = 0
        self.playerIcon = self.playerIconAngled
        self.timerDeadAnimation.start(1000/self.fps)
        self.timerDeadAccurate.start(1)

    def deadAnimation2(self):
        """
        Metoda, ktora uaktywnia druga czesc animacji po smierci.
        """
        if self.player.y >=600:
            self.playerIcon = self.playerIconReversed
            if self.audioPlayback:
                self.dieSound.play()
            self.repaint()
            self.timerDeadAnimation.stop()
            self.timerDeadAccurate.stop()
            if self.checkBestScore() and self.score>0:
                name = self.askForName().strip()
                if name=="": name = "Anonim"				
                self.bestScores.updateScores(name, self.score)
            self.onDeathButtons()
            return
            
    def askForName(self):
        """
        Metoda, ktora pokazuje okno dialogowe z zapytaniem o imie gracza.
        """
        self.releaseKeyboard()
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')  
              
        if ok:
            name = str(text)
            self.grabKeyboard()
            return name
        return "Anonim"
        
    def center(self):
        """
        Metoda, ktora centruje okno.
        """           
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def frameEvent(self):
        """
        Metoda, ktora uaktualnia wartosci zmieniajace sie z kazda klatka - polozenie gracza, i przeszkod. 
        """
        self.backgroundPosition.setX(((self.backgroundPosition.x() + self.backgroundSpeed) % 350)-350)
        if self.firstSpace == 1:
            self.player.y+=self.speed
            self.speed+=self.acc
            self.obstacles.x = self.obstacles.x - self.obstacleSpeed
            self.obstacles.updatePosition(self.obstacleHeightModifier) 
            self.player.updateLocation()
        if (self.player.x > self.obstacles.x[1]+50) and (self.passedObstacle==0):       
            if self.audioPlayback:             
                self.pointSound.play()
            self.score+=1
            self.passedObstacle=1
        
    def startTimer(self):
        """
        Metoda, ktora aktywuje glowny licznik czasu, oraz ten dla przeszkod.
        """
        self.timer.start(1000/self.fps)
        self.obstacleTimer.start(self.obstacleTimeBetween)
        
    def keyPressEvent(self, event):
        """
        Metoda, ktora odpowiada za skok gracza po nacisnieciu spacji.
        """
        key = event.key()
        if key == QtCore.Qt.Key_Space and self.timer.isActive():
            if self.audioPlayback:            
                self.wingSound.play()
            self.firstSpace = 1
            self.speed = -12* self.ratio
            return
        if key == QtCore.Qt.Key_Space and not self.timer.isActive():
            self.bestScores.close()
    def updateObstacles(self):
        """
        Metoda, ktora uaktualnia przeszkody (i tworzy nowa przeszkode) po minieciu czasu mierzonego przez licznik czasu dla przeszkod.
        """
        if self.firstSpace == 1:
            self.obstacles.x[:2] =  self.obstacles.x[1:]
            self.obstacles.h[:2] = self.obstacles.h[1:]
            self.obstacles.speed[:2] = self.obstacles.speed[1:]
            self.obstacles.x[2] = 500
            self.obstacles.h[2] = np.random.random_integers(50+self.obstacleHeightModifier,450 -self.obstacleHeightModifier)
            self.obstacles.speed[2] = np.random.choice( [self.obstacleMovingSpeed, -self.obstacleMovingSpeed])
            self.passedObstacle=0
            
    def checkBestScore(self):
        """
        Metoda, ktora sprawdza, czy gracz osiagnal godny wynik.
        """
        return any(self.bestScores.values < np.repeat(self.score, 5))
    
    def checkIfPlayerLost(self):
        """
        Metoda, ktora sprawdza, czy w danym momencie gracz koliduje z przeszkodami, lub ze skrajnymi krawedziami planszy.
        """
        if self.player.y <=20:
            self.timer.stop()
            self.obstacleTimer.stop()
            self.deadAnimation1()
            return 
        if self.player.y >=620:
            self.timer.stop()
            self.obstacleTimer.stop()
            self.deadAnimation1()
            return
        for i in range(0,2):
            h = self.obstacles.h[i]
            x = self.obstacles.x[i]
            if doRectanglesCross(self.player.x+2, self.player.y+2, 31, 21, x-3,h+160,71,550-h):
                self.timer.stop()
                self.obstacleTimer.stop()
                self.deadAnimation1()
                return
            if doRectanglesCross(self.player.x+2, self.player.y+2, 31, 21, x -3 ,0,71,h):
                self.timer.stop()
                self.obstacleTimer.stop()
                self.deadAnimation1()
                return
                
    def initGame(self):
        """
        Metoda, ktora ustala poczatkowe wartosci zmiennych zwiazanych z gra.
        """
        self.setGameOptions(self.options)
        self.setDifficulty(self.difficulty)
        self.player = Player(75,350)
        self.obstacles = Obstacles(np.array([10000,10000, 10000]), np.repeat(350,3), self.obstaclesAreMoving, self.obstacleMovingSpeed, self)
        self.obstacleTimer = QtCore.QTimer()
        self.timer = QtCore.QTimer()
        self.timerDeadAnimation = QtCore.QTimer()
        self.timerDeadAccurate = QtCore.QTimer()
        self.timer.timeout.connect(self.frameEvent) 
        self.timer.timeout.connect(self.repaint)
        self.timer.timeout.connect(self.checkIfPlayerLost) 
        self.obstacleTimer.timeout.connect(self.updateObstacles)     
        self.timerDeadAnimation.timeout.connect(self.repaint)
        self.timerDeadAnimation.timeout.connect(self.frameEvent)
        self.timerDeadAccurate.timeout.connect(self.deadAnimation2)
        self.playerIcon = self.playerIconNormal
        self.pipePosition = QtCore.QPoint(0,0)
        self.score = 0
        
    def initSounds(self):
        """
        Metoda, ktora wczytuje dzwieki.
        """
        self.pointSound = pyglet.media.load("./sounds/sfx_point.wav", streaming=False)
        self.dieSound = pyglet.media.load("./sounds/sfx_die.wav", streaming=False)
        self.wingSound = pyglet.media.load("./sounds/sfx_wing.wav", streaming=False)
        self.hitSound = pyglet.media.load("./sounds/sfx_hit.wav", streaming=False)    
        
    def initGraphics(self):
        """
        Metoda, ktora wczytuje grafike.
        """
        self.background_high = QtGui.QImage() 
        self.background_high.load("./graphics/background.png")
        self.playerIconNormal_high = QtGui.QImage() 
        self.playerIconNormal_high.load("./graphics/flappy2.png") 
        self.playerIconAngled_high = QtGui.QImage()
        self.playerIconAngled_high.load("./graphics/flappyAngled.png") 
        self.playerIconReversed_high = QtGui.QImage() 
        self.playerIconReversed_high.load("./graphics/flappyDead.png") 
        self.backgroundPosition = QtCore.QPoint(0,0)
        self.pipe_high = QtGui.QImage() 
        self.pipe_high.load("./graphics/pipe.png")
        self.pipeReversed_high = QtGui.QImage() 
        self.pipeReversed_high.load("./graphics/pipeReverted.png")
        self.background_low = QtGui.QImage() 
        self.background_low.load("./graphics/background_low.png")
        self.playerIconNormal_low = QtGui.QImage() 
        self.playerIconNormal_low.load("./graphics/flappy2_low.png") 
        self.playerIconAngled_low = QtGui.QImage()
        self.playerIconAngled_low.load("./graphics/flappyAngled_low.png") 
        self.playerIconReversed_low = QtGui.QImage() 
        self.playerIconReversed_low.load("./graphics/flappyDead_low.png") 
        self.playerIcon = self.playerIconNormal_high
        self.backgroundPosition = QtCore.QPoint(0,0)
        self.pipe_low = QtGui.QImage() 
        self.pipe_low.load("./graphics/pipe_low.png")
        self.pipeReversed_low = QtGui.QImage() 
        self.pipeReversed_low.load("./graphics/pipeReverted_low.png")
        self.c0 = QtGui.QImage("./cyfry/0.png") 
        self.c1 = QtGui.QImage("./cyfry/1.png") 
        self.c2 = QtGui.QImage("./cyfry/2.png") 
        self.c3 = QtGui.QImage("./cyfry/3.png") 
        self.c4 = QtGui.QImage("./cyfry/4.png") 
        self.c5 = QtGui.QImage("./cyfry/5.png") 
        self.c6 = QtGui.QImage("./cyfry/6.png") 
        self.c7 = QtGui.QImage("./cyfry/7.png") 
        self.c8 = QtGui.QImage("./cyfry/8.png") 
        self.c9 = QtGui.QImage("./cyfry/9.png")
        self.digits = [self.c0,self.c1,self.c2,self.c3,self.c4,self.c5,self.c6,self.c7,self.c8,self.c9] 
    
    def initButtons(self):
        """
        Metoda, ktora tworzy trzy podstawowe przyciski, oraz wczytuje do nich grafike.
        """   
        self.playButton = QtGui.QPushButton("", self)
        self.playButton.clicked.connect(self.startGame)
        self.playButton.setIcon(QtGui.QIcon("./graphics/playbutton.png"))
        self.playButton.setIconSize(QtCore.QSize(145,72))
        self.playButton.resize(145,72)
        self.playButton.move(180,400)
        self.playButton.clearFocus()
        
        self.settingsButton = QtGui.QPushButton("", self)
        self.settingsButton.clicked.connect(self.optionsWindow.show)
        self.settingsButton.setIcon(QtGui.QIcon("./graphics/settings.png"))
        self.settingsButton.setIconSize(QtCore.QSize(145,72))
        self.settingsButton.resize(145,72)
        self.settingsButton.move(75,500)
        self.settingsButton.clearFocus()
        
        self.leaderboardsButton = QtGui.QPushButton("", self)
        self.leaderboardsButton.clicked.connect(self.bestScores.updateScoresDiffChange)
        self.leaderboardsButton.clicked.connect(self.bestScores.show)
        self.leaderboardsButton.setIcon(QtGui.QIcon("./graphics/leaderboards.png"))
        self.leaderboardsButton.setIconSize(QtCore.QSize(145,72))
        self.leaderboardsButton.resize(145,72)
        self.leaderboardsButton.move(280,500)   
        self.leaderboardsButton.clearFocus()
    
    def onDeathButtons(self):
        """
        Metoda, ktora wyswietla przyciski po smierci.
        """
        self.playButton.show()
        self.settingsButton.show()
        self.leaderboardsButton.show()
        self.playButton.clicked.connect(self.restartGame)
    
    def showAbout(self):
        """
        Metoda, ktora pokazuje okno about po wybraniu odpowiedniej opcji z menu
        """
        QtGui.QMessageBox.about(self, "About", """ Flappy Bird \n \n
        Instrukcje: \n
        Wciśnij spację, aby podskoczyć. \n
        Po śmierci wciśnij N lub przycisk PLAY, aby spróbować ponownie. \n \n
        Bartosz Topolski 04.01.2016""")
    
    def initUI(self):
        """
        Metoda, ktora tworzy okno gry oraz jego elementy.
        """
        exitAction = QtGui.QAction('Wyjdź', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Wyjdź z gry')
        exitAction.triggered.connect(self.close)
        
        restartAction = QtGui.QAction('Restart', self)
        restartAction.setShortcut('N')
        restartAction.setStatusTip('Restartuj grę')
        restartAction.triggered.connect(self.restartGame)
        
        optionsAction = QtGui.QAction("Opcje", self)
        optionsAction.setStatusTip('Opcje')
        optionsAction.triggered.connect(self.optionsWindow.show)

        leaderboardsAction = QtGui.QAction("Hall of Fame", self)
        leaderboardsAction.setStatusTip('Tabela wyników')
        leaderboardsAction.triggered.connect(self.bestScores.updateScoresDiffChange)
        leaderboardsAction.triggered.connect(self.bestScores.show)
        
        aboutAction = QtGui.QAction("O mnie", self)
        aboutAction.setStatusTip("O mnie")
        aboutAction.triggered.connect(self.showAbout)
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('Plik')
        optionsMenu = menubar.addMenu('Opcje')
        leaderboardsMenu = menubar.addMenu('?')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(restartAction)
        optionsMenu.addAction(optionsAction)
        leaderboardsMenu.addAction(leaderboardsAction)
        leaderboardsMenu.addAction(aboutAction)
        
        self.scorePositionSingle = QtCore.QPoint(231,150)
        self.scorePositionDouble1 = QtCore.QPoint(209,150)
        self.scorePositionDouble2 = QtCore.QPoint(251,150)
        self.setWindowTitle('Flappy Bird')        
        self.initButtons()
        #self.setGeometry(300, 300, 500, 700)
        self.setFixedSize(500,700)
        self.setWindowIcon(QtGui.QIcon('./graphics/flappyIcon.png'))  
        
        self.center()
        self.show()
        self.grabKeyboard()
        
    def startGame(self):        
        """
        Metoda, ktora rozpoczyna gre.
        """
        self.optionsWindow.close()
        self.bestScores.close()
        self.startTimer()
        self.playButton.hide()
        self.settingsButton.hide()
        self.leaderboardsButton.hide()
        self.firstSpace=0
        self.grabKeyboard()
    def restartGame(self):
        """
        Metoda, ktora rozpoczyna gre ponownie po smierci.
        """
        self.setGameOptions(self.options)
        self.setDifficulty(self.difficulty)       
        self.speed = 0
        self.initGame()
        self.repaint()
        self.startGame()
        
def main():
    
    time=0  
    app = QtGui.QApplication(sys.argv)
    ex = FlappyGame()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
