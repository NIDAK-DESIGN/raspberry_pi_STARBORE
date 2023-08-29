# -*- coding: cp1252 -*-
import sys
import os
import time
from PySide.QtGui import *
from PySide.QtCore import *
from coms import CNC
from PySide.phonon import Phonon
from controls import borderLessButton
from maintDialogs import dlgInputTest, dlgOutputTest, dlgInfo, dlgTools
from tunningDialogs import dlgGralParams
from motorDialogs import dlgMotorTunning
from homeDialog import dlgHomeConfig
from jog import dlgJog
from basicFuncs import *
from TAPEditor import dlgTAPEditor
import threading
from basicDialogs import dlgInputNumber
from mainDialogs import *
from lang import cLanguage
from os import listdir
import re

class dlgDimensions(QDialog):
    def __init__(self, dims, mrkEdge, filename, isOpenFile=False, parent=None):
        super(dlgDimensions, self).__init__(parent)

        self.lang = cLanguage()
        self.filename = filename
        self.isOpenFile = isOpenFile
        self.closedOk = False

        # Create widgets
        self.setFont(QFont('SansSerif', 14))

        lblStyle = "QLabel {color: white; font-size:14pt; float: center;}"

        lblXdim = QLabel( dims[0] )
        lblXdim.setStyleSheet( lblStyle )
        lblXdim.setMaximumWidth(100)
        lblYdim = QLabel( dims[1] )
        lblYdim.setStyleSheet( lblStyle )
        lblZdim = QLabel( dims[2] )
        lblZdim.setStyleSheet( lblStyle )
        lblPieza = QLabel()
        lblPieza.setPixmap(QPixmap("pieza.png"))
        lblFlecha = QLabel()
        lblFlecha.setPixmap(QPixmap("leftArrow.png"))

        lblFilename = QLabel( filename )
        lblFilename.setStyleSheet( lblStyle )
        
        btnOk = borderLessButton(self.lang.tr("ok"), "iconOk48.png")
        btnOk.clicked.connect(self.handleOk)
        btnDel = borderLessButton(self.lang.tr("delete"), "iconRecycle48.png")
        btnCancel = borderLessButton(self.lang.tr("cancel"), "iconCancel48.png")
        btnCancel.clicked.connect(self.handleCancel)

        wPieza = wdgtPieza(mrkEdge)
        grid = QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(lblXdim, 2, 1)
        grid.addWidget(lblYdim, 1, 2)
        grid.addWidget(lblZdim, 0, 2)
        grid.addWidget(wPieza, 1, 1)
        grid.addWidget(lblFlecha, 1, 0)
        grid.addWidget(btnOk, 6, 1)

        # Se habilita el botón eliminar cuando el fichero seleccionado
        # No es el fichero abierto previamente. EN caso de que haya alguno
        # NIDAK 20190917



        if self.isOpenFile == False:
            btnDel.clicked.connect(self.handleDel)
        else:
            btnDel = borderLessButton(self.lang.tr("delete"), "iconRecycleDisabled48.png")

        grid.addWidget(btnDel, 6, 2)
        grid.addWidget(btnCancel, 6, 3)
        grid.addWidget(lblFilename, 0, 1)

        self.setLayout(grid)
        if develPlatform() == True:
            self.setGeometry(50, 50, screenWidth, screenHeight)
        else:
            self.setGeometry(0, 0, screenWidth, screenHeight)

        self.setStyleSheet("QDialog {background-color: #232234;color:#ffffff;}")

    def handleOk( self ):
        self.closedOk = True
        self.filename = ""
        self.close()

    def handleDel(self):

        msg = QMessageBox()
       #msg.setStyle("color:white")
        if msg.question(self, "STARBORE", self.lang.tr("Do you want to delete the file ") + self.filename + "?", QMessageBox.Yes | QMessageBox.No) \
                == QMessageBox.Yes:
            os.remove(self.filename)
            self.closedOk = False
            self.filename = ""
            self.close()

    def handleCancel( self ):
        self.closedOk = False
        self.filename = ""
        self.close()

class wdgtPieza(QWidget):
    def __init__(self, mrkEdge):
        super(wdgtPieza, self).__init__()
        self.initUI(mrkEdge)

    def initUI(self, mrkEdge):
        self.mrkEdge  = mrkEdge
        self.pixmap = QPixmap("pieza.png")

        self.setFixedSize(self.pixmap.size())
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.drawPixmap(self.rect(), self.pixmap)

        pen = QPen(Qt.red, 7)
        qp.setPen(pen)

        # Canto izquierda
        if self.mrkEdge[0]:
            qp.drawLine(7, 84, 7, 253)

        # Canto derecha
        if self.mrkEdge[1]:
            qp.drawLine(249, 84, 249, 253)

        # Canto superior
        if self.mrkEdge[2]:
            qp.drawLine(7, 84, 249, 84)

        # Canto inferior
        if self.mrkEdge[3]:
            qp.drawLine(7, 253, 249, 253)

        qp.end()
        
class dlgHelp(QDialog):
    def __init__(self, parent=None):
        super(dlgHelp, self).__init__(parent)
        self.playing = False
        self.lang = cLanguage()
        
        # Create widgets
        self.setFont(QFont('SansSerif', 14))
        self.setStyleSheet("QDialog {background-color: #232234;color:#ffffff;}")

        with open("cfg.txt") as f:
            cfg = f.readlines()

        self.videoTitles = []
        self.videoNames = []

        for line in cfg:
            if "video:" in line:
                fields = line.split(":")
                self.videoTitles.append(fields[1])
                self.videoNames.append(fields[2])

        btnClose = borderLessButton(self.lang.tr("close"), "")
        btnClose.clicked.connect(self.handleClose)
        
        grid = QGridLayout()
        grid.setSpacing(5)

        buttons = []
        for i in range(len(self.videoTitles)):
            buttons.append( borderLessButton(self.videoTitles[i], "") )
            buttons[i].clicked.connect(self.handleVideo)
            grid.addWidget(buttons[i], i% 5, i / 5)

        grid.addWidget(btnClose, 6, 0)
        self.setLayout(grid)
        
        if develPlatform() == True:
            self.setGeometry(50, 50, screenWidth, screenHeight)
        else:
            self.setGeometry(0,0, screenWidth, screenHeight)

    def handleVideo(self):
        videoTitle = self.sender().text()
        idx = self.videoTitles.index(videoTitle)
        videoFile = self.videoNames[idx]
        self.playing = True

        from subprocess import Popen
        omxc = Popen(['omxplayer', '--win', '0,0,800,400', 'videos/'+videoFile])
        
    def handleVideo1(self):
        self.playing = True
        
    def handleClose(self):
        if self.playing == True:
            os.system('killall omxplayer.bin')
            self.playing = False
        else:
            self.close()            
    
class dlgOutputConfig(QDialog):
    def __init__(self, cnc, parent=None):
        super(dlgOutputConfig, self).__init__(parent)

        self.cnc = cnc
        self.cnc.readConfig()

        self.lang = cLanguage()
        
        # Create widgets
        self.setFont(QFont('SansSerif', 16))
        self.setStyleSheet("QDialog {background-color: #232234;color:#ffffff;}")

        lblOut1 = QLabel(self.lang.tr("PRESS"))
        lblOut1.setStyleSheet(labelStyle)
        self.out1Group = createIOConfigGroup()

        buttons = self.out1Group.findChildren(QRadioButton)
        if self.cnc.outputs[0].sense == 0:
            buttons[0].setChecked(True)
        else:
            if self.cnc.outputs[0].sense == 1:
                buttons[1].setChecked(True)
            else:
                buttons[2].setChecked(True)
        
        lblSpire = QLabel(self.lang.tr("AS SPIRE?"))
        lblSpire.setStyleSheet(labelStyle)
        self.spireGroup = createYesNoConfigGroup()

        buttons = self.spireGroup.findChildren(QRadioButton)
        print("spire delay:"+str(self.cnc.spireDelay))
        if self.cnc.spireDelay == 1:
            buttons[0].setChecked(True)
        else:
            buttons[1].setChecked(True)

        lblSpireDelay = QLabel(self.lang.tr("SPIRE DELAY"))
        lblSpireDelay.setStyleSheet(labelStyle)
        self.txtSpireDelay = QLineEdit()
        self.txtSpireDelay.setText(str(self.cnc.spireEnabled/10.0))
        self.txtSpireDelay.installEventFilter( self )
        
        lblOut2 = QLabel(self.lang.tr("CLAMP"))
        lblOut2.setStyleSheet(labelStyle)
        self.out2Group = createIOConfigGroup()

        buttons = self.out2Group.findChildren(QRadioButton)
        if self.cnc.outputs[1].sense == 0:
            buttons[0].setChecked(True)
        else:
            if self.cnc.outputs[1].sense == 1:
                buttons[1].setChecked(True)
            else:
                buttons[2].setChecked(True)
                
        
        lblOut3 = QLabel(self.lang.tr("DRILL"))
        lblOut3.setStyleSheet(labelStyle)
        self.out3Group = createIOConfigGroup()

        buttons = self.out3Group.findChildren(QRadioButton)
        if self.cnc.outputs[2].sense == 0:
            buttons[0].setChecked(True)
        else:
            if self.cnc.outputs[2].sense == 1:
                buttons[1].setChecked(True)
            else:
                buttons[2].setChecked(True)
                
        
        lblDelay = QLabel(self.lang.tr("DRILL DELAY"))
        lblDelay.setStyleSheet(labelStyle)
        self.txtDelay = QLineEdit()
        self.txtDelay.setText(str(self.cnc.drillDelay))
        self.txtDelay.installEventFilter( self )
        
        
        btnOk = borderLessButton(self.lang.tr("save"), "iconOk.png")
        btnOk.clicked.connect(self.handleOk)
        
        btnCancel = borderLessButton(self.lang.tr("cancel"), "iconCancel.png")
        btnCancel.clicked.connect(self.close)
        
        grid = QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(lblOut1, 0, 0)
        grid.addWidget(self.out1Group, 0 ,1)
        
        grid.addWidget(lblSpire, 1, 0)
        grid.addWidget(self.spireGroup, 1 ,1)
        
        grid.addWidget(lblSpireDelay, 2, 0)
        grid.addWidget(self.txtSpireDelay, 2, 1)
        
        grid.addWidget(lblOut2, 3, 0)
        grid.addWidget(self.out2Group, 3, 1)
        
        grid.addWidget(lblOut3, 4, 0)
        grid.addWidget(self.out3Group, 4, 1)
        
        grid.addWidget(lblDelay, 5, 0)
        grid.addWidget(self.txtDelay, 5, 1)
        
        grid.addWidget(btnCancel, 6, 0)
        grid.addWidget(btnOk, 6, 2)

        
        self.setLayout(grid)
        if develPlatform() == True:
            self.setGeometry(50, 50, screenWidth, screenHeight)
        else:
            self.setGeometry(0,0, screenWidth, screenHeight)

    def eventFilter( self, widget, event):
        if event.type() == QEvent.MouseButtonPress:
            if widget is self.txtDelay:
                dialog = dlgInputNumber(pos=(290,50), widg = self.txtDelay)
                dialog.show()
                    
                dialog.exec_()
            else:
                if widget is self.txtSpireDelay:
                    dialog = dlgInputNumber(pos=(290,50), widg = self.txtSpireDelay)
                    dialog.show()
                    
                    dialog.exec_()

        return QWidget.eventFilter(self, widget, event)
                
                
    def handleOk(self):
        # Sólo enviamos coms para guardar las cosas que hayan cambiado

        value = int(10*float(self.txtSpireDelay.text()))
        if value != self.cnc.spireEnabled:
            #param = "config.outputs.spireDelay"
            param = "config.outputs.spireEnabled"
            self.cnc.saveConfig(param, value)

        value = int(10*float(self.txtDelay.text()))
        if value != self.cnc.drillDelay:
            param = "config.outputs.DrillDelay"
            self.cnc.saveConfig(param, value)
        
        buttons = self.out1Group.findChildren(QRadioButton)
        i=0
        for b in buttons:
            if b.isChecked():
                sense = i
                break
            i += 1
        
        if self.cnc.outputs[0].sense != sense:
            tmps = "config.outputs.ClipActiveLow "+str(sense)
            param = "config.outputs.ClipActiveLow"
            value = str(sense)
            self.cnc.saveConfig(param, value)

        # Use clamp as SPIRE
        buttons = self.spireGroup.findChildren(QRadioButton)
        if buttons[0].isChecked():
            spireEnabled = True
            spireValue = 1
        else:
            spireEnabled = False
            spireValue = 0
            
        if self.cnc.spireEnabled != spireValue:
            tmps = "config.outputs.spireEnabled "+str(spireValue)
            #param = "config.outputs.spireEnabled"
            param = "config.outputs.spireDelay"
            value = str(spireValue)
            self.cnc.saveConfig(param, value)

        buttons = self.out2Group.findChildren(QRadioButton)
        i=0
        for b in buttons:
            if b.isChecked():
                sense = i
                break
            i += 1
        
        if self.cnc.outputs[1].sense != sense:
            param = "config.outputs.ClampActiveLow"
            value = str(sense)
            self.cnc.saveConfig(param, value)
            print("Change output clamp, "+param+": "+str(value))

        buttons = self.out3Group.findChildren(QRadioButton)
        i=0
        for b in buttons:
            if b.isChecked():
                sense = i
                break
            i += 1
        
        if self.cnc.outputs[2].sense != sense:
            param = "config.outputs.DrillActiveLow"
            value = str(sense)
            self.cnc.saveConfig(param, value)
            print("Change output drill, "+param+": "+str(value))
            
        self.close()
            
            
class dlgInputConfig(QDialog):
    def __init__(self, cnc, parent=None):
        super(dlgInputConfig, self).__init__(parent)

        self.cnc = cnc
        self.cnc.readConfig()

        self.lang = cLanguage()
        
        # Create widgets
        self.setFont(QFont('SansSerif', 16))
        self.setStyleSheet("QDialog {background-color: #232234;color:#ffffff;}")
            
        lblEmerg = QLabel(self.lang.tr("E_STOP"))
        lblEmerg.setStyleSheet(labelStyle)
        lblIconEmerg = QLabel("")
        lblIconEmerg.setPixmap(QPixmap("iconEmergency32Off.png"))
        self.emergGroup = createIOConfigGroup()

        buttons = self.emergGroup.findChildren(QRadioButton)
        #buttons = self.emergGroup.buttons()
        
        if self.cnc.inputs[1].sense == 0:
            buttons[1].setChecked(True)
        else:
            if self.cnc.inputs[1].sense == 1:
                buttons[0].setChecked(True)
            else:
                buttons[2].setChecked(True)

        lblDoor = QLabel(self.lang.tr("DOOR"))
        lblDoor.setStyleSheet(labelStyle)
        lblIconDoor = QLabel("")
        lblIconDoor.setPixmap(QPixmap("iconDoor32Off.png"))

        self.doorGroup = createIOConfigGroup()

        buttons = self.doorGroup.findChildren(QRadioButton)
        #buttons = self.doorGroup.buttons()
        if self.cnc.inputs[2].sense == 0:
            buttons[1].setChecked(True)
        else:
            if self.cnc.inputs[2].sense == 1:
                buttons[0].setChecked(True)
            else:
                buttons[2].setChecked(True)

        
        lblAir = QLabel(self.lang.tr("AIR"))
        lblIconAir = QLabel("")
        lblIconAir.setPixmap(QPixmap("iconAir32Off.png"))
        lblAir.setStyleSheet(labelStyle)
        self.airGroup = createIOConfigGroup()

        buttons = self.airGroup.findChildren(QRadioButton)
        #buttons = self.airGroup.buttons()
        if self.cnc.inputs[3].sense == 0:
            buttons[1].setChecked(True)
        else:
            if self.cnc.inputs[3].sense == 1:
                buttons[0].setChecked(True)
            else:
                buttons[2].setChecked(True)
        
        lblGrease = QLabel(self.lang.tr("HEADER LOCK"))
        lblGrease.setStyleSheet(labelStyle)
        lblIconGrease = QLabel("")
        lblIconGrease.setPixmap(QPixmap("iconGrease32Off.png"))
        self.greaseGroup = createIOConfigGroup()

        buttons = self.greaseGroup.findChildren(QRadioButton)
        #buttons = self.greaseGroup.buttons()
        if self.cnc.inputs[4].sense == 0:
            buttons[1].setChecked(True)
        else:
            if self.cnc.inputs[4].sense == 1:
                buttons[0].setChecked(True)
            else:
                buttons[2].setChecked(True)
        
        lblStart = QLabel(self.lang.tr("START"))
        lblStart.setStyleSheet(labelStyle)
        lblIconStart = QLabel("")
        lblIconStart.setPixmap(QPixmap("iconStart32Off.png"))
        self.startGroup = createIOConfigGroup()

        buttons = self.startGroup.findChildren(QRadioButton)
        #buttons = self.startGroup.buttons()
        if self.cnc.inputs[5].sense == 0:
            buttons[1].setChecked(True)
        else:
            if self.cnc.inputs[5].sense == 1:
                buttons[0].setChecked(True)
            else:
                buttons[2].setChecked(True)
        
        lblInverter = QLabel(self.lang.tr("INVERTER"))
        lblInverter.setStyleSheet(labelStyle)
        lblIconInverter = QLabel("")
        lblIconInverter.setPixmap(QPixmap("iconInverter32Off.png"))
        self.inverterGroup = createIOConfigGroup()

        buttons = self.inverterGroup.findChildren(QRadioButton)
        #buttons = self.inverterGroup.buttons()
        
        if self.cnc.inputs[0].sense == 0:
            buttons[1].setChecked(True)
        else:
            if self.cnc.inputs[0].sense == 1:
                buttons[0].setChecked(True)
            else:
                buttons[2].setChecked(True)

        btnOk = borderLessButton(self.lang.tr("save"), "iconOk.png")
        btnOk.clicked.connect(self.handleOk)
        
        btnCancel = borderLessButton(self.lang.tr("cancel"), "iconCancel.png")
        btnCancel.clicked.connect(self.close)
        
        grid = QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(lblIconEmerg, 0, 0)
        grid.addWidget(lblEmerg, 0, 1)
        grid.addWidget(self.emergGroup, 0, 2)

        grid.addWidget(lblIconDoor, 1, 0)
        grid.addWidget(lblDoor, 1, 1)
        grid.addWidget(self.doorGroup, 1 ,2)

        grid.addWidget(lblIconAir, 2, 0)
        grid.addWidget(lblAir, 2, 1)
        grid.addWidget(self.airGroup, 2, 2)

        grid.addWidget(lblIconGrease, 3, 0)
        grid.addWidget(lblGrease, 3, 1)
        grid.addWidget(self.greaseGroup, 3, 2)

        grid.addWidget(lblIconStart, 4, 0)
        grid.addWidget(lblStart, 4, 1)
        grid.addWidget(self.startGroup, 4, 2)

        grid.addWidget(lblIconInverter, 5, 0)
        grid.addWidget(lblInverter, 5, 1)
        grid.addWidget(self.inverterGroup, 5, 2)
        
        grid.addWidget(btnCancel, 6, 1)
        grid.addWidget(btnOk, 6, 2)

        
        self.setLayout(grid)
        if develPlatform() == True:
            self.setGeometry(50, 50, screenWidth, screenHeight)
        else:
            self.setGeometry(0,0, screenWidth, screenHeight)

    def handleOk(self):

        # Como las inputs sólo tienen un parámetro que es sense, simplificamos
        # con un buffer de enteros
        senses = []
        buttons = self.inverterGroup.findChildren(QRadioButton)
        if buttons[0].isChecked():
            senses.append(1)
        else:
            if buttons[1].isChecked():
                senses.append(0)
            else:
                senses.append(2)

        buttons = self.emergGroup.findChildren(QRadioButton)
        if buttons[0].isChecked():
            senses.append(1)
        else:
            if buttons[1].isChecked():
                senses.append(0)
            else:
                senses.append(2)

        buttons = self.doorGroup.findChildren(QRadioButton)
        if buttons[0].isChecked():
            senses.append(1)
        else:
            if buttons[1].isChecked():
                senses.append(0)
            else:
                senses.append(2)

        buttons = self.airGroup.findChildren(QRadioButton)
        if buttons[0].isChecked():
            senses.append(1)
        else:
            if buttons[1].isChecked():
                senses.append(0)
            else:
                senses.append(2)

        buttons = self.greaseGroup.findChildren(QRadioButton)
        if buttons[0].isChecked():
            senses.append(1)
        else:
            if buttons[1].isChecked():
                senses.append(0)
            else:
                senses.append(2)

        buttons = self.startGroup.findChildren(QRadioButton)
        if buttons[0].isChecked():
            senses.append(1)
        else:
            if buttons[1].isChecked():
                senses.append(0)
            else:
                senses.append(2)

        inputNames = ["InverterActiveLow","StopActiveLow","DoorActiveLow","AirActiveLow","GreaseActiveLow","StartActiveLow"]
        for i in range(0,6):
            if self.cnc.inputs[i].sense != senses[i]:
                tmps = "config.inputs."+inputNames[i]+" "+str(senses[i])
                print("Change input: "+tmps)
                param = "config.inputs."+inputNames[i]
                value = str(senses[i])
                self.cnc.saveConfig(param, value)
            
        self.close()

class dlgSAT(QDialog):
    def __init__(self, cnc, parent=None):
        super(dlgSAT, self).__init__(parent)

        self.cnc = cnc

        self.lang = cLanguage()
        
        # Create widgets
        self.setFont(QFont('SansSerif', 16))

        btnTunning = borderLessButton(self.lang.tr("motor tunning"), "iconMotorTunning.png")
        btnTunning.clicked.connect(self.showTunning)
        
        btnHome = borderLessButton(self.lang.tr("home config"), "iconHomeConfig.png")
        btnHome.clicked.connect(self.showHome)
        
        btnInput = borderLessButton(self.lang.tr("input config"), "iconInputConfig.png")
        btnInput.clicked.connect(self.showInputConfig)
        
        btnOutput = borderLessButton( self.lang.tr("output config"), "iconOutputConfig.png")
        btnOutput.clicked.connect( self.showOutputConfig )

        btnGralParams = borderLessButton( self.lang.tr("gral. params"), "iconGralParams.png")
        btnGralParams.clicked.connect( self.showGralParams )
        
        btnConfigRead = borderLessButton( self.lang.tr("config. read"), "iconReadConfig.png")
        btnConfigRead.clicked.connect(self.handleConfigRead)
        
        btnConfigWrite = borderLessButton( self.lang.tr("config. write"), "iconWriteConfig.png")
        btnConfigWrite.clicked.connect(self.handleConfigWrite)

        btnFactory = borderLessButton( self.lang.tr("factory def."), "btnFactDefaults.png")
        btnFactory.clicked.connect(self.handleFactory)

        btnClose = borderLessButton( self.lang.tr("close"), "btnJogLSlow.png")
        btnClose.clicked.connect( self.handleClose )
        
        grid = QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(btnTunning, 0, 0)
        grid.addWidget(btnHome, 0, 1)
        grid.addWidget(btnInput, 0, 2)
        grid.addWidget(btnOutput, 0, 3)
        grid.addWidget(btnGralParams, 1, 0)
        grid.addWidget(btnConfigRead, 1, 1)
        grid.addWidget(btnConfigWrite, 1, 2)
        grid.addWidget(btnFactory, 1, 3)
        grid.addWidget(btnClose, 2, 0)

        self.setLayout(grid)
        if develPlatform() == True:
            self.setGeometry(50, 50, screenWidth, screenHeight)
        else:
            self.setGeometry(0, 0, screenWidth, screenHeight)

        self.setStyleSheet("QDialog {background-color: #232234;}")

    def handleFactory(self):

        # rev20180624: Que pida confirmación antes de pasar a defaults
        # TODO: Dice Victor que esto lo jode todo
        '''
        msgBox = QMessageBox()
        msgBox.setInformativeText(self.lang.tr("Do you really want to revert configuration to factory defaults?"))
        msgBox.setStandardButtons( QMessageBox.Yes | QMessageBox.No )
        msgBox.setDefaultButton( QMessageBox.No )
        ret = msgBox.exec_()
        '''

        passwordOk = False
                
        userInfo = QMessageBox.question(self,"STARBORE","<font color='#ffffff'>"+self.lang.tr("Do you really want to revert configuration to factory defaults?"),QMessageBox.Yes | QMessageBox.No)

        if userInfo == QMessageBox.Yes:

            if getSettingsPassword() != "No":
                dialog = dlgInputNumber(pos=(290,50))
                dialog.show()
                dialog.exec_()

                if dialog.strValue == getSettingsPassword():
                    passwordOk = True
            else:
                passwordOk = True

            if passwordOk:
            
                print("resetting")
                self.cnc.saveConfig("config.system.Mark", "0")
                self.cnc.send("reset\r")
                self.cnc.blockSend()

            else:
                userInfo = QMessageBox.question(self,"STARBORE","<font color='#ffffff'>"+self.lang.tr("Password error."),QMessageBox.Ok)
        
    def handleConfigRead(self):
        from os import listdir
        from os.path import isfile, join

        passwordOk = False
        
        if getSettingsPassword() != "No":
            dialog = dlgInputNumber(pos=(290,50))
            dialog.show()
            dialog.exec_()

            if dialog.strValue == getSettingsPassword():
                passwordOk = True
        else:
            passwordOk = True

        if passwordOk == False:
            userInfo = QMessageBox.question(self,"STARBORE","<font color='#ffffff'>"+self.lang.tr("Password error."),QMessageBox.Ok)
            return
        
        config_found = 0
        
        if develPlatform() == True:
            for f in listdir("."):
                if f.endswith("config.txt"):
                    infile = open("config.txt","r")
                    config_found = 1
        else:
            for d in listdir("/media/pi/"):
                for f in listdir("/media/pi/"+d):
                    if f.endswith("config.txt"):
                        infile = open("/media/pi/"+d+"/config.txt","r")
                        config_found = 1

        if config_found == 1:
            try:
                for line in infile:
                    #fields = line.split(" = ")
                    #self.cnc.saveConfig(fields[0], fields[1])
                    fields = line.split(" = ")
                    if "." in fields[1]:
                        self.cnc.saveConfig(fields[0], float(fields[1]))
                    else:
                        if "True" in fields[1]:
                            self.cnc.saveConfig(fields[0], 1)
                        else:
                            if "False" in fields[1]:
                                self.cnc.saveConfig(fields[0], 0)
                            else:
                                self.cnc.saveConfig(fields[0], int(fields[1]))
            
            except:
                userInfo = QMessageBox.question(self,"STARBORE","<font color='#ffffff'>"+self.lang.tr("Error reading configuration file."),QMessageBox.Ok)
                return

            userInfo = QMessageBox.question(self,"STARBORE","<font color='#ffffff'>"+self.lang.tr("Configuration read OK."),QMessageBox.Ok)
        else:
            userInfo = QMessageBox.question(self,"STARBORE","<font color='#ffffff'>"+self.lang.tr("Configuration file not found."),QMessageBox.Ok)
            
    def handleConfigWrite(self):
        # generamos un archivo config.txt con los datos de config
        # y luego lo copiamos al usb

        # rev20180620: Si no se entraba a ninguna pantalla de config
        # no se leía del cnc y se grababan valores incorrectos
        self.cnc.readConfig()   
        
        if develPlatform() == True:
            outfile = open("config.txt","w")
        else:

            usb_encontrado = 0
            
            from os import stat
            from pwd import getpwuid

            for d in listdir("/media/pi/"):
                if getpwuid(stat("/media/pi/"+d).st_uid).pw_name == 'pi':
                    outfile = open("/media/pi/"+d+"/config.txt","w")
                    usb_encontrado = 1

            if usb_encontrado == 0:
                userInfo = QMessageBox.question(self,"STARBORE","<font color='#ffffff'>"+self.lang.tr("USB Not found. Unable to save config to the USB device."),QMessageBox.Ok)
                return

        try:
            axn = 0
            # ejes
            for ax in self.cnc.axis:
                outfile.write("config.axis["+str(axn)+"].StepsByUnit = "+str(ax.resolution)+"\n")
                outfile.write("config.axis["+str(axn)+"].Speed = "+str(ax.maxSpeed)+"\n")
                outfile.write("config.axis["+str(axn)+"].Acceleration = "+str(ax.acceleration)+"\n")
                outfile.write("config.axis["+str(axn)+"].PulseWidth = "+str(ax.pulseWidth)+"\n")
                outfile.write("config.axis["+str(axn)+"].DirectionWidth = "+str(ax.pulseWidth)+"\n")
                outfile.write("config.axis["+str(axn)+"].HomePosition = "+str(ax.homePos)+"\n")
                outfile.write("config.axis["+str(axn)+"].Linial = "+str(ax.linear)+"\n")
                outfile.write("config.axis["+str(axn)+"].HomeSpeed = "+str(ax.homeSpeed)+"\n")
                outfile.write("config.axis["+str(axn)+"].HomeDir = "+str(ax.homeDir)+"\n")
                outfile.write("config.axis["+str(axn)+"].JogSlowSpeed = "+str(ax.jogSlowSpeed)+"\n")
                outfile.write("config.axis["+str(axn)+"].JogFastSpeed = "+str(ax.jogFastSpeed)+"\n")
                outfile.write("config.axis["+str(axn)+"].StepActiveLow = "+str(ax.stepOutput.sense)+"\n")
                outfile.write("config.axis["+str(axn)+"].DirActiveLow = "+str(ax.dirOutput.sense)+"\n")
                outfile.write("config.axis["+str(axn)+"].HomeActiveLow = "+str(ax.homeSensor.sense)+"\n")
                outfile.write("config.axis["+str(axn)+"].Encoder = "+str(ax.encoder)+"\n")
                axn += 1

            # Entradas
            outfile.write("config.inputs.InverterActiveLow = "+str(self.cnc.inputs[0].sense)+"\n")
            outfile.write("config.inputs.StopActiveLow = "+str(self.cnc.inputs[1].sense)+"\n")
            outfile.write("config.inputs.DoorActiveLow = "+str(self.cnc.inputs[2].sense)+"\n")
            outfile.write("config.inputs.AirActiveLow = "+str(self.cnc.inputs[3].sense)+"\n")
            outfile.write("config.inputs.GreaseActiveLow = "+str(self.cnc.inputs[4].sense)+"\n")
            outfile.write("config.inputs.StartActiveLow = "+str(self.cnc.inputs[5].sense)+"\n")
            

            # Salidas
            outfile.write("config.outputs.ClipActiveLow = "+str(self.cnc.outputs[0].sense)+"\n")
            outfile.write("config.outputs.ClampActiveLow = "+str(self.cnc.outputs[1].sense)+"\n")
            outfile.write("config.outputs.DrillActiveLow = "+str(self.cnc.outputs[2].sense)+"\n")
            outfile.write("config.outputs.spireDelay = "+str(self.cnc.spireDelay)+"\n")
            outfile.write("config.outputs.spireEnabled = "+str(self.cnc.spireEnabled)+"\n")
            outfile.write("config.outputs.DrillDelay = "+str(int(10*self.cnc.drillDelay))+"\n")
            
            # Sistema
            outfile.write("config.system.ArcSysFactor = "+str(self.cnc.arcSysFactor)+"\n")
            outfile.write("config.system.LedRef = "+str(self.cnc.ledRef)+"\n")
            #outfile.write("config.system.Mark = "+str(self.cnc.mark)+"\n")

            # Encoder
            outfile.write("config.EncoderTimeout = "+str(self.cnc.encoderTimeout)+"\n")
            outfile.write("config.EncoderError = "+str(self.cnc.encoderError)+"\n")

            # Autogrease
            outfile.write("config.autogreaseMinutes = "+str(self.cnc.autogreaseMinutes)+"\n")
            outfile.write("config.autogreaseSeconds = "+str(self.cnc.autogreaseSeconds)+"\n")
        except:
            raise
            userInfo = QMessageBox.question(self,"STARBORE","<font color='#ffffff'>"+self.lang.tr("Error while writing configuration file."),QMessageBox.Ok)
            return

        # Si hemos llegado hasta aquí todo está OK
        userInfo = QMessageBox.question(self,"STARBORE","<font color='#ffffff'>"+self.lang.tr("Configuration written to file config.txt."),QMessageBox.Ok)
        
        
    def handleClose(self):
        self.cnc.blockSend()    # Bloqueamos las peticiones al cnc para que no se bloquee
        self.cnc.send("reset\r")
        self.close()
        
    def showGralParams(self):
        dialog = dlgGralParams(self.cnc)
        if develPlatform() == True:
            dialog.show()
        else:
            dialog.showFullScreen()
        dialog.exec_()
        
    def showOutputConfig(self):
        dialog = dlgOutputConfig(self.cnc)
        if develPlatform() == True:
            dialog.show()
        else:
            dialog.showFullScreen()
            
        dialog.exec_()
        
    def showInputConfig(self):
        dialog = dlgInputConfig(self.cnc)
        if develPlatform() == True:
            dialog.show()
        else:
            dialog.showFullScreen()
            
        dialog.exec_()
        
    def showTunning(self):
        dialog = dlgMotorTunning(self.cnc)
        if develPlatform() == True:
            dialog.show()
        else:
            dialog.showFullScreen()
            
        dialog.exec_()

    def showHome(self):
        dialog = dlgHomeConfig(self.cnc)
        if develPlatform() == True:
            dialog.show()
        else:
            dialog.showFullScreen()
            
        dialog.exec_()

                
class dlgMaint(QDialog):
        
    def __init__(self, cnc, parent=None):
        super(dlgMaint, self).__init__(parent)
        # Control de com
        self.cnc = cnc
        cnc.printStatus()

        self.lang = cLanguage()
        
        # Create widgets
        self.setFont(QFont('SansSerif', 16))

        self.setStyleSheet("QDialog {background-color: #232234;color:#ffffff;}")
        
        #btnTools = QPushButton("TOOLS")
        btnTools = borderLessButton( self.lang.tr("tools"), "iconTools.png")
        btnTools.clicked.connect(self.showTools)
        
        btnInputTest = borderLessButton( self.lang.tr("input test"), "iconInputTest.png")
        btnInputTest.clicked.connect(self.showInputTest)

        btnOutputTest = borderLessButton( self.lang.tr("output test"), "iconOutputTest.png")
        btnOutputTest.clicked.connect(self.showOutputTest)
        
        btnSettings = borderLessButton( self.lang.tr("settings"), "iconSettings.png")
        btnSettings.clicked.connect(self.handleSettings)
        
        btnInfo = borderLessButton( self.lang.tr("info"), "iconInfo.png")
        btnInfo.clicked.connect(self.showInfo)
        
        btnLicense = borderLessButton("license", "iconLicense.png")
        
        btnEscape = borderLessButton( self.lang.tr("close"), "btnJogLSlow.png")
        
        # Create layout and add widgets
        grid = QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(btnTools, 0, 0)
        grid.addWidget(btnInputTest, 0, 1)
        grid.addWidget(btnOutputTest, 0, 2)
        #grid.addWidget(btnGrease, 1, 0)
        grid.addWidget(btnInfo, 1, 1)
        grid.addWidget(btnSettings, 1, 0)
        grid.addWidget(btnEscape, 2, 0)
        # Set dialog layout
        self.setLayout(grid)
        # Add button signal to greetings slot
        btnEscape.clicked.connect(self.escape)
        
        if develPlatform() == True:
            self.setGeometry(50, 50, screenWidth, screenHeight)
        else:
            self.setGeometry(0,0, screenWidth, screenHeight)

        # vars
        self.filename = ""

    # Greets the user
    def escape(self):
        self.close()

    def handleSettings(self):

        showSettings = False
        
        if getSettingsPassword() != "No":
            dialog = dlgInputNumber(pos=(290,50))
            dialog.show()
            dialog.exec_()

            if dialog.strValue == getSettingsPassword():
                showSettings = True
            else:
                userInfo = QMessageBox.question(self,"STARBORE","<font color='#ffffff'>"+self.lang.tr("Password error."),QMessageBox.Ok)
        else:
            showSettings=True

        if showSettings:
            dialog = dlgSAT(self.cnc)
            if develPlatform() == True:
                dialog.show()
            else:
                dialog.showFullScreen()
                        
            dialog.exec_()
        
    def showInputTest(self):
        dialog = dlgInputTest(self.cnc)
        
        if develPlatform() == True:
            dialog.show()
        else:
            dialog.showFullScreen()
            
        dialog.exec_()

    def showOutputTest(self):
        dialog = dlgOutputTest(self.cnc)
        if develPlatform() == True:
            dialog.show()
        else:
            dialog.showFullScreen()
            
        dialog.exec_()

        dialog.refreshTimer.stop()
        
    def showJog(self):
        
        # rev20180319: Si está activa la alarma de emergencia no dejamos hacer nada
        if self.cnc.alarmStop == True:
            userInfo = QMessageBox.question(self,"STARBORE", self.lang.tr("STOP alarm active."),QMessageBox.Ok)
            return
        
        dialog = dlgJog( self.cnc )
        #dialog = dlgInputTest()
        if develPlatform() == True:
            dialog.show()
        else:
            dialog.showFullScreen()

        dialog.exec_()
            
    def showTools(self):
        # rev20180319: Si está activa la alarma de emergencia no dejamos hacer nada
        if self.cnc.alarmStop == True:
            userInfo = QMessageBox.question(self,"STARBORE", "<font color='#ffffff'>"+self.lang.tr("STOP alarm active."),QMessageBox.Ok)
            return
        
        dialog = dlgTools(self.cnc)
        if develPlatform() == True:
            dialog.show()
        else:
            dialog.showFullScreen()
            
        dialog.exec_()

    def showSAT(self):
        dialog = dlgSAT(self.cnc)
        if develPlatform() == True:
            dialog.show()
        else:
            dialog.showFullScreen()
            
        dialog.exec_()
                    
        dialog.exec_()

    def openFile(self):
        self.fileName = QFileDialog.getOpenFileName(self, "Open Files", ".", "tap files(*.tap)")
        self.close()

    def showInfo(self):
        dialog = dlgInfo(self.cnc)
        if develPlatform() == True:
            dialog.show()
        else:
            dialog.showFullScreen()
                    
        dialog.exec_()

    def showGrease(self):
        dialog = dlgGrease()
        if develPlatform() == True:
            dialog.show()
        else:
            dialog.showFullScreen()
                    
        dialog.exec_()

class dlgFileContents(QDialog):
    def __init__(self, parent=None):
        super(dlgFileContents, self).__init__(parent)
        # Create widgets
        self.setFont(QFont('SansSerif', 16))

        self.textBox = QTextEdit(self)
        self.textBox.setReadOnly(True)
        btnClose = QPushButton("CLOSE")
        btnClose.clicked.connect(self.close)

        grid = QGridLayout()
        grid.setSpacing(40)
        grid.addWidget(self.textBox, 0, 0)
        grid.addWidget(btnClose, 1, 0)

        self.setLayout(grid)

        if develPlatform() == True:
            self.setGeometry(50, 50, screenWidth, screenHeight)
        else:
            self.setGeometry(0,0, screenWidth, screenHeight)

    def setContent(self, cont):
        self.textBox.setText(cont)


class dlgErrors(QDialog):
    def __init__(self, cnc, parent=None):
        super(dlgErrors, self).__init__(parent)

        # Control coms con equipo
        self.cnc = cnc

        self.lang = cLanguage()
                                            
        self.errorList = self.cnc.getErrors()
        self.firstLine = 0

        self.setStyleSheet("QDialog {background-color: #232234;color:#ffffff;}")

        self.lblErrors = QLabel("")
        self.lblErrors.setStyleSheet(labelStyle)

        self.btnClear = borderLessButton(self.lang.tr("clear"),"iconOk.png")
        self.btnClear.clicked.connect(self.handleClear)
        
        self.btnAlarms = borderLessButton(self.lang.tr("alarms"),"iconAlarms.png")
        self.btnAlarms.clicked.connect( self.close )
        #self.errorList = []
        #for i in range(40):
        #    self.errorList.append("Test error line "+str(i+1)+"\r\n")
            
        if not self.errorList is None:
            print("Error list:"+str(self.errorList))
            # Si hay más de 20 errores mostramos los 20 seleccionados
            errorWindow = []
            if len(self.errorList) > 15:
                for i in range(self.firstLine, self.firstLine+15):
                    if not "Error list" in self.errorList[i] and not "Error list end" in self.errorList[i]:
                        errorWindow.append(self.errorList[i])
            else:
                for line in self.errorList:
                    if not "Error list" in line and not "Error list end" in line:
                        errorWindow.append(line)

            if len(errorWindow) > 0:        
                tmps = ""
                idx = 1
                for line in errorWindow:
                    tmps += str(idx)+": "+line
                    idx += 1
            else:
                tmps = self.lang.tr("No errors found.")
            
        else:
            tmps = self.lang.tr("No errors found.")

        self.lblErrors.setText(tmps)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.lblErrors, 0, 0)
        grid.addWidget(self.btnClear, 1, 1)
        grid.addWidget(self.btnAlarms, 1, 0)
        
        self.setLayout(grid)

        if develPlatform() == True:
            self.setGeometry(50, 50, screenWidth, screenHeight)
        else:
            self.setGeometry(0,0, screenWidth, screenHeight)

    def refreshErrorList(self):
            
        if not self.errorList is None:
            # Si hay más de 20 errores mostramos los 20 seleccionados
            errorWindow = []
            if len(self.errorList) > 15:
                try:
                    for i in range(self.firstLine, self.firstLine+15):
                        if not "Error list" in self.errorList[i] and not "Error list end" in self.errorList[i]:
                            errorWindow.append(self.errorList[i])
                except IndexError:
                    print("Fin buffer")
            else:
                for line in self.errorList:
                    if not "Error list" in line and not "Error list end" in line:
                        errorWindow.append(line)
                    
            tmps = ""
            idx = self.firstLine
            for line in errorWindow:
                tmps += str(idx+1)+": "+line
                idx += 1
            
        else:
            tmps = self.lang.tr("No errors found.")

        self.lblErrors.setText(tmps)

    def handleClear(self):
        self.cnc.send(b"clear e\r")
        self.lblErrors.setText(self.lang.tr("No errors found."))
        
    def mousePressEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        siz = self.lblErrors.size()

        if pos.x() > 190 and pos.x() < 350:
            if pos.y() > 22 and pos.y() < 341:
                print("pos x:"+str(pos.x())+" y:"+str(pos.y()))

                if pos.y() < 180:
                    if self.firstLine > 15:
                        self.firstLine -= 15
                    else:
                        self.firstLine = 0
                else:
                    self.firstLine += 15

                print("First line:"+str(self.firstLine))

                self.refreshErrorList()

        
# Implementación de la Vista Alarmas

class dlgAlarms(QDialog):
    def __init__(self, cnc, parent=None):
        super(dlgAlarms, self).__init__(parent)

        # Control coms con equipo
        self.cnc = cnc
        self.cnc.readStatus()

        self.lang = cLanguage()
                                            
        # Timer para actualizar el estado de las entradas
        self.refreshTimer = QTimer(self)
        self.connect(self.refreshTimer, SIGNAL("timeout()"), self.refresh)
        self.refreshTimer.start(1000)
        
        # Create widgets
        self.setFont(QFont('SansSerif', 16))

        self.setStyleSheet("QDialog {background-color: #232234;color:#ffffff;}")

        # Definicion de los Botones de la vista utlizando los textos del
        # fichero de traducción lang.txt en la raiz del proyecto (En total 12 botones)
        # COmenzando desde botón aire hasta botón confirmar

        self.btnAir = borderLessButton(self.lang.tr("air"),"iconAir.png")
        self.btnInverter = borderLessButton( self.lang.tr("inverter"),"iconInputInverter.png")
        self.btnDoor = borderLessButton( self.lang.tr("door"), "iconInputDoor.png")
        #self.btnGrease = borderLessButton( self.lang.tr("header lock"), "iconOutSpindle.png")
        self.btnEmergency = borderLessButton( self.lang.tr("emergency"), "iconInputEmergency.png")
        # rev20171107: Alarmas que faltan
        self.btnLimits = borderLessButton( self.lang.tr("limits"), "iconAlarmLimits.png")
        self.btnExec = borderLessButton( self.lang.tr("execution"),"iconAlarmExec.png")
        self.btnSyntax = borderLessButton( self.lang.tr("syntax"),"iconAlarmSyntax.png")
        self.btnEncoder = borderLessButton( self.lang.tr("encoder"),"iconAlarmEncoder.png")

        # rev20171227: Lista de errores
        # para estos tres último botones se define ademas
        self.btnErrors = borderLessButton( self.lang.tr("errors"), "iconErr.png")
        self.btnErrors.clicked.connect(self.showErrors)
        
        self.btnConfirm = borderLessButton( self.lang.tr("confirm"), "iconOk.png")
        self.btnConfirm.clicked.connect(self.handleClear)

        btnClose = borderLessButton( self.lang.tr("close"), "btnJogLSlow.png")
        btnClose.clicked.connect(self.close)

        # Fin de la declaración de Botones de la vista Alarmas

        '''
        self.AlarmsBox = QTextEdit(self)
        self.AlarmsBox.setReadOnly(True)
        self.AlarmsBox.setText("EMERGENCIA\nUSUARIO")

        self.WarningBox = QTextEdit(self)
        self.WarningBox.setReadOnly(True)
        self.WarningBox.setText("EMERGENCIA\nUSUARIO")
        '''

        # Ahora se procede a establecer la posición de los botones
        # Utilizando una Grilla y acomodando los botones en filas y columnas

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.btnAir, 0, 0)
        grid.addWidget(self.btnInverter, 0, 1)
        grid.addWidget(self.btnDoor, 0, 2)
        #grid.addWidget(self.btnGrease, 0, 3)
        grid.addWidget(self.btnEmergency, 0, 3)

        grid.addWidget(self.btnLimits, 1, 0)
        grid.addWidget(self.btnExec, 1, 1)
        grid.addWidget(self.btnSyntax, 1, 2)
        grid.addWidget(self.btnEncoder, 1, 3)
        
        grid.addWidget(btnClose, 2, 0)
        grid.addWidget(self.btnConfirm, 2, 4)

        grid.addWidget(self.btnErrors, 2, 2)
        
        self.setLayout(grid)

        # Fin del posicionamiento de los botones en la vista

        if develPlatform() == True:
            self.setGeometry(50, 50, screenWidth, screenHeight)
        else:
            self.setGeometry(0,0, screenWidth, screenHeight)

        self.refresh()

    def showErrors(self):
        dialog = dlgErrors(self.cnc)
        if develPlatform() == True:
            dialog.show()
        else:
            dialog.showFullScreen()
                    
        dialog.exec_()
        
    def handleClear(self):
        self.cnc.send(b"clear a\r")
        
    def refresh(self):
        self.cnc.readStatus()
        #self.cnc.printStatus()
            
        if self.cnc.alarmStop == 1:
            self.btnEmergency.setIcon(QPixmap("iconAlarmEmergencyOn.png"))
        else:
            self.btnEmergency.setIcon(QPixmap("iconInputEmergency.png"))

        if self.cnc.alarmDoor == 1:
            self.btnDoor.setIcon( QPixmap("iconAlarmDoorOn.png") )
        else:
            self.btnDoor.setIcon( QPixmap("iconInputDoor.png") )
            
        if self.cnc.alarmAir == 1:
            self.btnAir.setIcon(QPixmap("iconAlarmAirOn.png"))
        else:
            self.btnAir.setIcon(QPixmap("iconAir.png"))

        #if self.cnc.alarmGrease == 1:
            #self.btnGrease.setIcon(QPixmap("iconAlarmHeaderLockOn.png"))
       # else:
            #self.btnGrease.setIcon(QPixmap("iconOutSpindle.png"))

        if self.cnc.alarmLimits == 1:
            self.btnLimits.setIcon( QPixmap("iconAlarmLimitsOn.png") )
        else:
            self.btnLimits.setIcon( QPixmap("iconAlarmLimits.png") )

        if self.cnc.alarmEncoder == 1:
            self.btnEncoder.setIcon( QPixmap("iconAlarmEncoderOn.png") )
        else:
            self.btnEncoder.setIcon( QPixmap("iconAlarmEncoder.png") )

        if self.cnc.alarmParser == 1:
            self.btnSyntax.setIcon(QPixmap("iconAlarmSyntaxOn.png"))
        else:
            self.btnSyntax.setIcon(QPixmap("iconAlarmSyntax.png"))
            
        if self.cnc.alarmExec == 1:
            self.btnExec.setIcon(QPixmap("iconAlarmExecOn.png"))
        else:
            self.btnExec.setIcon(QPixmap("iconAlarmExec.png"))

        if self.cnc.alarmInverter == 1:
            self.btnInverter.setIcon( QPixmap("iconAlarmInverterOn.png") )
        else:
            self.btnInverter.setIcon( QPixmap("iconInputInverter.png") )
            

def createVBox(items):
        vbox = QVBoxLayout()
        for w in items:
            vbox.addWidget(w)

        return vbox

def createHBox(items):
        hbox = QHBoxLayout()
        for w in items:
            hbox.addWidget(w)

        return hbox

def parseMrkEdge(line):
    mrkEdge = []

    sNumbers = line[line.find("=")+1:line.find(")")]

    if len(sNumbers) == 4:
        for i in range(len(sNumbers)):
            if sNumbers[i] == "1":
                mrkEdge.append(True)
            else:
                mrkEdge.append(False)
    else:
        mrkEdge = [False, False, False, False]

    return mrkEdge


class MainWindow(QMainWindow):
    refreshSignal = Signal()
    
    def __init__(self, cnc):
        super(MainWindow, self).__init__()

        # rev20170728: control del cnc
        self.cnc = cnc
        self.ctrlFile = controlFile()
        self.ctrlFile.readFile()

        # rev20190502: Marcar los cantos a trabajar
        self.STUB_CANTOS = "CANTOS"

        self.DIR_LEFT_DELIMETER = "["
        self.DIR_RIGHT_DELIMETER = "]"

        if develPlatform():
            self.LOCAL_PATH = "."
        else:
            self.LOCAL_PATH = "/media/pi"

        # res20180121
        self.remotePath = "/cncNetwork/"
        self.REMOTE_PATH = "/cncNetwork/"

        with open("cfg.txt") as f:
            cfg = f.readlines()

        for line in cfg:
            if "remoteDir:" in line:
                fields = line.split(":")
                self.REMOTE_PATH = fields[1]

            if "localDir:" in line:
                fields = line.split(":")
                self.LOCAL_PATH = fields[1]

        self.currentRemoteDir = self.REMOTE_PATH
        self.currentLocalDir = self.LOCAL_PATH

        # rev20180321: MUltiidioma
        self.lang = cLanguage()

        # rev20180704: Control sense de la fresa
        if getFresaActiveLow() == 1:
            self.cnc.send("exec M502\r\n")
        self.initGui()

        self.setStyleSheet("QMainWindow {background-color: #232234;color:#ffffff;}")
        # rev20170630: Datos de la app
        self.tapFile = ""
        self.dimensions = [0, 0, 0]

        # rev20170928: Estado del proceso
        self.running = False
        self.expectedPage = 0
        self.executingLine = 0

        self.stopCnt = 0


        if getDefaultCyclesOn() == 0:
            self.cyclesOn = False
            self.btnCiclos.setIcon( QPixmap("iconFile.png") )
            self.lblCycles.setVisible(False)
        else:
            self.cyclesOn = True
            self.btnCiclos.setIcon( QPixmap("iconFile.png") )
            self.lblCycles.setVisible(True)
            


        # rev20180622: Para mostrar el tiempo de ejecución del último tap
        self.executingTime = ""

        # contador refresco usb
        self.cntUSB = 0

        # Veamos si hemos encontrado el cnc
        if self.cnc.port == 0:
            # Ups no lo hemos encontrado
            userInfo = QMessageBox.information(self,"STARBORE",self.lang.tr("Unable to connect with CNC. Please verify connection and power on CNC."),QMessageBox.Ok)
            # copdebug: Simulamos la emergencia de STOP para pruebas
            #self.cnc.alarmStop = True
        
        self.timer = QTimer(self)
        self.timer.setInterval(300) # 1500
        self.timer.timeout.connect(self.com)
        self.timer.start()

        #rev20180203: Añadimos miembro para guardar nombre del archivo y mostrarlo en status
        self.fname = ""
        self.xdim = ""
        self.ydim = ""
        self.zdim = ""

        # rev20180225: Proceso de teclao para lector código de barras
        self.installEventFilter( self )
        self.receivedBarcode = ""

        # rev20190502: Marcar los cantos a trabajar
        self.mrkEdge = [False, False, False, False]

        # Modificacion 20190903 23.54
        # Código modificado por krlossrs@gmail.com
        self.content = []

    def eventFilter( self, widget, event):

        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter or event.key() == 10 or event.key() == 13:
                # El return es final de nombre de archivo

                print "Código de barras leído es: " + self.receivedBarcode

                # rev20180227: Filtramos el barcode, algunos vendran como 9>nombre_archivo_sin.tao, otros como 0:nombre y otros sólo nombre
                if ":" in self.receivedBarcode:
                    fname = self.receivedBarcode.split(":")[1].lower()
                else:
                    if ">" in self.receivedBarcode:
                        fname = self.receivedBarcode.split(">")[1].lower()
                    else:
                        fname = self.receivedBarcode.lower()

                fname2 = fname + ".TAP"
                fname += ".tap"

                self.receivedBarcode = ""
                print("Archivo: " + fname)

                # rev20180506: Segun si estamos en usb o red escogemos una lista de archivos u otra
                if self.fileStatus == 0:
                    fileList = self.getFileList()
                else:
                    fileList = self.getRemoteFiles()

                for f in fileList:
                    if fname in f.lower() or fname2 in f.lower():

                        print("File found:" + fname)
                        fname = f

                        if self.fileStatus == 0:
                            fname = os.path.join(self.currentLocalDir, fname)
                        else:
                            fname = os.path.join(self.currentRemoteDir, fname)

                        # self.fileStatus = 1
                        # self.btnFile.setIcon(self.iconFile)

                        with open(fname) as f:
                            # self.content = f.readlines()
                            contents = f.readlines()

                        self.content = []
                        self.mrkEdge = [False, False, False, False]
                        for line in contents:
                            if len(line) > 2 and not "(" in line:
                                # rev20181114: Eliminamos los tabuladores
                                line = line.replace('\t', '')
                                # rev20190617: Eliminamos espacios duplicados
                                line = re.sub(' +', ' ', line)
                                self.content.append(line)

                            # rev20190502: Marcar los cantos a trabajar
                            if self.STUB_CANTOS in line:
                                self.mrkEdge = parseMrkEdge(line)
                                print("eventFilter: ")
                                print(self.mrkEdge)

                            # rev20180203: Extraemos las dimensiones
                            # En linux sale el ), en windows es :-2
                            if "PIEZA_" in line:
                                print(line)
                                if "PIEZA_DX" in line:
                                    self.xdim = line.split("=")[1].split(")")[0]
                                if "PIEZA_DY" in line:
                                    self.ydim = line.split("=")[1].split(")")[0]
                                if "PIEZA_DZ" in line:
                                    self.zdim = line.split("=")[1].split(")")[0]

                        # rev20180630: Cuando tenemos las dimensiones
                        dialog2 = dlgDimensions([self.xdim, self.ydim, self.zdim], self.mrkEdge, fname)
                        if develPlatform() == True:
                            dialog2.show()
                        else:
                            dialog2.showFullScreen()
                        dialog2.exec_()

                        if dialog2.closedOk != True:
                            return QWidget.eventFilter(self, widget, event)

                        # rev20190724 Solucionar actualización de fichero abierto
                        self.fname = fname

                        self.lblFiles.setTextInteractionFlags(Qt.TextSelectableByKeyboard)

                        self.fromLine = 0
                        self.refreshFileText2()  # copdebug

                        self.lv.setVisible(False)
                        self.lvNetwork.setVisible(False)
                        self.lblFiles.setVisible(True)
                        self.btnFile.setText(self.lang.tr("contents"))
                        self.lv.setVisible(False)

                        self.btnStart.setEnabled(True)
                        self.btnStart.setIcon(QPixmap("iconStart.png"))

                        # rev20180504: Si estan activados los ciclos,
                        # cada vez que se lea un código hay que preguntar el nº de piezas
                        if self.cyclesOn == True:
                            dialog = dlgInputNumber(pos=(290, 50), widg=self.lblCycles)
                            dialog.show()
                            dialog.exec_()

                            self.totalCiclos = int(self.lblCycles.text())
                            self.ciclosRealizados = 0
                            self.lblCycles.setText("cycles\n0/" + str(self.totalCiclos))
                    else:
                        print "Comparando : " + f.lower() + " con " + fname

            else:
                try:
                    self.receivedBarcode += chr(event.key())
                    print("Key press ") + str(event.key())
                    print("barcode:" + str(self.receivedBarcode))
                except:
                    print("unkown char")

            event.accept()

        return QWidget.eventFilter(self, widget, event)

    def mousePressEvent(self, QMouseEvent):
        #print QMouseEvent.pos()
        #print("label:"+str(self.lblFiles.x())+","+str(self.lblFiles.y()))
        pos = QMouseEvent.pos()
        siz = self.lblFiles.size()
        #print("size:"+str(siz))
        #if pos.x > self.lblFiles.x() and pos.x < self.lblFiles.x()+siz.width():
        #print("pos x:"+str(pos.x())+" y:"+str(pos.y()))
        if pos.x() >400 and pos.x() < 687:
            if pos.y() > 88 and pos.y() < 316:
                if pos.y() < 202:
                    if self.fromLine > 10:
                        self.fromLine -= 10
                    else:
                        self.fromLine = 0
                else:
                    self.fromLine += 10

                self.refreshFileText2()
        
    def com(self):

        if self.cnc.blocked() == True:
            return
            
        if self.running == False:
            self.cnc.readStatus()
            if self.cnc.inputs[5].state == 1:
                # rev20180425: Si ya estamos ejecutando un programa ignoramos la entrada
                if self.running == False:
                    self.handleStart()
                
            if self.fname != "":
                fields = self.fname.split("/")
                fname = fields[len(fields)-1]
                self.statusBar().showMessage(self.lang.tr("Ready")+", "+self.lang.tr("curent file: ")+fname+", "+self.lang.tr("Dimension: ")+self.xdim+"x"+self.ydim+"x"+self.zdim + self.executingTime )
            else:
                self.statusBar().showMessage(self.lang.tr("Ready"))

            # rev20180506: cada segundo refrescamos info de los directorios de usb y remoto
            self.cntUSB += 1
            if self.cntUSB >= 3:
                self.refreshUSBdir()
                self.refreshNetworkDir()
                self.cntUSB = 0
            
        else:
            self.cnc.readStatus()

            if self.cnc.mode == 4:
                print("waiting4user...")
                userInfo = QMessageBox.question(self,"STARBORE", self.lang.tr("Turn piece and click OK."),QMessageBox.Ok)
                self.cnc.send("m1end\r")
                print("Piece turned...")

            # rev20181001: Los homes tb paran y el resto de alarmas tb
            if self.cnc.alarmLimits == 1:
                print("stopping limits...")
                self.handleStop()

            if self.cnc.alarmDoor == 1 or self.cnc.alarmAir == 1 or self.cnc.alarmInverter == 1 or self.cnc.alarmGrease == 1:
                #print("stopping door, air, inverter, grease...")
                self.handleStop()

            if self.cnc.alarmEncoder == 1 or self.cnc.alarmParser == 1 or self.cnc.alarmExec == 1:
                #print("stopping encoder, parser, exec...")
                self.handleStop()
                
                        # rev20180425: Si se pulsa emergencia paramos el programa
            if self.cnc.inputs[1].state == 1 or self.cnc.alarmStop == 1:
                print("stopping EMERG...")
                #self.handleStop()

            # Si se activa la alarma del spindle tb paramos
            if self.cnc.alarmExec == 1:
                print("stopping SPINDLE...")
                self.handleStop()
                
            # rev20180202: Añadimos a la status bar la info del archivo y del timpo de ejecución
            currTime = time.time() - self.startTime
            
            print("t:"+str(time.time())+", st:"+str(self.startTime)+", ct:"+str(currTime))

            hours = currTime / 3600

            # rev20180508: Quitar el path del nombre también en ejecución
            fields = self.fname.split("/")
            fname = fields[ len(fields) - 1 ]
            self.executingTime = ", Execution time: "+str(int(currTime / 3600)).zfill(2)+":"+str(int(currTime / 60)).zfill(2) +":"+str(int(currTime)%60).zfill(2)
            self.statusBar().showMessage("Executing file: " + fname + ", Dimension: "+self.xdim+"x"+self.ydim+"x"+self.zdim + self.executingTime )
            if len(self.tapPages) > self.cnc.expectedPage:
                self.cnc.send(b"addpage "+self.tapPages[self.cnc.expectedPage]+"\r")
                print("addpage:"+str(self.tapPages[self.cnc.expectedPage])+"total length:"+str(9+len(self.tapPages[self.cnc.expectedPage])))
                self.all_send = False
            else:
                self.all_send = True
                '''
                fdebug = open("debug.txt","a")
                fdebug.write("------ALL SENT!!--------\r")
                fdebug.close()
                '''

            '''
            print("stopcnt:"+str(self.stopCnt)+"mode:"+str(self.cnc.mode))
            fdebug = open("debug.txt","a")
            fdebug.write("stopcnt:"+str(self.stopCnt)+"mode:"+str(self.cnc.mode)+"\r")
            fdebug.close()
            '''

            if self.cnc.mode == 0:
                if self.all_send == True:
                    self.stopCnt += 1
                else:
                    self.stopCnt = 0

                if self.stopCnt > 15:
                    print(" --- STOP ---"+str(self.stopCnt))
                    self.running = False
                    #rev20190614: Aplicar un reset y un referenciar tras finalizar un TAP
                    print("Va a resetear y referenciar")
                    self.resetAndReference()
                    self.btnStart.setIcon(QPixmap("iconStart.png"))
                    # rev20180503: Cuando acaba el proceso, si estamo en modo
                    # ciclos hay que contar una pieza más
                    if self.cyclesOn == True:
                        self.ciclosRealizados += 1
                        self.lblCycles.setText("cycles\n"+str(self.ciclosRealizados)+"/"+str(self.totalCiclos))

                    self.btnJog.setIcon( QPixmap("iconJog.png") )
                    self.btnRef.setIcon( QPixmap("iconRef.png") )
                    self.btnAlarm.setIcon( QPixmap("iconAlarms.png") )
                    self.btnHelp.setIcon( QPixmap("iconHelp.png") )
                    self.btnQuit.setIcon( QPixmap("iconQuit.png") )
                    #rev20180508
                    #if self.cyclesOn == False:
                    self.btnCiclos.setIcon( QPixmap("iconFile.png") )
                    #else:
                        #self.btnCiclos.setIcon( QPixmap("iconCyclesOn.png") )
                    self.btnMant.setIcon( QPixmap("iconMaint.png") )

                    if self.fileStatus == 1:
                        self.btnFile.setIcon(self.iconNetwork)
                    else:
                        self.btnFile.setIcon(self.iconUSB)

                    
            else:
                self.stopCnt = 0

            self.executingLine = self.cnc.currentExecutionLine
            #print("Executing line:"+str(self.executingLine))
            self.refreshFileText()
            
        

        self.lblXpos.setText ( "{:6.2f}".format( self.cnc.axis[0].position ) + " mm")
        self.lblYpos.setText ( "{:6.2f}".format( self.cnc.axis[1].position ) + " mm")
        self.lblZpos.setText ( "{:6.2f}".format( self.cnc.axis[2].position ) + " mm")
        #self.lblApos.setText ( "{:6.2f}".format( self.cnc.axis[3].position ) + " º")

        # Entradas
        '''
        if self.cnc.axis[0].homeSensor.state == 1:
            self.xInput.setPixmap(QPixmap("iconX32On.png"))
        else:
            self.xInput.setPixmap(QPixmap("iconX32Off.png"))
        '''
        
        # Salidas
        if self.cnc.outputs[0].state == 1:
            self.fresaOutput.setPixmap(QPixmap("iconTool32On.png"))
        else:
            self.fresaOutput.setPixmap(QPixmap("iconTool32Off.png"))
            
        if self.cnc.outputs[2].state == 1:
            self.toolOutput.setPixmap(QPixmap("iconTool32On.png"))
        else:
            self.toolOutput.setPixmap(QPixmap("iconTool32Off.png"))

        if self.cnc.outputs[1].state == 1:
            self.pinzaOutput.setPixmap(QPixmap("iconPinza32On.png"))
        else:
            self.pinzaOutput.setPixmap(QPixmap("iconPinza32Off.png"))

        if self.cnc.outputs[3].state == 1:
            self.greaseOutput.setPixmap(QPixmap("iconSpindle32On.png"))
        else:
            self.greaseOutput.setPixmap(QPixmap("iconSpindle32Off.png"))

        # Alarmas
        if self.cnc.alarmDoor == 1:
            self.doorAlarm.setPixmap( QPixmap("iconDoor32On.png") )
        else:
            # rev20180626: Si está la puerta abierta tb activamos el icono
            if self.cnc.inputs[2].state == 1:
                self.doorAlarm.setPixmap( QPixmap("iconDoor32On.png") )
            else:
                self.doorAlarm.setPixmap( QPixmap("iconDoor32Off.png") )

        if self.cnc.alarmAir == 1:
            self.airAlarm.setPixmap(QPixmap("iconAir32On.png"))
        else:
            self.airAlarm.setPixmap(QPixmap("iconAir32Off.png"))

        if self.cnc.alarmGrease == 1:
            self.alarmGrease.setPixmap(QPixmap("iconSpindle32On.png"))
        else:
            self.alarmGrease.setPixmap(QPixmap("iconSpindle32Off.png"))

        if self.cnc.alarmStop == 1:
            self.emergAlarm.setPixmap( QPixmap("iconEmergency32On.png") )
        else:
            self.emergAlarm.setPixmap( QPixmap("iconEmergency32Off.png") )

        if self.cnc.alarmLimits == 1:
            self.alarmLimits.setPixmap( QPixmap("iconAlarmLimits32On.png") )
        else:
            self.alarmLimits.setPixmap( QPixmap("iconAlarmLimits32Off.png") )

        if self.cnc.alarmEncoder == 1:
            self.encoderAlarm.setPixmap( QPixmap("iconAlarmEncoder32Off.png") )
        else:
            self.encoderAlarm.setPixmap( QPixmap("iconAlarmEncoder32Off.png") )

        if self.cnc.alarmParser == 1:
            self.alarmSyntax.setPixmap(QPixmap("iconAlarmSyntax32On.png"))
        else:
            self.alarmSyntax.setPixmap(QPixmap("iconAlarmSyntax32Off.png"))
            
        if self.cnc.alarmExec == 1:
            self.alarmExec.setPixmap(QPixmap("iconAlarmExec32On.png"))
        else:
            self.alarmExec.setPixmap(QPixmap("iconAlarmExec32Off.png"))

        if self.cnc.alarmInverter == 1:
            self.inverterAlarm.setPixmap( QPixmap("iconInverter32On.png") )
        else:
            self.inverterAlarm.setPixmap( QPixmap("iconInverter32Off.png") )

            
    def initGui(self):
        self.setWindowTitle("Main window")

        self.setFont(QFont('SansSerif', 16))
        
        if develPlatform() == True:
            self.setGeometry(50, 50, screenWidth, screenHeight)
        else:
            self.setGeometry(0,0, screenWidth, screenHeight)
            
        self.setupComponents()
        if develPlatform() == True:
            self.show()
        else:
            self.showFullScreen()

    def handleRef(self):
        # rev20180425: Si estamos ejecutando un programa no podemos entrar a jog
        if self.running == True:
            return
        
        # rev20180319: Si está activa la alarma de emergencia no dejamos hacer nada
        if self.cnc.alarmStop == True:
            userInfo = QMessageBox.question(self,"STARBORE",self.lang.tr("STOP alarm active."),QMessageBox.Ok)
            return
        
        userInfo = QMessageBox.question(self,"STARBORE",self.lang.tr("Remove piece before homing"),QMessageBox.Ok)
        # Leemos el contenido de ref_all.txt
        with open("ref_all.txt") as f:
            self.ref_all = f.readlines()

        if "Windows" in platform.system():
            windows = True
        else:
            windows = False

        #rev20181115: Sacamos los ejes que esten pisando HOME
        tmps = ""

        if self.cnc.axis[0].homeSensor.state == 1:
            tmps += "G28 X0;"
            
        if self.cnc.axis[1].homeSensor.state == 1:
            tmps += "G28 Y0;"
        
        for line in self.ref_all:
            lastchar = ord(line[-1])
            if lastchar == 10 or lastchar == 13:
                if windows:
                    line = line[0:-1]
                else:
                    line = line[0:-2]
                
            tmps += line + ";"

        chk = self.getChecksum(tmps)
        tmps = "0000"+chk+tmps
        print("Sending:"+ tmps)

        self.timer.stop()
        self.cnc.send(b"start\r")
        time.sleep(1)
        #self.cnc.send("addpage 00000887G28 Z0 F1000;G28 Y0 F1000;G28 X-100 F1000")
        #self.cnc.send("addpage 00010299G28 A0 F10000")
        self.cnc.send(b"addpage "+tmps+"\r")
        time.sleep(1)
        self.timer.start()

    def showFileContents(self):
        dialog = dlgFileContents()
        dialog.setContent(self.tapFileContents)
        if develPlatform() == True:
            dialog.show()
        else:
            dialog.showFullScreen()
            
        dialog.exec_()
        
    def handleMenu(self):
        # rev20180425: Si estamos ejecutando un programa no podemos entrar a jog
        if self.running == True:
            return
        
        dialog = dlgMaint(self.cnc)
        if develPlatform() == True:
            dialog.show()
        else:
            dialog.showFullScreen()
                    
        dialog.exec_()            

    # Evento click botón inicio

    def handleStart(self):

        # copdebug
        self.tapPages = self.processFile()

        print( self.tapPages )
            

        # rev20180425: Si estamos ejecutando un programa no
        if self.running == True:
            return

        # rev20180510: Si hemos llegado al límite de ciclos tenemos que mirar
        # si la config nos permite hacer más ciclos
        # self.lblCycles.setText("cycles\n"+str(self.ciclosRealizados)+"/"+str(self.totalCiclos))
        if self.cyclesOn == True:
            if self.ciclosRealizados == self.totalCiclos:
                print("lala "+str(getLimiteCiclos()))
                if int(getLimiteCiclos()) == 1:
                    userInfo = QMessageBox.question(self,"STARBORE",self.lang.tr("Cycles done, please restart cycle counter."),QMessageBox.Ok)
                    return
                
        # rev20180319: Si está activa la alarma de emergencia no dejamos hacer nada
        if self.cnc.alarmStop == True:
            userInfo = QMessageBox.question(self,"STARBORE",self.lang.tr("STOP alarm active."),QMessageBox.Ok)
            return

        # rev20180527: Comprobamos que se haya seleccionado algun tap
        if not 'content' in dir(self):
            userInfo = QMessageBox.question(self,"STARBORE",self.lang.tr("No tap file selected."),QMessageBox.Ok)
            return
            
        # rev20180102: Chequeo del referenciado antes de iniciar la ejecución
        if self.cnc.referenced == False:
            userInfo = QMessageBox.question(self,"STARBORE",self.lang.tr("Machine not referenced."),QMessageBox.Ok)
            return
            
        if self.running == False:
                            
            # "Deshabilitamos" todos los botones menos stop
            self.btnStart.setIcon( QPixmap("iconStartDis.png") )
            self.btnFile.setIcon( QPixmap("iconUSBDis.png") )
            self.btnJog.setIcon( QPixmap("iconJogDis.png") )
            self.btnRef.setIcon( QPixmap("iconRefDis.png") )
            self.btnAlarm.setIcon( QPixmap("iconAlarmsDis.png") )
            self.btnMant.setIcon( QPixmap("iconMaintDis.png"))
            self.btnCiclos.setIcon( QPixmap("iconFile.png") )
            #self.btnHelp.setIcon( QPixmap("iconHelpDis.png") )
            self.btnQuit.setIcon( QPixmap("iconQuitDis.png") )
            
            # rev20180202: Añadimos una variable para la cuenta de tiempo
            self.startTime = time.time()
            
            self.running = True
            self.timer.stop()

            self.cnc.send(b"start\r")
            
            self.tapPages = self.processFile()

            print( self.tapPages )
            #self.btnStart.setIcon( QPixmap("iconStop.png") )

            self.executingLine = 0

            self.stopCnt = 0

            self.timer.start()
            
        else:
            self.cnc.send(b"stop\r")
            self.running = False
            self.btnStart.setIcon(QPixmap("iconStart.png"))

        self.executingLine += 1
        self.refreshFileText()

    def getChecksum(self, line):
        chk = 0
        for c in line:
            chk += ord(c)

        chks = str(hex(chk))[2:].zfill(4)
        return chks
            
    def processFile(self):
        npage = 0
        pages = []
        page = ""

        if "Windows" in platform.system():
            windows = True
        else:
            windows = False
            
        for line in self.content:
            if not line.startswith('('):
                line = line.rstrip(' \n\r')

                # rev20180203, prueba de triempo de ejecución, aumentamos el tamaño de la pagina a ver
                if len(line) + len(page) > 50:
                #if len(line) + len(page) > 200:
                    chk = self.getChecksum(page)
                    print("page:"+page+"chk:"+chk)
                    
                    pages.append(str(npage).zfill(4)+chk+page)
                    npage += 1
                    page = line + ";"
                    line = ""
                else:
                    page += line + ";"
                    line = ""

        # Cuando acabamos puede que quede una página que no ha llegado a llenarse
        if len(page) > 0:
            chk = self.getChecksum(page)
            #print("page:"+page+"chk:"+chk)
            pages.append(str(npage).zfill(4)+chk+page)

        return pages

    # Evento click botón alarma
    # Ejecuta una instancia de la Vista Alarma desclarada en la
    # línea 1229 de este fichero

    def showAlarms(self):
        # rev20180425: Si estamos ejecutando un programa no podemos entrar a jog
        if self.running == True:
            return
        
        dialog = dlgAlarms(self.cnc)
        if develPlatform() == True:
            dialog.show()
        else:
            dialog.showFullScreen()
                    
        dialog.exec_()
        
    def showHelp(self):
        # rev20180425: Si estamos ejecutando un programa no podemos entrar a jog
        if self.running == True:
            return
        
        dialog = dlgHelp()
        if develPlatform() == True:
            dialog.show()
        else:
            dialog.showFullScreen()
                    
        dialog.exec_()

    def showJog(self):
        # rev20180425: Si estamos ejecutando un programa no podemos entrar a jog
        if self.running == True:
            return
        
        # rev20180319: Si está activa la alarma de emergencia no dejamos hacer nada
        if self.cnc.alarmStop == True:
            userInfo = QMessageBox.question(self,"STARBORE",self.lang.tr("STOP alarm active."),QMessageBox.Ok)
            return
        
        dialog = dlgJog( self.cnc )
        if develPlatform() == True:
            dialog.show()
        else:
            dialog.showFullScreen()

        dialog.exec_()

    def getFileList(self):
        from os import listdir
        from os.path import isdir, isfile, join
        alltaps = []

        for f in sorted(listdir(self.currentLocalDir)):
            if isfile(join(self.currentLocalDir, f)):
                if f.endswith(".tap") or f.endswith(".TAP"):
                    alltaps.append(f)
            elif isdir(join(self.currentLocalDir, f)):
                if f[0] != ".":     #Obviar directorio ocultos (Linux)
                    alltaps.append(self.DIR_LEFT_DELIMETER + f + self.DIR_RIGHT_DELIMETER)

        if self.currentLocalDir != self.LOCAL_PATH:
            alltaps.append(self.DIR_LEFT_DELIMETER + ".." + self.DIR_RIGHT_DELIMETER)

        # Error lector código barras
        listdir(".")

        return alltaps

    def getRemoteFiles(self):
        from os import listdir
        from os.path import isdir, isfile, join
        alltaps = []

        #copdebug
        #if develPlatform() == True:
        #    return alltaps
        
        for f in sorted(listdir(self.currentRemoteDir)):
            if isfile(join(self.currentRemoteDir, f)):
                if f.endswith(".tap") or f.endswith(".TAP"):
                    alltaps.append(f)
            elif isdir(join(self.currentRemoteDir, f)):
                if f[0] != ".":     #Obviar directorio ocultos (Linux)
                    alltaps.append(self.DIR_LEFT_DELIMETER + f + self.DIR_RIGHT_DELIMETER)

        if self.currentRemoteDir != self.REMOTE_PATH:
            alltaps.append(self.DIR_LEFT_DELIMETER + ".." + self.DIR_RIGHT_DELIMETER)

        return alltaps

    def paintEvent(self, e):
        if self.running == True:
            if self.executingLine < 5:
                fromLine = 0
            else:
                if self.executingLine > len(self.content)-10:
                    fromLine = len(self.content)-10
                else:
                    fromLine = self.executingLine - 2
            
            qp = QPainter()
            qp.begin(self)
            lblPos = self.lblFiles.pos()

            #qp.drawRect(lblPos.x(), 178+23*(self.executingLine-fromLine), 300, 20)
            if self.executingLine <= len(self.content):
                qp.drawRect(lblPos.x(), lblPos.y()+71+23*(self.executingLine-fromLine-1), 380, 20)
            else:
                qp.drawRect(lblPos.x(), lblPos.y()+71+23*(len(self.content)-fromLine-1), 380, 20)
            '''
            for i in range(10):
                qp.drawRect(lblPos.x(), 178+23*i, 300, 19)
            '''
            qp.end()
            self.update()

        '''
        rev20181023: Prueba ajuste cursor en rasp
        else:
            #self.lblFiles.setStyleSheet(self.lblFiles.styleSheet()+"QLabel{border:2px solid red;}")
            fromLine = 8
            qp = QPainter()
            qp.begin(self)
            lblPos = self.lblFiles.pos()
            qp.drawRect(lblPos.x(), lblPos.y()+72+22*fromLine, 350, 20)
        '''
            
    def refreshFileText2(self):
        tmps = ""
        iniLine = 0
        endLine = 0
        lineBoundaries = []

        for nline in range(self.fromLine, self.fromLine+10):
            if nline < len(self.content):
                line = str(nline+1)+":"+self.content[nline]
                tmps += line
                lineLen = len( line )
                lineBoundaries.append([iniLine, lineLen])
                iniLine += lineLen

        self.lblFiles.setText(tmps)
        
        
    def refreshFileText(self):
        tmps = ""
        iniLine = 0
        endLine = 0
        lineBoundaries = []
        
        # Calculamos el inicio de la ventana que vamos a mostrar
        if self.executingLine < 5:
            fromLine = 0
        else:
            if self.executingLine > len(self.content)-10:
                fromLine = len(self.content)-10
            else:
                fromLine = self.executingLine - 2

        for nline in range(fromLine, fromLine+10):
            if nline < len(self.content):
                line = str(nline+1)+":"+self.content[nline]
                tmps += line
                lineLen = len( line )
                lineBoundaries.append([iniLine, lineLen])
                iniLine += lineLen

        self.lblFiles.setText(tmps)

    def handleLvRemote(self):

        file = self.lvNetwork.selectedIndexes()
        fname = self.getRemoteFiles()[file[0].row()]

        if fname[0] == self.DIR_LEFT_DELIMETER:
            if fname[1:-1] == "..":
                self.currentRemoteDir = os.path.dirname(self.currentRemoteDir)
            else:
                self.currentRemoteDir = os.path.join(self.currentRemoteDir, fname[1:-1])
            print "Cambio de directorio" + self.currentRemoteDir

            # Estas dos líneas resetea el componente QListView
            # de lo contrario interfiere con el eventHandler (lectura por código barras)
            self.lvNetwork.setVisible(False)
            self.lvNetwork.setVisible(True)
        else:
            fname = os.path.join(self.currentRemoteDir, fname)
            print "Procesando el fichero " + self.fname

            #self.fileStatus = 1
            #self.btnFile.setIcon(self.iconFile)

            with open(fname) as f:
                contents = f.readlines()

            # rev20180504: Si estan activados los ciclos,
            # cada vez que se lea un código hay que preguntar el nº de piezas

            if self.cyclesOn == True:
                dialog = dlgInputNumber(pos=(290,50), widg=self.lblCycles)
                dialog.show()
                dialog.exec_()

                self.ciclosRealizados = 0
                self.totalCiclos = int(self.lblCycles.text())
                self.lblCycles.setText("cycles\n0/"+str(self.totalCiclos))

            self.xdim = "0"
            self.ydim = "0"
            self.zdim = "0"

            #Modificacion 20190903 23.54
            #Código modificado por krlossrs@gmail.com
            #La intension es utilizar variables temporales para almacenar
            #El contenido y el nombre del fichero pues en caso de que la
            #Vista dimension se cancele se debe seguir mostrando los valores
            #anteriores.
            #self.content = []
            content = []
            self.mrkEdge = [False, False, False, False]
            for line in contents:
                if len(line) > 2 and not "(" in line:
                   # rev20181114: Eliminamos los tabuladores
                   line = line.replace('\t','')
                   # rev20190617: Eliminamos espacios duplicados
                   line = re.sub(' +', ' ', line)

                   # Modificacion 20190903 23.54
                   # Código modificado por krlossrs@gmail.com
                   #self.content.append(line)
                   content.append(line)

                # rev20190502: Marcar los cantos a trabajar
                if self.STUB_CANTOS in line:
                    self.mrkEdge = parseMrkEdge(line)
                    print("handleLvRemote: ")
                    print(self.mrkEdge)

                #rev20180203: Extraemos las dimensiones
                if "PIEZA_" in line:
                    if "PIEZA_DX" in line:
                        self.xdim = line.split("=")[1].split(")")[0]
                    if "PIEZA_DY" in line:
                        self.ydim = line.split("=")[1].split(")")[0]
                    if "PIEZA_DZ" in line:
                        self.zdim = line.split("=")[1].split(")")[0]

            # rev20180630: Cuando tenemos las dimensiones
            dialog2 = dlgDimensions([self.xdim, self.ydim, self.zdim], self.mrkEdge, fname, (self.fname == fname))
            if develPlatform() == True:
                dialog2.show()
            else:
                dialog2.showFullScreen()
            dialog2.exec_()

            # Modificacion 20190903 23.54
            # Código modificado por krlossrs@gmail.com
            if dialog2.closedOk == True:
                # rev20190724 Solucionar actualización de fichero abierto
                self.fname = fname
                self.content = content

            self.lblFiles.setTextInteractionFlags( Qt.TextSelectableByKeyboard )


            self.fromLine = 0
            self.refreshFileText2()  # copdebug

            self.lv.setVisible(False)
            self.lvNetwork.setVisible(False)
            self.lblFiles.setVisible(True)
            #self.btnFile.setText(self.lang.tr("contents"))
            self.lv.setVisible(False)

            self.btnStart.setEnabled( True )
            self.btnStart.setIcon(QPixmap("iconStart.png"))

    def handleLv(self):

        file = self.lv.selectedIndexes()
        fname = self.getFileList()[file[0].row()]

        if fname[0] == self.DIR_LEFT_DELIMETER:

            if fname[1:-1] == "..":
                self.currentLocalDir = os.path.dirname(self.currentLocalDir)
            else:
                # if self.currentLocalDir== ".":
                #     self.currentLocalDir= fname[1:-1]
                # else:
                self.currentLocalDir = os.path.join(self.currentLocalDir, fname[1:-1])

            # Estas dos líneas resetea el componente QListView
            # de lo contrario interfiere con el eventHandler (lectura por código barras)
            self.lv.setVisible(False)
            self.lv.setVisible(True)

            print "Cambio de directorio: " + self.currentLocalDir
        else:
            fname = os.path.join(self.currentLocalDir, fname)
            print "Procesando el fichero: " + self.fname

            # self.fileStatus = 1
            # self.btnFile.setIcon(self.iconFile)

            with open(fname) as f:
                # self.content = f.readlines()
                contents = f.readlines()

			# rev20180504: Si estan activados los ciclos,
            # cada vez que se lea un código hay que preguntar el nº de piezas
            if self.cyclesOn == True:
				dialog = dlgInputNumber(pos=(290,50), widg=self.lblCycles)
				dialog.show()
				dialog.exec_()

				self.totalCiclos = int(self.lblCycles.text())
				self.ciclosRealizados = 0
				self.lblCycles.setText("cycles\n0/"+str(self.totalCiclos))


			# rev20180604: Si el fichero no tiene dimendiones que no se quede
			# con las de la pieza anterior
            self.xdim = "0"
            self.ydim = "0"
            self.zdim = "0"

            #Modificacion 20190903 23.54
            #Código modificado por krlossrs@gmail.com
            #La intension es utilizar variables temporales para almacenar
            #El contenido y el nombre del fichero pues en caso de que la
            #Vista dimension se cancele se debe seguir mostrando los valores
            #anteriores.
            #self.content = []
            content = []

            self.mrkEdge = [False, False, False, False]
            for line in contents:
                if len(line) > 2 and not "(" in line:
                    #self.content.append(line)

                    '''
                    #rev20181030: Eliminamos los carácteres raros
                    ret = re.findall("[A-Za-z0-9 +#()_.\n]", line)
                    tmps = ""
                    for c in ret:
                        tmps += c
                        
                    if str(tmps) != str(line):
                        print("line:"+str(len(line))+",tmps:"+str(len(tmps)))
                        line = tmps
                    '''

                    # rev20181114: Eliminamos los tabuladores
                    line = line.replace('\t','')
                    # rev20190617: Eliminamos espacios duplicados
                    line = re.sub(' +', ' ', line)

                    # Modificacion 20190903 23.54
                    # Código modificado por krlossrs@gmail.com
                    # self.content.append(line)
                    content.append(line)

                #rev20190502: Marcar los cantos a trabajar
                if self.STUB_CANTOS in line:
                    self.mrkEdge = parseMrkEdge(line)
                    print("handleLv: ")
                    print(self.mrkEdge)

                #rev20180203: Extraemos las dimensiones
                if "PIEZA_" in line:
                    if "PIEZA_DX" in line:
                        self.xdim = line.split("=")[1].split(")")[0]
                    if "PIEZA_DY" in line:
                        self.ydim = line.split("=")[1].split(")")[0]
                    if "PIEZA_DZ" in line:
                        self.zdim = line.split("=")[1].split(")")[0]

            # rev20180630: Cuando tenemos las dimensiones
            dialog2 = dlgDimensions([self.xdim, self.ydim, self.zdim], self.mrkEdge, fname, (self.fname == fname))

            if develPlatform() == True:
                dialog2.show()
            else:
                dialog2.showFullScreen()
            dialog2.exec_()

            # Modificacion 20190903 23.54
            # Código modificado por krlossrs@gmail.com
            if dialog2.closedOk == True:
                # rev20190724 Solucionar actualización de fichero abierto
                self.fname = fname
                self.content = content

            self.lblFiles.setTextInteractionFlags( Qt.TextSelectableByKeyboard )

            self.fromLine = 0
            self.refreshFileText2() # copdebug

            self.lv.setVisible(False)
            self.lvNetwork.setVisible(False)
            self.lblFiles.setVisible(True)
            #self.btnFile.setText(self.lang.tr("contents"))
            self.lv.setVisible(False)

            self.btnStart.setEnabled( True )
            self.btnStart.setIcon(QPixmap("iconStart.png"))

    def refreshUSBdir(self):
        self.lvModel.clear()
        for f in self.getFileList():
            if "/" in f:
                fields = f.split("/")
                fname = fields[len(fields)-1]
            else:
                fname = f
                            
            self.lvModel.appendRow(QStandardItem(fname))
            self.lv.setModel(self.lvModel)

    def refreshNetworkDir(self):
        self.lvNetworkModel.clear()
        for f in self.getRemoteFiles():
            self.lvNetworkModel.appendRow(QStandardItem(f))

    # Evento click para boton File (USB / Network)
    def handleFile(self):
        print("file status"+str(self.fileStatus))

        if self.running == True:
            return
        
        if self.fileStatus == 0:
            if self.lblFiles.isVisible() == True:
                print("visible!")       
                # Si se estaba viendo el contenido sólo quitamos contenido y pasadmos a dir
                self.lv.setVisible(True)
                self.lblFiles.setVisible(False)
                self.lvNetwork.setVisible(False)
            else:
                self.fileStatus = 1
                self.refreshNetworkDir()

                self.btnFile.setIcon(self.iconNetwork)
                self.btnFile.setText(self.lang.tr("network"))

                self.lv.setVisible(False)
                self.lblFiles.setVisible(False)
                self.lvNetwork.setVisible(True)
                    
        else:
            if self.lblFiles.isVisible() == True:
                self.lv.setVisible(False)
                self.lblFiles.setVisible(False)
                self.lvNetwork.setVisible(True)
            else:
                self.fileStatus = 0

                self.refreshUSBdir()
                        
                self.btnFile.setIcon(self.iconUSB)
                self.btnFile.setText(self.lang.tr("usb"))

                self.lv.setVisible(True)
                self.lblFiles.setVisible(False)
                self.lvNetwork.setVisible(False)
            
    def close(self):
        self.cnc.close()
        self.timer.stop()

    def handleFileNav(self):
        userInfo = QMessageBox.question(self,"STARBORE","file",QMessageBox.Ok)

    def handleQuit(self):

        # rev20180425: Si estamos ejecutando un programa no podemos entrar a jog
        if self.running == True:
            return

        msgBox = QMessageBox()
        msgBox.move(0,0)
        msgBox.setText("STARBORE")
        msgBox.setInformativeText(self.lang.tr("Do you want to shutdown the machine, to restart it or to enter maintenance screen?"))
        shutdownButton = msgBox.addButton(self.tr("Shutdown"), QMessageBox.ActionRole)
        restartButton = msgBox.addButton(self.tr("Restart"), QMessageBox.ActionRole)
        maintenanceButton = msgBox.addButton(self.tr("Maintenance (password required)"), QMessageBox.ActionRole)

        msgBox.exec_()

        if msgBox.clickedButton() == maintenanceButton:
            # rev20180315: Pedir clave para salir al linux
            dialog = dlgInputNumber(pos=(290,50))
            dialog.show()
            dialog.exec_()

            if dialog.strValue == getQuitPassword():
                exit(0)
            else:
                userInfo = QMessageBox.question(self,"STARBORE",self.lang.tr("Password error."),QMessageBox.Ok)
            
            
        else:
            # TODO: Comprobar que estamos en linux
            import os
            if msgBox.clickedButton() == shutdownButton:
                os.system("poweroff")
            else:
                if msgBox.clickedButton() == restartButton:
                    os.system("shutdown -r now")
        
        
    def handleStop(self):
        # rev20180831
        if self.running == True:
            self.cnc.send(b"stop\r")

        # rev20181002: Que envie stop siempre para parar cambios de herramientas, homes, etc
        self.cnc.send(b"stop\r")
            
        self.running = False
        self.btnStart.setIcon(QPixmap("iconStart.png"))
        # rev20180425: Volvemos a los iconos normales
        if self.fileStatus == 0:
            self.btnFile.setIcon( QPixmap("iconUSB.png") ) #poner variable estado
        else:
            self.btnFile.setIcon( QPixmap("iconNetwork.png") ) #poner variable estado
            
        self.btnJog.setIcon( QPixmap("iconJog.png") )
        self.btnRef.setIcon( QPixmap("iconRef.png") )
        self.btnAlarm.setIcon( QPixmap("iconAlarms.png") )
        #self.btnHelp.setIcon( QPixmap("iconHelp.png") )
        self.btnQuit.setIcon( QPixmap("iconQuit.png") )
        #rev20180508
        #if self.cyclesOn == False:
        self.btnCiclos.setIcon( QPixmap("iconFile.png") )
        #else:
            #self.btnCiclos.setIcon( QPixmap("iconCyclesOn.png") )

        self.btnMant.setIcon( QPixmap("iconMaint.png") )
    """

    def handleCycles(self):
        if self.running == True:
            return
            
        if self.cyclesOn == True:
            self.cyclesOn = False
            self.btnCiclos.setIcon( QPixmap("iconCycles.png") )
            self.lblCycles.setVisible(False)
        else:
            self.cyclesOn = True
            self.btnCiclos.setIcon( QPixmap("iconCyclesOn.png") )
            self.lblCycles.setVisible(True)
            
    """
            
            
    def setupComponents(self):
        
        btnPinza = QPushButton(self.lang.tr("CLAMP"))
        btnPinza.setMinimumHeight(70)

        # Línea superior estado (alarmas y salidas
        lblUpperStatus = QLabel("PRES")
        
        # Posiciones de los ejes
        # Ubicados en la parte izquierda de la pantalla principal

        xAxisIcon = QPixmap("xIcon.png")
        xLabelIcon = QLabel()
        xLabelIcon.setPixmap(xAxisIcon)
        self.lblXpos = QLabel(str(self.cnc.axis[0].position)+" mm")
        self.lblXpos.setStyleSheet("QLabel { background-color:none; color: #ffffff; font-weight: bold; font-size:24pt;}")
        xWidget = QWidget()
        xBox = createHBox([xLabelIcon, self.lblXpos])
        xWidget.setLayout(xBox)

        yAxisIcon = QPixmap("yIcon.png")
        yLabelIcon = QLabel()
        yLabelIcon.setPixmap(yAxisIcon)
        self.lblYpos = QLabel(str(self.cnc.axis[1].position)+" mm")
        self.lblYpos.setStyleSheet("QLabel { background-color:none; color: #ffffff; font-weight: bold; font-size:24pt;}")
        yWidget = QWidget()
        yBox = createHBox([yLabelIcon, self.lblYpos])
        yWidget.setLayout(yBox)

        zAxisIcon = QPixmap("zIcon.png")
        zLabelIcon = QLabel()
        zLabelIcon.setPixmap(zAxisIcon)
        self.lblZpos = QLabel(str(self.cnc.axis[2].position)+" mm")
        self.lblZpos.setStyleSheet("QLabel { background-color:none; color: #ffffff; font-weight: bold; font-size:24pt;}")
        zWidget = QWidget()
        zBox = createHBox([zLabelIcon, self.lblZpos])
        zWidget.setLayout(zBox)
        """
        aAxisIcon = QPixmap("aIcon.png")
        aLabelIcon = QLabel()
        aLabelIcon.setPixmap(aAxisIcon)
        self.lblApos = QLabel(str(self.cnc.axis[3].position)+" º")
        self.lblApos.setStyleSheet("QLabel { background-color:none; color: #ffffff; font-weight: bold; font-size:24pt;}")
        aWidget = QWidget()
        aBox = createHBox([aLabelIcon, self.lblApos])
        aWidget.setLayout(aBox)
        """
        # Lista de archivos
        #self.lblFiles = QLabel("")
        #self.lblFiles.setStyleSheet("QLabel {color:white; font-size:14pt;}")
        
        
        self.lv = QListView()
        self.lv.setStyleSheet("QListView {background-color: #232234;color:#ffffff; font-size:18pt; font-weight:bold;}")
        self.lvModel = QStandardItemModel(self.lv)
        for f in self.getFileList():
            #self.lvModel.appendRow(QStandardItem(f))
            if "/" in f:
                fields = f.split("/")
                fname = fields[len(fields)-1]
            else:
                fname = f

            self.lvModel.appendRow(QStandardItem(fname))

        self.lv.setModel(self.lvModel)
        self.lv.clicked.connect(self.handleLv)

        self.lblFiles = QLabel("")
        self.lblFiles.setStyleSheet("QLabel {color:white; font-size:14pt; margin-bottom:30px;}")
        self.lblFiles.setVisible(False)
        #rev20181023: Ajuste cursor linea ejecución
        self.lblFiles.setMaximumHeight( 300 )
        
        self.lvNetwork = QListView()
        self.lvNetwork.setStyleSheet("QListView {background-color: #232234;color:#ffffff; font-size:18pt; font-weight:bold;}")
        self.lvNetworkModel = QStandardItemModel(self.lvNetwork)
        for f in self.getRemoteFiles():
            self.lvNetworkModel.appendRow(QStandardItem(f))
        self.lvNetwork.setModel(self.lvNetworkModel)
        self.lvNetwork.setVisible( False )
        self.lvNetwork.clicked.connect(self.handleLvRemote)

        # Botones
        # OPEN FILE
        self.btnFile = borderLessButton(self.lang.tr("usb"), "iconUSB.png")
        self.fileStatus = 0
        self.btnFile.clicked.connect(self.handleFile)
        self.iconUSB = QPixmap("iconUSB.png")
        self.iconNetwork = QPixmap("iconNetwork.png")
        self.iconFile = QPixmap("iconFile.png")
        self.iconDir = QPixmap("iconOpen.png")
        
        # JOG
        self.btnJog = borderLessButton(self.lang.tr("jog"), "iconJog.png")
        self.btnJog.clicked.connect(self.showJog)
        # REF
        self.btnRef = borderLessButton(self.lang.tr("ref."), "iconRef.png")
        self.btnRef.clicked.connect(self.handleRef)
        # START
        self.btnStart = borderLessButton(self.lang.tr("start"),"iconStartDis.png")
        self.btnStart.clicked.connect(self.handleStart)
        # STOP
        self.btnStop = borderLessButton(self.lang.tr("stop"),"iconStop.png")
        self.btnStop.clicked.connect(self.handleStop)
        # ALARMS
        self.btnAlarm = borderLessButton(self.lang.tr("alarms"),"iconAlarms.png")
        self.btnAlarm.clicked.connect(self.showAlarms)
        # MAINTENANCE
        self.btnMant = borderLessButton(self.lang.tr("maint."), "iconMaint.png")
        self.btnMant.clicked.connect(self.handleMenu)
        # SETTINGS
        #self.btnSettings = borderLessButton("settings", "iconSettings.png")
        #self.btnSettings.clicked.connect( self.handleSettings )
        # HELP
        #self.btnHelp = borderLessButton(self.lang.tr("help"), "iconHelp.png")
        #self.btnHelp.clicked.connect(self.showHelp)
        # QUIT
        self.btnQuit = borderLessButton(self.lang.tr("quit"), "iconQuit.png")
        self.btnQuit.clicked.connect(self.handleQuit)
        # CICLOS
        self.btnCiclos = borderLessButton(self.lang.tr("cycles"), "iconFile.png")
        self.btnCiclos.clicked.connect(self.handleTAPEditor)

        '''
        airAlarm = QLabel("air")
        self.xInput = QLabel()
        self.xInput.setPixmap(QPixmap("iconX32Off"))
        self.yInput = QLabel()
        self.yInput.setPixmap(QPixmap("iconY32Off"))
        self.zInput = QLabel()
        self.zInput.setPixmap(QPixmap("iconZ32Off"))
        self.aInput = QLabel()
        self.aInput.setPixmap(QPixmap("iconA32Off"))
        '''

        # Alarmas
        self.alarmLimits = QLabel()
        self.alarmLimits.setPixmap( QPixmap("iconAlarmLimits32Off.png") )

        self.alarmSyntax = QLabel()
        self.alarmSyntax.setPixmap(QPixmap("iconAlarmSyntax32Off.png"))

        self.alarmExec = QLabel()
        self.alarmExec.setPixmap(QPixmap("iconAlarmExec32Off.png"))

        self.alarmGrease = QLabel()
        self.alarmGrease.setPixmap(QPixmap("iconGrease32Off.png"))
        
        self.airAlarm = QLabel()
        self.airAlarm.setPixmap(QPixmap("iconAir32Off.png"))

        self.doorAlarm = QLabel()
        self.doorAlarm.setPixmap( QPixmap("iconDoor32Off.png") )

        self.emergAlarm = QLabel()
        self.emergAlarm.setPixmap( QPixmap("iconEmergency32Off.png") )

        self.inverterAlarm = QLabel()
        self.inverterAlarm.setPixmap( QPixmap("iconInverter32Off.png") )

        self.encoderAlarm = QLabel()
        self.encoderAlarm.setPixmap( QPixmap("iconAlarmEncoder32Off.png") )

        # Salidas
        self.toolOutput = QLabel()
        self.toolOutput.setPixmap(QPixmap("iconTool32Off.png"))

        self.greaseOutput = QLabel()
        self.greaseOutput.setPixmap(QPixmap("iconSpindle32Off.png"))

        self.pinzaOutput = QLabel()
        self.pinzaOutput.setPixmap(QPixmap("iconPinza32Off.png"))

        self.fresaOutput = QLabel()
        self.fresaOutput.setPixmap(QPixmap("iconPinza32Off.png"))

        spacer1 = QLabel()
        spacer1.setPixmap(QPixmap("iconSpacer.png"))

        spacer2 = QLabel()
        spacer2.setPixmap(QPixmap("iconSpacer.png"))


        
        self.lblCycles = QLabel("cycles:\n1/50")
        self.lblCycles.setStyleSheet( labelStyle )
        self.lblCycles.setAlignment(Qt.AlignCenter)
        self.lblCycles.setVisible(False)
        


        self.statusBox = createHBox([self.alarmLimits, self.alarmSyntax, self.alarmExec, self.alarmGrease, self.encoderAlarm,
                                     self.airAlarm, self.doorAlarm, self.emergAlarm, self.inverterAlarm,
                                     spacer1, spacer2,
                                     self.pinzaOutput, self.toolOutput, self.greaseOutput, self.fresaOutput])
        topWidget = QWidget()
        topWidget.setLayout(self.statusBox)
        
        axisBox = createVBox([xWidget, yWidget, zWidget])
        axisBox.setSpacing(0)
        axisWidget = QFrame()
        axisWidget.setLayout(axisBox)

        centralBox = createHBox([axisWidget, self.lblFiles, self.lv, self.lvNetwork])
        centralWidget = QWidget()
        centralWidget.setLayout(centralBox)
        
        toolbarBox = createHBox([self.btnFile, self.btnJog, self.btnRef, self.btnStart, self.btnStop, self.btnAlarm, self.btnCiclos, self.btnMant, self.btnQuit])
        toolbarWidget = QFrame()
        toolbarWidget.setLayout(toolbarBox)
        toolbarWidget.setStyleSheet("QFrame {border-top:1px solid #636270; border-bottom: 1px solid #636270;margin-top:0px;}")
        toolbarBox.setSpacing(0)
        toolbarBox.setContentsMargins(0,0,0,0)

        mainBox = createVBox([topWidget, centralWidget, toolbarWidget])
        mainBox.setSpacing(0)
        mainBox.setContentsMargins(0,0,0,0)
        
        centralWidget = QWidget()
        centralWidget.setLayout(mainBox)
        self.setCentralWidget(centralWidget)

        self.statusBar().showMessage(self.lang.tr("Ready"))
        self.statusBar().setStyleSheet("color:white;font-size:10pt;font-weight:bold; margin-top:0px;")

        self.setFocus()

    def resetAndReference(self):
        # 20190614: Aplicar un reset y un referenciar tras finalizar un TAP

        # Reset
        print("resetting")
        # rev 20190802: Comentada linea de config.system.Mark porque resetea a valores de fabrica
        # self.cnc.saveConfig("config.system.Mark", "0")
        #self.cnc.send("reset\r")
        #self.cnc.blockSend()
        #time.sleep(5)

        self.lblXpos.setText("{:6.2f}".format(self.cnc.axis[0].position) + " mm")
        self.lblYpos.setText("{:6.2f}".format(self.cnc.axis[1].position) + " mm")
        self.lblZpos.setText("{:6.2f}".format(self.cnc.axis[2].position) + " mm")
        self.lblApos.setText("{:6.2f}".format(self.cnc.axis[3].position) + " º")

        #Reference
        # rev20180425: Si estamos ejecutando un programa no podemos entrar a jog
        #if self.running == True:
        #    return

        # rev20180319: Si está activa la alarma de emergencia no dejamos hacer nada
        #if self.cnc.alarmStop == True:
        #    userInfo = QMessageBox.question(self, "STARBORE", self.lang.tr("STOP alarm active."), QMessageBox.Ok)
        #    return

        #userInfo = QMessageBox.question(self, "STARBORE", self.lang.tr("Remove piece before homing"), QMessageBox.Ok)

        # Leemos el contenido de ref_all.txt
        with open("ref_all.txt") as f:
            self.ref_all = f.readlines()

        if "Windows" in platform.system():
            windows = True
        else:
            windows = False

        # rev20181115: Sacamos los ejes que esten pisando HOME
        tmps = ""

        if self.cnc.axis[0].homeSensor.state == 1:
            tmps += "G28 X0;"

        if self.cnc.axis[1].homeSensor.state == 1:
            tmps += "G28 Y0;"

        for line in self.ref_all:
            lastchar = ord(line[-1])
            if lastchar == 10 or lastchar == 13:
                if windows:
                    line = line[0:-1]
                else:
                    line = line[0:-2]

            tmps += line + ";"

        chk = self.getChecksum(tmps)
        tmps = "0000" + chk + tmps
        print("Sending:" + tmps)

        self.timer.stop()
        #self.cnc.send(b"start\r")
        #time.sleep(5)
        # self.cnc.send("addpage 00000887G28 Z0 F1000;G28 Y0 F1000;G28 X-100 F1000")
        # self.cnc.send("addpage 00010299G28 A0 F10000")
        self.cnc.send(b"addpage " + tmps + "\r")
        #time.sleep(5)
        self.timer.start()

    def handleTAPEditor(self):

        # rev20180319: Si esta activa la alarma de emergencia no dejamos hacer nada
        if self.cnc.alarmStop == True:
            userInfo = QMessageBox.question(self, "VERTIMAQ-CNC", self.lang.tr("STOP alarm active."), QMessageBox.Ok)
            return

        dialog = dlgTAPEditor(self.cnc, self.ctrlFile)
        if develPlatform() == True:
            dialog.show()
        else:
            dialog.showFullScreen()

        dialog.exec_()

        if dialog.retRun and dialog.retFilename is not "":
            self.setupTAPFile(dialog.retFilename)