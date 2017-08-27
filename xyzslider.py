# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 20:09:23 2017

@author: Lokesh Johri
"""
import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *
import xyzslider 

from time import sleep

class XYZSlider(QWidget):
    
    
    def __init__(self):
        print('here')
        self.a = QApplication(sys.argv)
        super().__init__()       
        self.initUI()
    
    def show_ux(self):
        sys.exit(self.a.exec_())    
        
    def initUI(self):           
      
      self.setGeometry(10,10,1500,500)  
      
      
      
      self.addSliderZ()  
      self.addSliderX()
      self.addSliderY()
      
 
      
      self.addGripperButton()
      
      self.connectButton = QPushButton('Connect', self)
      self.connectButton.clicked.connect(self.handleConnectButton)
        
      self.exitButton = QPushButton('Exit', self)
      self.exitButton.clicked.connect(self.handleExitButton)
        
      self.setGeometry(300, 300, 1500, 500)
      self.setWindowTitle('Control Sliders')
      
      
      self.sld1.setEnabled(False)
      self.sldX.setEnabled(False)
      self.sldY.setEnabled(False)
      self.gripperButton.setEnabled(False)
      self.mylayout()



      
      self.show()

    def mylayout(self):

      self.qwsld = QWidget() 
      self.qwsld.setStyleSheet("Background-color: red")
      
      self.grid = QGridLayout(self.qwsld)
      self.setLayout(self.grid)
      
      self.subW = QWidget()
      self.grid.addWidget(self.subW,1,1)
      self.subGridW = QGridLayout(self.subW) 
      self.setLayout(self.subGridW)

      self.dummyW = QWidget()        
                    
      connectButtonPos = {"r":1,"c":1}
      exitButtonPos = {"r":1,"c":2}
      gripperButtonPos = {"r":2,"c":1}
      self.grid.addWidget(self.dummyW,2,2)
      
      
      zSliderPos = {"r":2,"c":1}
      zLabelPos = {"r":zSliderPos['r'],"c":2}
      
      xSliderPos = {"r":zSliderPos['r']+1,
                    "c":zSliderPos['c']}
      xLabelPos = {"r":zLabelPos['r']+1,
                   "c":zLabelPos['c']}
      
      ySliderPos = {"r":zSliderPos['r']+2,
                    "c":zSliderPos['c']}
      yLabelPos = {"r":zLabelPos['r']+2,
                   "c":zLabelPos['c']}
      
      
      print(connectButtonPos["r"],"  ",connectButtonPos["c"])
      
      self.subGridW.addWidget(self.connectButton,
                          connectButtonPos["r"],
                          connectButtonPos["c"])
      
      self.subGridW.addWidget(self.exitButton,
                          exitButtonPos["r"],
                          exitButtonPos["c"])  
      
      self.subGridW.addWidget(self.gripperButton,
                          gripperButtonPos["r"],
                          gripperButtonPos["c"])      
      
      self.grid.addWidget(self.l1,
                          zLabelPos["r"],
                          zLabelPos["c"])
      
      self.grid.addWidget(self.sld1,
                          zSliderPos["r"],
                          zSliderPos["c"])
          
      self.grid.addWidget(self.lX,
                          xLabelPos["r"],
                          xLabelPos["c"])
      
      self.grid.addWidget(self.sldX,
                          xSliderPos["r"],
                          xSliderPos["c"])


      self.grid.addWidget(self.lY,
                          yLabelPos["r"],
                          yLabelPos["c"])
      
      self.grid.addWidget(self.sldY,
                          ySliderPos["r"],
                          ySliderPos["c"])
   
    def addGripperButton(self):
      self.gripper = True  
      self.gripperButton = QPushButton('Gripper', self)
      self.gripperButton.clicked.connect(self.handleGripperButton)

    def handleConnectButton(self):
        print('In ConnectButton ')
        self.swift = SwiftAPI(dev_port = 'COM4')
        sleep(2)
        print(self.swift.get_device_info())
        print('set x=150, y=0, z=150')
        self.uarmZ = 150
        self.uarmX = 150
        self.uarmY = 0
        self.swift.set_position(x=self.uarmX,y=self.uarmY,z = self.uarmZ , wait = True,speed=2000)
        self.swift.set_gripper (self.gripper)
        
        self.sld1.setValue(self.uarmZ )
        self.sldX.setValue(self.uarmX )
        self.sldY.setValue(self.uarmY )
        self.sld1.setEnabled(True)
        self.sldX.setEnabled(True)
        self.sldY.setEnabled(True)
        self.gripperButton.setEnabled(True)
        
        self.connectButton.setEnabled(False)
   
    
    def handleGripperButton(self):
        self.gripper = False if self.gripper else True  #toggle
        self.swift.set_gripper(self.gripper)
        sleep(4)
    
    def handleExitButton(self):
        sys.exit()    
                
#----------------------Z----------------     
        
    def changeValueSld1(self):
        txt = "Z: " + str(self.sld1.value()) 
        self.l1.setText(txt)
        #print('changeValue slider is: ', self.sld1.value())
    
    def sliderReleaseSld1(self):
        print('sliderreleased slider is: ', self.sld1.value()) 
        self.uarmZ = self.sld1.value()
        self.swift.set_position(z = self.uarmZ, wait = True,speed=2000)
    

    def addSliderZ(self):
      self.sld1 = QSlider(Qt.Horizontal, self)
      p=self.sld1.palette()
      p.setColor(self.sld1.backgroundRole(), Qt.red)
      self.sld1.setPalette(p)
      self.sld1.setFocusPolicy(Qt.NoFocus)
      self.sld1.setGeometry(30, 40, 1000, 30)
      self.sld1.setMaximum(150)
      self.sld1.setMinimum(0)
      self.sld1.setTickPosition(QSlider.TicksBelow)
      self.sld1.setTickInterval(5) 
      self.sld1.sliderReleased.connect(self.sliderReleaseSld1)
      self.sld1.valueChanged.connect(self.changeValueSld1)
      self.l1 = QLabel(self)
      self.l1.setForegroundRole(QPalette.Dark)
      self.l1.setText('Z:')

#-----------x-----------------------------------------------
    def addSliderX(self):
      self.sldX = QSlider(Qt.Horizontal, self)
      p=self.sldX.palette()
      p.setColor(self.sldX.backgroundRole(), Qt.red)
      self.sldX.setPalette(p)
      self.sldX.setFocusPolicy(Qt.NoFocus)
      self.sldX.setGeometry(30, 40, 1000, 30)
      self.sldX.setMaximum(350)
      self.sldX.setMinimum(100)
      self.sldX.setTickPosition(QSlider.TicksBelow)
      self.sldX.setTickInterval(5) 
      self.sldX.sliderReleased.connect(self.sliderReleaseSldX)
      self.sldX.valueChanged.connect(self.changeValueSldX)

      self.lX = QLabel(self)
      self.lX.setForegroundRole(QPalette.Dark)
      self.lX.setText('X:')
    
    def changeValueSldX(self):
        txt = "X: " + str(self.sldX.value()) 
        self.lX.setText(txt)
        #print('changeValue slider is: ', self.sld1.value())
    
    def sliderReleaseSldX(self):
        print('sliderreleased X slider : ', self.sldY.value()) 
        self.uarmX = self.sldX.value()
        self.swift.set_position(x = self.uarmX, wait = True,speed=2000) 

        
#-----------Y-----------------------------------------------
    def addSliderY(self):
      self.sldY = QSlider(Qt.Horizontal, self)
      p=self.sldY.palette()
      p.setColor(self.sldY.backgroundRole(), Qt.red)
      self.sldY.setPalette(p)
      self.sldY.setFocusPolicy(Qt.NoFocus)
      self.sldY.setGeometry(30, 40, 1000, 30)
      self.sldY.setMaximum(100)
      self.sldY.setMinimum(-100)
      self.sldY.setTickPosition(QSlider.TicksBelow)
      self.sldY.setTickInterval(5) 
      self.sldY.sliderReleased.connect(self.sliderReleaseSldY)
      self.sldY.valueChanged.connect(self.changeValueSldY)

      self.lY = QLabel(self)
      self.lY.setForegroundRole(QPalette.Dark)
      self.lY.setText('Y:')
    
    def changeValueSldY(self):
        txt = "Y: " + str(self.sldY.value()) 
        self.lY.setText(txt)
        #print('changeValue slider is: ', self.sld1.value())
    
    def sliderReleaseSldY(self):
        print('sliderreleased Y slider : ', self.sldY.value()) 
        self.uarmY = self.sldY.value()
        self.swift.set_position(y = self.uarmY, wait = True,speed=2000)      