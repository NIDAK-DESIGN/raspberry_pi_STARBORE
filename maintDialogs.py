# -*- coding: cp1252 -*-
from PySide.QtGui import QDialog, QFont, QPixmap, QGridLayout, QLabel, QMessageBox
from PySide.QtCore import *
from controls import borderLessButton
from basicFuncs import *
from lang import cLanguage

class dlgInputTest(QDialog):
    def __init__(self, cnc, parent=None):
        super(dlgInputTest, self).__init__(parent)

        # Control coms con equipo
        self.cnc = cnc
        self.cnc.readStatus()

        self.lang = cLanguage()
        
        # Timer para actualizar el estado de las entradas
        refreshTimer = QTimer(self)
        self.connect(refreshTimer, SIGNAL("timeout()"), self.refresh)
        refreshTimer.start(1000)

        # Creamos los iconos para luego cambiar la imagen de ON a OFF
        self.xIcons = [QPixmap("iconInputX.png"), QPixmap("iconInputXOn.png")]
        self.yIcons = [QPixmap("iconInputY.png"), QPixmap("iconInputYOn.png")]
        self.zIcons = [QPixmap("iconInputZ.png"), QPixmap("iconInputZOn.png")]
        #self.aIcons = [QPixmap("iconInputA.png"), QPixmap("iconInputAOn.png")]
        self.airIcons = [QPixmap("iconAir.png"), QPixmap("iconAirOn.png")]
        self.startIcons = [QPixmap("iconInputStart.png"), QPixmap("iconInputStartOn.png")]
        self.doorIcons = [QPixmap("iconInputDoor.png"), QPixmap("iconInputDoorOn.png")]
        #self.greaseIcons = [QPixmap("iconInputGrease.png"), QPixmap("iconGreaseOn.png")]
        self.emergencyIcons = [QPixmap("iconInputEmergency.png"), QPixmap("iconInputEmergencyOn.png")]
        self.inverterIcons = [QPixmap("iconInputInverter.png"), QPixmap("iconInputInverterOn.png")]
        
        # Create widgets
        self.setFont(QFont('SansSerif', 16))

        iconOn = QPixmap("ledOn.png")
        iconOff = QPixmap("ledOff.png")

        if self.cnc.axis[0].homeSensor.state == 1:
            self.btnHomeX = borderLessButton(self.lang.tr("home x"), "iconInputXOn.png")
        else:
            self.btnHomeX = borderLessButton(self.lang.tr("home x"), "iconInputX.png")

        if self.cnc.axis[1].homeSensor.state == 1:
            self.btnHomeY = borderLessButton(self.lang.tr("home y"), "iconInputYOn.png")
        else:
            self.btnHomeY = borderLessButton(self.lang.tr("home y"), "iconInputY.png")

        if self.cnc.axis[2].homeSensor.state == 1:
            self.btnHomeZ = borderLessButton(self.lang.tr("home z"), "iconInputZOn.png")
        else:
            self.btnHomeZ = borderLessButton(self.lang.tr("home z"), "iconInputZ.png")

        #if self.cnc.axis[3].homeSensor.state == 1:
            #self.btnHomeA = borderLessButton(self.lang.tr("home a"), "iconInputAOn.png")
        #else:
            #self.btnHomeA = borderLessButton(self.lang.tr("home a"), "iconInputA.png")

        self.btnAir = borderLessButton(self.lang.tr("air"), "iconAir.png")
        self.btnStart = borderLessButton(self.lang.tr("start"), "iconInputStart.png")
        self.btnDoor = borderLessButton(self.lang.tr("door"), "iconInputDoor.png")
        #self.btnGrease = borderLessButton(self.lang.tr("header lock"), "iconInputGrease.png")
        self.btnEmergency = borderLessButton(self.lang.tr("emergency"), "iconInputEmergency.png")
        self.btnInverter = borderLessButton(self.lang.tr("inverter"), "iconInputInverter.png")

        self.btnClose = borderLessButton(self.lang.tr("close"), "btnJogLSlow.png")
        self.btnClose.clicked.connect( self.close )
        
        grid = QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(self.btnHomeX, 0, 0)
        grid.addWidget(self.btnHomeY, 0, 1)
        grid.addWidget(self.btnHomeZ, 0, 2)
        #grid.addWidget(self.btnHomeA, 0, 3)
        grid.addWidget(self.btnAir, 1, 0)
        grid.addWidget(self.btnStart, 1, 1)
        grid.addWidget(self.btnDoor, 1, 2)
        #grid.addWidget(self.btnGrease, 1, 3)
        grid.addWidget(self.btnEmergency, 1, 3)
        grid.addWidget(self.btnInverter, 0, 3)
        grid.addWidget(self.btnClose, 4, 0)
        
        self.setLayout(grid)
        if develPlatform() == True:
            self.setGeometry(50, 50, screenWidth, screenHeight)
        else:
            self.setGeometry(0,0,648,432)

        self.setStyleSheet("QDialog {background-color: #232234;}")

    def refresh(self):
        self.cnc.readStatus()
        self.cnc.printStatus()
        
        self.btnHomeX.setIcon(self.xIcons[self.cnc.axis[0].homeSensor.state])
        self.btnHomeY.setIcon(self.yIcons[self.cnc.axis[1].homeSensor.state])
        self.btnHomeZ.setIcon(self.zIcons[self.cnc.axis[2].homeSensor.state])
        self.btnHomeA.setIcon(self.aIcons[self.cnc.axis[3].homeSensor.state])

        self.btnInverter.setIcon(self.inverterIcons[self.cnc.inputs[0].state])
        self.btnEmergency.setIcon(self.emergencyIcons[self.cnc.inputs[1].state])
        self.btnDoor.setIcon(self.doorIcons[self.cnc.inputs[2].state])
        self.btnAir.setIcon(self.airIcons[self.cnc.inputs[3].state])
        self.btnGrease.setIcon(self.greaseIcons[self.cnc.inputs[4].state])
        self.btnStart.setIcon(self.startIcons[self.cnc.inputs[5].state])
        

class dlgOutputTest(QDialog):

    def refresh( self ):
        self.cnc.readStatus()

        if self.toolSt == 0 and self.cnc.outputs[2].state == 1:
            self.cnc.send("exec M5\r")
            
    def __init__(self, cnc, parent=None):
        super(dlgOutputTest, self).__init__(parent)

        self.cnc = cnc

        self.lang = cLanguage()
        
        # Create widgets
        self.setFont(QFont('SansSerif', 16))

        self.refreshTimer = QTimer(self)
        self.connect(self.refreshTimer, SIGNAL("timeout()"), self.refresh)
        self.refreshTimer.start(400)
        
        iconOn = QPixmap("ledOn.png")
        iconOff = QPixmap("ledOff.png")

        # rev20180103: Mirar el estado de la salida para que el icono
        # inicial refleje el estado actual de la salida
        self.cnc.readStatus()
        self.cnc.printStatus()
        
        if self.cnc.outputs[2].state == 0:
            self.btnTool = borderLessButton(self.lang.tr("tool"), "iconOutTool.png")
            self.toolSt = 0
        else:
            self.btnTool = borderLessButton(self.lang.tr("tool"), "iconOutToolOn.png")
            self.toolSt = 1
        self.btnTool.clicked.connect( self.handleTool )

        if self.cnc.outputs[1].state == 0:
            self.btnPliers = borderLessButton(self.lang.tr("clamp"), "iconOutPliers.png")
            self.pliersSt = 0
        else:
            self.btnPliers = borderLessButton(self.lang.tr("clamp"), "iconOutPliersOn.png")
            self.pliersSt = 1
        self.btnPliers.clicked.connect( self.handlePliers )
        
        
        self.btnLeds = borderLessButton(self.lang.tr("leds"), "iconOutLeds.png")
        self.btnLeds.clicked.connect( self.handleLeds )
        self.ledsSt = 0

        if self.cnc.outputs[2].state == 0:
            self.btnLockHeader = borderLessButton(self.lang.tr("header lock"), "iconOutSpindle.png")
            self.lockSt = 0
        else:
            self.btnLockHeader = borderLessButton(self.lang.tr("header lock"), "iconOutSpindleOn.png")
            self.lockSt = 1
        self.btnLockHeader.clicked.connect( self.handleLock )
        
        if self.cnc.outputs[0].state == 0:
            if getFresaActiveLow() == 0:
                self.btnSpindle = borderLessButton(self.lang.tr("mil. cutter"), "iconOutTool.png")
                self.spindleSt = 0
            else:
                self.btnSpindle = borderLessButton(self.lang.tr("mil. cutter"), "iconOutToolOn.png")
                self.spindleSt = 1
            
        else:
            if getFresaActiveLow() == 0:
                self.btnSpindle = borderLessButton(self.lang.tr("mil. cutter"), "iconOutToolOn.png")
                self.spindleSt = 1
            else:
                self.btnSpindle = borderLessButton(self.lang.tr("mil. cutter"), "iconOutTool.png")
                self.spindleSt = 0
                
        self.btnSpindle.clicked.connect( self.handleFresa )

        # rev20180515: El icono de aguja activaba la grasa, y faltaba la activación de la grasa
        if self.cnc.outputs[3].state == 0:
            self.btnGrease = borderLessButton(self.lang.tr("grease"), "iconOutGrease.png")
            self.greaseSt = 0
        else:
            self.btnGrease = borderLessButton(self.lang.tr("grease"), "iconOutGreaseOn.png")
            self.greaseSt = 1
        self.btnGrease.clicked.connect( self.handleGrease )
        

        self.btnClose = borderLessButton( self.lang.tr("close"), "btnJogLSlow.png")
        self.btnClose.clicked.connect( self.handleClose )
        
        grid = QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(self.btnTool, 0, 0)
        grid.addWidget(self.btnPliers, 0, 1)
        grid.addWidget(self.btnLeds, 0, 2)
        grid.addWidget(self.btnGrease, 0, 3)
        grid.addWidget(self.btnSpindle, 0, 4)

        self.cnc.readConfig()
        if self.cnc.spireDelay == 0:
            grid.addWidget(self.btnLockHeader, 0, 5)
        
        grid.addWidget(self.btnClose, 4, 0)
        
        self.setLayout(grid)
        if develPlatform() == True:
            self.setGeometry(50, 50, screenWidth, screenHeight)
        else:
            self.setGeometry(0,0, screenWidth, screenHeight)

        self.setStyleSheet("QDialog {background-color: #232234;}")

    def handleClose(self):
        canClose = True
        if self.toolSt == 1:
            canClose = False
        if self.pliersSt == 1:
            canClose = False
        if self.spindleSt == 1:
            canClose = False

        if self.greaseSt == 1:
            canClose = False
        if self.ledsSt != 0:
            canClose = False

        if canClose == True:
            self.close()
        else:
            userInfo = QMessageBox.question(self,"STARBORE","<font color='#ffffff'>"+self.lang.tr("Set all outputs to off before closing."),QMessageBox.Ok)
            
    def handleTool(self):
        if self.toolSt == 0:
            self.cnc.send("exec M3\r")
            self.toolSt = 1
            self.btnTool.setIcon(QPixmap("iconOutToolOn.png"))
        else:
            self.cnc.send("exec M5\r")
            self.toolSt = 0
            self.btnTool.setIcon(QPixmap("iconOutTool.png"))

    def handlePliers(self):
        if self.pliersSt == 0:
            self.cnc.send("exec M20\r")
            self.pliersSt = 1
            self.btnPliers.setIcon(QPixmap("iconOutPliersOn.png"))
        else:
            self.cnc.send("exec M21\r")
            self.pliersSt = 0
            self.btnPliers.setIcon(QPixmap("iconOutPliers.png"))

    def handleFresa(self):
        if self.spindleSt == 0:
            # rev20180704: Control sense fresa
            if getFresaActiveLow() == 1:
                self.cnc.send("exec M503\r")
            else:    
                self.cnc.send("exec M502\r")
            self.spindleSt = 1
            self.btnSpindle.setIcon(QPixmap("iconOutToolOn.png"))
        else:
            if getFresaActiveLow() == 1:
                self.cnc.send("exec M502\r")
            else:
                self.cnc.send("exec M503\r")
            self.spindleSt = 0
            self.btnSpindle.setIcon(QPixmap("iconOutTool.png"))

    def handleGrease(self):
        if self.greaseSt == 0:
            self.cnc.send("exec M504\r")
            self.greaseSt = 1
            self.btnGrease.setIcon(QPixmap("iconOutGreaseOn.png"))
        else:
            self.cnc.send("exec M505\r")
            self.greaseSt = 0
            self.btnGrease.setIcon(QPixmap("iconOutGrease.png"))

    def handleLock(self):
        if self.lockSt == 0:
            self.cnc.send("exec M7\r")
            self.lockSt = 1
            self.btnLockHeader.setIcon(QPixmap("iconOutSpindleOn.png"))
        else:
            self.cnc.send("exec M9\r")
            self.lockSt = 0
            self.btnLockHeader.setIcon(QPixmap("iconOutSpindle.png"))

    def handleLeds(self):
        if self.ledsSt == 0:
            self.ledsSt = 1
            self.btnLeds.setIcon(QPixmap("iconOutLedGreen.png"))
            self.cnc.send("output 51\r")
            self.cnc.send("output 60\r")
        else:
            if self.ledsSt == 1:
                self.ledsSt = 2
                self.btnLeds.setIcon(QPixmap("iconOutLedRed.png"))
                self.cnc.send("output 50\r")
                self.cnc.send("output 61\r")
            else:
                self.ledsSt = 0
                self.btnLeds.setIcon(QPixmap("iconOutLeds.png"))
                self.cnc.send("output 52\r")


class dlgGrease(QDialog):
    def __init__(self, parent=None):
        super(dlgGrease, self).__init__(parent)
        # Create widgets
        self.setFont(QFont('SansSerif', 14))

        self.setStyleSheet("QDialog {background-color: #232234;color:#ffffff;}")
        
        lblTitle = QLabel("CONFIRM GREASING?")
        lblTitle.setStyleSheet("QLabel {color:white; font-size:16pt;}")
        btnYes = borderLessButton("", "iconOk.png")
        btnYes.clicked.connect(self.close)
        
        btnNo = borderLessButton("", "iconCancel.png")
        btnNo.clicked.connect(self.close)
        
        grid = QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(lblTitle, 0, 0)
        grid.addWidget(btnYes, 1, 0)
        grid.addWidget(btnNo, 2, 0)

        self.setLayout(grid)
        if develPlatform() == True:
            self.setGeometry(50, 50, screenWidth, screenHeight)
        else:
            self.setGeometry(0,0, screenWidth, screenHeight)
            
class dlgInfo(QDialog):
    def __init__(self, cnc, parent=None):
        super(dlgInfo, self).__init__(parent)

        self.cnc = cnc

        self.lang = cLanguage()
        
        # Create widgets
        self.setFont(QFont('SansSerif', 14))

        lblStyle = "QLabel {color: white; font-size:14pt; float: center;}"

        #rev20180123: Leemos info del archivo
        with open("serial.txt") as f:
            contents = f.readlines()

        for line in contents:
            if "name:" in line:
                fields = line.split(":")
                name = fields[1]

            if "SN:" in line:
                fields = line.split(":")
                sn = fields[1]
            
        lblTitle = QLabel( name )
        lblTitle.setStyleSheet( lblStyle )

        from version import VERSION_MAJOR, VERSION_MINOR, VERSION_REVISION
        strVersion = str(VERSION_MAJOR)+"."
        strVersion += str(VERSION_MINOR)+"."
        strVersion += str(VERSION_REVISION)
        
        lblFirmwareVersion = QLabel(self.lang.tr("software version: ")+strVersion)
        lblFirmwareVersion.setStyleSheet( lblStyle )

        lblSerialNumber = QLabel(self.lang.tr("serial number: ") + sn)
        lblSerialNumber.setStyleSheet( lblStyle )

        # El resto de info la leemos del cnc
        [version, machineTime] = self.cnc.getInfo()
        
        lblSoftwareVersion = QLabel(self.lang.tr("firmware version: ") + version)
        # TODO: leer firmware version del cnc
        lblSoftwareVersion.setStyleSheet( lblStyle )

        # TODO; leer working time tb del cnc
        lblWorkingTime = QLabel(self.lang.tr("working time: ")+ machineTime)
        lblWorkingTime.setStyleSheet( lblStyle )

        btnClose = borderLessButton(self.lang.tr("close"), "btnJogLSlow.png")
        btnClose.clicked.connect(self.close)
        
        grid = QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(lblTitle, 0, 0)
        grid.addWidget(lblFirmwareVersion, 1, 0, aligment=Qt.AlignRight)
        grid.addWidget(lblSoftwareVersion, 2, 0)
        grid.addWidget(lblSerialNumber, 3, 0)
        grid.addWidget(lblWorkingTime, 4, 0)
        grid.addWidget(btnClose, 6, 0)

        self.setLayout(grid)
        if develPlatform() == True:
            self.setGeometry(50, 50, screenWidth, screenHeight)
        else:
            self.setGeometry(0,0, screenWidth, screenHeight)

        self.setStyleSheet("QDialog {background-color: #232234;color:#ffffff;}")
        '''
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(35,34,52))
        self.setPalette(p)
        '''

class dlgTools(QDialog):
    def __init__(self, cnc,parent=None):
        super(dlgTools, self).__init__(parent)

        self.cnc = cnc

        self.lang = cLanguage()
        
        # Create widgets
        self.setFont(QFont('SansSerif', 16))

        self.setStyleSheet("QDialog {background-color: #232234;color:#ffffff;}")

        self.btnClose = borderLessButton(self.lang.tr("close"), "btnJogLSlow.png")
        self.btnClose.clicked.connect(self.close)
        self.btnTool1 = borderLessButton(self.lang.tr("tool 1"), "iconDrill.png")
        self.btnTool2 = borderLessButton(self.lang.tr("tool 2"), "iconDrill.png")
        self.btnTool3 = borderLessButton(self.lang.tr("tool 3"), "iconDrill.png")
        self.btnTool4 = borderLessButton(self.lang.tr("tool 4"), "iconDrill.png")

        self.btnTool1.clicked.connect(self.handleTool1)
        self.btnTool2.clicked.connect(self.handleTool2)
        self.btnTool3.clicked.connect(self.handleTool3)
        self.btnTool4.clicked.connect(self.handleTool4)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.btnTool1, 0, 0)
        grid.addWidget(self.btnTool2, 0, 1)
        grid.addWidget(self.btnTool3, 1, 0)
        grid.addWidget(self.btnTool4, 1, 1)

        grid.addWidget(self.btnClose, 2, 0)
        
        self.setLayout(grid)

        if develPlatform() == True:
            self.setGeometry(50, 50, screenWidth, screenHeight)
        else:
            self.setGeometry(0,0, screenWidth, screenHeight)

    def getChecksum(self, line):
        chk = 0
        for c in line:
            chk += ord(c)

        chks = str(hex(chk))[2:].zfill(4)
        return chks
    
    def handleTool(self, fname):

        # rev20180103: Chequeo del referenciado antes de iniciar la ejecución
        if self.cnc.referenced == False:
            userInfo = QMessageBox.question(self,"DRILLMASTER","<font color='#ffffff'>"+self.lang.tr("Machine not referenced."),QMessageBox.Ok)
            return
        
        with open(fname) as f:
            self.tool1 = f.readlines()

        tmps = ""
        for line in self.tool1:
            # Distinguir windows(-1) de linux(-2)
            lastchar = ord(line[-1])
            if lastchar == 10:
                line = line[0:-2]
                
            tmps += line + ";"

        chk = self.getChecksum(tmps)
        tmps = "0000"+chk+tmps
        print tmps
        
        self.cnc.send(b"start\r")
        self.cnc.send(b"addpage "+tmps+"\r")
        
    def handleTool1(self):
        self.handleTool("tool_0.txt")

    def handleTool2(self):
        self.handleTool("tool_1.txt")

    def handleTool3(self):
        self.handleTool("tool_2.txt")

    def handleTool4(self):
        self.handleTool("tool_3.txt")
    
        
