from PySide.QtGui import QDialog, QFont, QPixmap, QGridLayout, QLabel, QMessageBox
from PySide.QtCore import *
from controls import borderLessButton
from basicFuncs import *
from basicDialogs import dlgInputNumber
import threading
from lang import cLanguage

class dlgJog(QDialog):

    def timerElapsed(self):
        if self.runningJog == True:

            self.cnc.readStatus()

            if self.enteringPos != 'X':
                self.lblX.setText( "{:6.2f}".format( self.cnc.axis[0].position ) + " mm")

            if self.enteringPos != 'Y':
                self.lblY.setText ( "{:6.2f}".format( self.cnc.axis[1].position ) + " mm")

            if self.enteringPos != 'Z':
                self.lblZ.setText ( "{:6.2f}".format( self.cnc.axis[2].position ) + " mm")

            #if self.enteringPos != 'A':
                #self.lblA.setText ( "{:6.2f}".format( self.cnc.axis[3].position ) + " mm")

            if self.cnc.outputs[2].state == 1:
                self.btnTool.setIcon(QPixmap("iconDrillSmallOn.png"))
            else:
                self.btnTool.setIcon(QPixmap("iconDrillSmall.png"))

            if self.cnc.outputs[1].state == 1:
                self.btnClamp.setIcon(QPixmap("iconClampSmallOn.png"))
            else:
                self.btnClamp.setIcon(QPixmap("iconClampSmall.png"))
                
                
                        
    def __init__(self, cnc, parent=None):
        super(dlgJog, self).__init__(parent)
        
        self.cnc = cnc
        # Create widgets
        self.setFont(QFont('SansSerif', 16))

        self.setStyleSheet("QDialog {background-color: #232234;color:#ffffff;}")

        self.lang = cLanguage()
        # X
        lblIconX = QLabel()
        xIcon = QPixmap("iconInputX.png")
        lblIconX.setPixmap(xIcon)
        self.lblX = QLabel("1234.56")
        self.lblX.setStyleSheet("QLabel { background-color:none; color: #ffffff; font-weight: bold; font-size:18pt;margin-left:10px;}")
        btnLFast = borderLessButton("", "btnJogLFast.png")
        btnLSlow = borderLessButton("", "btnJogLSlow.png")
        btnXHome = borderLessButton("", "btnJogHome.png")
        btnRSlow = borderLessButton("", "btnJogRSlow.png")
        btnRFast = borderLessButton("", "btnJogRFast.png")
        btnXGoto = borderLessButton("", "btnJogXGoto.png")
        btnXGoto.clicked.connect(self.handleGotoX)
        btnLFast.pressed.connect(self.handleLFast)
        btnLFast.released.connect(self.stopMovement)
        btnLSlow.pressed.connect(self.handleLSlow)
        btnLSlow.released.connect(self.stopMovement)
        btnRFast.pressed.connect(self.handleRFast)
        btnRFast.released.connect(self.stopMovement)
        btnRSlow.pressed.connect(self.handleRSlow)
        btnRSlow.released.connect(self.stopMovement)
        btnXHome.clicked.connect( self.handleHomeX )
        
        # Y
        lblIconY = QLabel()
        yIcon = QPixmap("iconInputY.png")
        lblIconY.setPixmap(yIcon)
        self.lblY = QLabel("-12.6")
        self.lblY.setStyleSheet("QLabel { background-color:none; color: #ffffff; font-weight: bold; font-size:18pt;margin-left:10px;}")
        btnUFast = borderLessButton("", "btnJogUFast.png")
        btnUSlow = borderLessButton("", "btnJogUSlow.png")
        btnYHome = borderLessButton("", "btnJogHome.png")
        btnDSlow = borderLessButton("", "btnJogDSlow.png")
        btnDFast = borderLessButton("", "btnJogDFast.png")
        btnYGoto = borderLessButton("", "btnJogYGoto.png")
        btnYGoto.clicked.connect(self.handleGotoY)
        btnUFast.pressed.connect(self.handleUFast)
        btnUFast.released.connect(self.stopMovement)
        btnUSlow.pressed.connect(self.handleUSlow)
        btnUSlow.released.connect(self.stopMovement)
        btnDFast.pressed.connect(self.handleDFast)
        btnDFast.released.connect(self.stopMovement)
        btnDSlow.pressed.connect(self.handleDSlow)
        btnDSlow.released.connect(self.stopMovement)
        btnYHome.clicked.connect( self.handleHomeY )

        # Z
        lblIconZ = QLabel()
        zIcon = QPixmap("iconInputZ.png")
        lblIconZ.setPixmap(zIcon)
        self.lblZ = QLabel("-100.00")
        self.lblZ.setStyleSheet("QLabel { background-color:none; color: #ffffff; font-weight: bold; font-size:18pt;margin-left:10px;}")
        btnFFast = borderLessButton("", "btnJogFFast.png")
        btnFSlow = borderLessButton("", "btnJogFSlow.png")
        btnZHome = borderLessButton("", "btnJogHome.png")
        btnBSlow = borderLessButton("", "btnJogBSlow.png")
        btnBFast = borderLessButton("", "btnJogBFast.png")
        btnZGoto = borderLessButton("", "btnJogZGoto.png")
        btnZGoto.clicked.connect(self.handleGotoZ)
        btnFFast.pressed.connect(self.handleFFast)
        btnFFast.released.connect(self.stopMovement)
        btnFSlow.pressed.connect(self.handleFSlow)
        btnFSlow.released.connect(self.stopMovement)
        btnBFast.pressed.connect(self.handleBFast)
        btnBFast.released.connect(self.stopMovement)
        btnBSlow.pressed.connect(self.handleBSlow)
        btnBSlow.released.connect(self.stopMovement)
        btnZHome.clicked.connect( self.handleHomeZ )

        # A
        lblIconA = QLabel()
        aIcon = QPixmap("iconInputA.png")
        lblIconA.setPixmap(aIcon)
        self.lblA = QLabel("172.12")
        self.lblA.setStyleSheet("QLabel { background-color:none; color: #ffffff; font-weight: bold; font-size:18pt;margin-left:10px;}")
        btnCFast = borderLessButton("", "btnJogCFast.png")
        btnCSlow = borderLessButton("", "btnJogCSlow.png")
        btnAHome = borderLessButton("", "btnJogHome.png")
        btnWSlow = borderLessButton("", "btnJogWSlow.png")
        btnWFast = borderLessButton("", "btnJogWFast.png")
        btnAGoto = borderLessButton("", "btnJogAGoto.png")
        btnAGoto.clicked.connect(self.handleGotoA)
        btnCFast.pressed.connect(self.handleCWFast)
        btnCFast.released.connect(self.stopMovement)
        btnCSlow.pressed.connect(self.handleCWSlow)
        btnCSlow.released.connect(self.stopMovement)
        btnWFast.pressed.connect(self.handleCCWFast)
        btnWFast.released.connect(self.stopMovement)
        btnWSlow.pressed.connect(self.handleCCWSlow)
        btnWSlow.released.connect(self.stopMovement)
        btnAHome.clicked.connect( self.handleHomeA )
        
        btnClose = borderLessButton(self.lang.tr("close"), "btnJogLSlow.png")
        #btnClose.setToolButtonStyle( Qt.ToolButtonTextBesideIcon )
        btnClose.clicked.connect(self.handleClose)

        self.btnTool = borderLessButton("", "iconDrillSmall.png")
        self.btnTool.clicked.connect(self.handleTool)
        
        btnHomeSettings = borderLessButton("", "iconHomeConfigSmall.png")
        btnHomeSettings.clicked.connect(self.handleHomeSettings)

        self.btnClamp = borderLessButton("", "iconClampSmall.png")
        self.btnClamp.clicked.connect(self.handleClamp)
        
        grid = QGridLayout()
        grid.setSpacing(2)

        grid.addWidget(lblIconX, 0, 0)
        grid.addWidget(self.lblX, 0, 1)
        grid.addWidget(btnLFast, 0, 2)
        grid.addWidget(btnLSlow, 0, 3)
        grid.addWidget(btnXHome, 0, 4)
        grid.addWidget(btnRSlow, 0, 5)
        grid.addWidget(btnRFast, 0, 6)
        grid.addWidget(btnXGoto, 0, 7)

        grid.addWidget(lblIconY, 1, 0)
        grid.addWidget(self.lblY, 1, 1)
        grid.addWidget(btnUFast, 1, 2)
        grid.addWidget(btnUSlow, 1, 3)
        grid.addWidget(btnYHome, 1, 4)
        grid.addWidget(btnDSlow, 1, 5)
        grid.addWidget(btnDFast, 1, 6)
        grid.addWidget(btnYGoto, 1, 7)

        grid.addWidget(lblIconZ, 2, 0)
        grid.addWidget(self.lblZ, 2, 1)
        grid.addWidget(btnFFast, 2, 2)
        grid.addWidget(btnFSlow, 2, 3)
        grid.addWidget(btnZHome, 2, 4)
        grid.addWidget(btnBSlow, 2, 5)
        grid.addWidget(btnBFast, 2, 6)
        grid.addWidget(btnZGoto, 2, 7)

        """
        grid.addWidget(lblIconA, 3, 0)
        grid.addWidget(self.lblA, 3, 1)
        grid.addWidget(btnCFast, 3, 2)
        grid.addWidget(btnCSlow, 3, 3)
        grid.addWidget(btnAHome, 3, 4)
        grid.addWidget(btnWSlow, 3, 5)
        grid.addWidget(btnWFast, 3, 6)
        grid.addWidget(btnAGoto, 3, 7)
        
         """
        
        grid.addWidget(btnClose, 5, 0)
        grid.addWidget(self.btnTool, 5, 2)
        grid.addWidget(btnHomeSettings, 5, 7)

        grid.addWidget(self.btnClamp, 5, 3)
        
        self.setLayout(grid)
        if develPlatform() == True:
            self.setGeometry(50, 50, screenWidth, screenHeight)
        else:
            self.setGeometry(0,0, screenWidth, screenHeight)

        # rev20171005: Timer para ir refrescando la posicion de cada eje
        self.enteringPos = ''
        self.runningJog = True

        self.timer = QTimer(self)
        self.timer.setInterval(1500)
        self.timer.timeout.connect(self.timerElapsed)
        self.timer.start()

    def handleClamp( self ):
        if self.cnc.outputs[1].state == 1:
            self.cnc.send(b"exec m21\r")
        else:
            self.cnc.send(b"exec m20\r")
            
    def handleTool(self):
        if self.cnc.outputs[2].state == 1:
            self.cnc.send(b"exec m5\r")
        else:
            self.cnc.send(b"start\r")
            self.cnc.send(b"addpage 000005ceG1 A0 F5000;M3;")

    def handleHomeSettings(self):

        dialog = dlgInputNumber(pos=(290,50))
        dialog.show()
        dialog.exec_()

        if dialog.strValue == getSettingsPassword():
            from homeDialog import dlgHomeConfig

            dialog = dlgHomeConfig(self.cnc)
            if develPlatform() == True:
                dialog.show()
            else:
                dialog.showFullScreen()
            
            dialog.exec_()
        else:
            userInfo = QMessageBox.question(self,"DRILLMASTER","<font color='#ffffff'>"+self.lang.tr("Password error."),QMessageBox.Ok)
                   
    def handleClose(self):
        self.runningJog = False
        self.close()

    def handleHomeZ(self):
        self.cnc.send("exec G28 Z0\r")
        
    def handleFFast(self):
        self.cnc.send("jog ZUF\r")

    def handleBFast(self):
        self.cnc.send("jog ZDF\r")

    def handleFSlow(self):
        self.cnc.send("jog ZUS\r")

    def handleBSlow(self):
        self.cnc.send("jog ZDS\r")

    def handleHomeA(self):
        self.cnc.send("exec G28 A0\r")
        
    def handleCWFast(self):
        self.cnc.send("jog AUF\r")

    def handleCCWFast(self):
        self.cnc.send("jog ADF\r")

    def handleCWSlow(self):
        self.cnc.send("jog AUS\r")

    def handleCCWSlow(self):
        self.cnc.send("jog ADS\r")

    def handleHomeY(self):
        self.cnc.send("exec G28 Y0\r")
        
    def handleUFast(self):
        self.cnc.send("jog YUF\r")

    def handleDFast(self):
        self.cnc.send("jog YDF\r")

    def handleUSlow(self):
        self.cnc.send("jog YUS\r")

    def handleDSlow(self):
        self.cnc.send("jog YDS\r")
        
    def handleHomeX(self):
        self.cnc.send("exec G28 X0\r")
        
    def stopMovement(self):
        self.cnc.send("jog\r")
        
    def handleLFast(self):
        self.cnc.send("jog XUF\r")

    def handleRFast(self):
        self.cnc.send("jog XDF\r")

    def handleLSlow(self):
        self.cnc.send("jog XUS\r")

    def handleRSlow(self):
        self.cnc.send("jog XDS\r")

    def getChecksum(self, line):
        chk = 0
        for c in line:
            chk += ord(c)

        chks = str(hex(chk))[2:].zfill(4)
        return chks
    
    def handleGotoX(self):
        self.enteringPos = 'X'
        dialog = dlgInputNumber(pos=(290,50), widg=self.lblX)
        dialog.show()
        dialog.exec_()

        if self.lblX.text()[0] == '+': 
            tmps = self.lblX.text()[1:]
        else:
            tmps = self.lblX.text()

        self.enteringPos = ''

        #tmps = "G1 X"+tmps+" F"+getGotoSpeed()+";"
        tmps = "G1 X"+tmps+" F5000;"
        tmps = tmps.encode('ascii')
        
        chk = self.getChecksum( tmps )
        self.cnc.send(b"start\r")
        self.cnc.send(b'addpage 0000'+chk+tmps+"\r")
        #self.cnc.send(b"addpage 00000344G1 X1000 F20000;\r")
        #self.cnc.send(b"addpage 000005ceG1 A0 F5000;M3;")
        print( "addpage 0000"+chk+tmps )

    def handleGotoY(self):
        self.enteringPos = 'Y'
        dialog = dlgInputNumber(pos=(290,50), widg=self.lblY)
        dialog.show()
        dialog.exec_()

        if self.lblY.text()[0] == '+': 
            tmps = self.lblY.text()[1:]
        else:
            tmps = self.lblY.text()

        tmps = tmps.encode('ascii')
        #self.cnc.send(b"exec G1 Y"+tmps+" F"+getGotoSpeed()+"\r")
        self.cnc.send(b"exec G1 Y"+tmps+" F5000\r")

    def handleGotoZ(self):
        self.enteringPos = 'Z'
        dialog = dlgInputNumber(pos=(290,50), widg=self.lblZ)
        dialog.show()
        dialog.exec_()

        if self.lblZ.text()[0] == '+': 
            tmps = self.lblZ.text()[1:]
        else:
            tmps = self.lblZ.text()

        tmps = tmps.encode('ascii')
        #self.cnc.send(b"exec G1 Z"+tmps+" F"+getGotoSpeed()+"\r")
        self.cnc.send(b"exec G1 Z"+tmps+" F5000\r")

    def handleGotoA(self):
        self.enteringPos = 'A'
        dialog = dlgInputNumber(pos=(290,50), widg=self.lblA)
        dialog.show()
        dialog.exec_()

        if self.lblA.text()[0] == '+': 
            tmps = self.lblA.text()[1:]
        else:
            tmps = self.lblA.text()

        tmps = tmps.encode('ascii')
        self.cnc.send(b"exec G1 A"+tmps+" F5000\r")
