#from PySide.QtGui import QDialog, QFont, QPixmap, QGridLayout, QLabel, QLineEdit, QGroupBox, QRadioButton, QPushButton, QWidget, QComboBox, QScrollArea, QVBoxLayout
from PySide.QtGui import *
from PySide.QtCore import *
from controls import borderLessButton
from basicFuncs import *
from basicDialogs import dlgInputNumber
from coms import Axis
from lang import cLanguage

class dlgHomeConfig(QDialog):
            
    def eventFilter( self, widget, event):
        if event.type() == QEvent.MouseButtonPress:
            if widget is self.txtPosX:
                dialog = dlgInputNumber(pos=(270,30), widg=self.txtPosX)
                dialog.setModal( True )
                dialog.show()
                dialog.exec_()
            else:
                if widget is self.txtPosY:
                        dialog = dlgInputNumber(pos=(450,30), widg=self.txtPosY)
                        dialog.setModal( True )
                        dialog.show()
                        dialog.exec_()
                else:
                    if widget is self.txtPosZ:
                        dialog = dlgInputNumber(pos=(180,30), widg=self.txtPosZ)
                        dialog.setModal( True )
                        dialog.show()
                        dialog.exec_()
                    else:
                        if widget is self.txtPosA:
                            dialog = dlgInputNumber(pos=(360, 30), widg=self.txtPosA)
                            dialog.setModal( True )
                            dialog.show()
                            dialog.exec_()
                        else:
                            if widget is self.txtSpeedX:
                                dialog = dlgInputNumber(pos=(270,30), widg=self.txtSpeedX)
                                dialog.setModal( True )
                                dialog.show()
                                dialog.exec_()
                            else:
                                if widget is self.txtSpeedY:
                                    dialog = dlgInputNumber(pos=(460,30), widg=self.txtSpeedY)
                                    dialog.setModal( True )
                                    dialog.show()
                                    dialog.exec_()
                                else:
                                    if widget is self.txtSpeedZ:
                                        dialog = dlgInputNumber(pos=(180,30), widg=self.txtSpeedZ)
                                        dialog.setModal( True )
                                        dialog.show()
                                        dialog.exec_()
                                    else:
                                        if widget is self.txtSpeedA:
                                            dialog = dlgInputNumber(pos=(360,30), widg=self.txtSpeedA)
                                            dialog.setModal( True )
                                            dialog.show()
                                            dialog.exec_()
            
        return QWidget.eventFilter(self, widget, event)
    
    def __init__(self, cnc, parent=None):
        super(dlgHomeConfig, self).__init__(parent)

        self.cnc = cnc

        self.cnc.readConfig()
        self.cnc.printConfig()

        self.lang = cLanguage()
        
        # Create widgets
        self.setFont(QFont('SansSerif', 14))

        self.setStyleSheet("QDialog {background-color: #232234;color:#ffffff;}")
        
        lblX = QLabel("")
        xpm = QPixmap("iconInputX.png")
        lblX.setPixmap(xpm)
        
        lblY = QLabel("Y")
        ypm = QPixmap("iconInputY.png")
        lblY.setPixmap(ypm)
        
        lblZ = QLabel("Z")
        zpm = QPixmap("iconInputZ.png")
        lblZ.setPixmap(zpm)
        
        lblA = QLabel("")
        apm = QPixmap("iconInputA.png")
        lblA.setPixmap(apm)

        lblIconHomePos = QLabel("")
        lblIconHomePos.setPixmap(QPixmap("iconHomePos.png"))
        lblIconHomeDir = QLabel("")
        lblIconHomeDir.setPixmap(QPixmap("iconHomeDirection.png"))
        lblIconHomeVel = QLabel("")
        lblIconHomeVel.setPixmap(QPixmap("iconHomeSpeed.png"))
        lblIconHomeSense = QLabel("")
        lblIconHomeSense.setPixmap(QPixmap("iconHomeSense.png"))

        lblHomePosition = QLabel(self.lang.tr("Position"))
        lblHomePosition.setStyleSheet(labelStyle)
        self.txtPosX = QLineEdit(str(self.cnc.axis[0].homePos))
        self.txtPosX.installEventFilter( self )
        self.txtPosX.setStyleSheet(lineEditStyle)
        self.txtPosY = QLineEdit(str(self.cnc.axis[1].homePos))
        self.txtPosY.setStyleSheet( lineEditStyle )
        self.txtPosY.installEventFilter( self )
        self.txtPosZ = QLineEdit(str(self.cnc.axis[2].homePos))
        self.txtPosZ.setStyleSheet( lineEditStyle )
        self.txtPosZ.installEventFilter( self )
        self.txtPosA = QLineEdit(str(self.cnc.axis[3].homePos))
        self.txtPosA.setStyleSheet( lineEditStyle )
        self.txtPosA.installEventFilter( self )
        
        lblHomeDirection = QLabel(self.lang.tr("Direction"))
        lblHomeDirection.setStyleSheet(labelStyle)

        itemDelegate = QStyledItemDelegate()
        
        self.dirXCombo = QComboBox()
        self.dirXCombo.addItem(self.lang.tr("Right (+)"))
        self.dirXCombo.addItem(self.lang.tr("Left (-)"))
        if self.cnc.axis[0].homeDir == 1:
            self.dirXCombo.setCurrentIndex(0)
        else:
            self.dirXCombo.setCurrentIndex(1)
        self.dirXCombo.setStyleSheet(comboStyle)
        self.dirXCombo.setItemDelegate(itemDelegate)

        self.dirYCombo = QComboBox()
        self.dirYCombo.addItem(self.lang.tr("Up (+)"))
        self.dirYCombo.addItem(self.lang.tr("Down (-)"))
        if self.cnc.axis[1].homeDir == 1:
            self.dirYCombo.setCurrentIndex(0)
        else:
            self.dirYCombo.setCurrentIndex(1)
        self.dirYCombo.setStyleSheet(comboStyle)
        self.dirYCombo.setItemDelegate(itemDelegate)

        self.dirZCombo = QComboBox()
        self.dirZCombo.addItem(self.lang.tr("Fwd (+)"))
        self.dirZCombo.addItem(self.lang.tr("BackWd (-)"))
        if self.cnc.axis[2].homeDir == 1:
            self.dirZCombo.setCurrentIndex(0)
        else:
            self.dirZCombo.setCurrentIndex(1)
        self.dirZCombo.setStyleSheet(comboStyle)
        self.dirZCombo.setItemDelegate(itemDelegate)

        self.dirACombo = QComboBox()
        self.dirACombo.addItem(self.lang.tr("CW (+)"))
        self.dirACombo.addItem(self.lang.tr("CCW (-)"))
        if self.cnc.axis[3].homeDir == 1:
            self.dirACombo.setCurrentIndex(0)
        else:
            self.dirACombo.setCurrentIndex(1)
        self.dirACombo.setStyleSheet(comboStyle)
        self.dirACombo.setItemDelegate(itemDelegate)
        
        lblHomeSpeed = QLabel(self.lang.tr("Speed"))
        lblHomeSpeed.setStyleSheet(labelStyle)
        self.txtSpeedX = QLineEdit(str(self.cnc.axis[0].homeSpeed))
        self.txtSpeedX.setStyleSheet( lineEditStyle )
        self.txtSpeedX.installEventFilter( self )
        self.txtSpeedY = QLineEdit(str(self.cnc.axis[1].homeSpeed))
        self.txtSpeedY.setStyleSheet( lineEditStyle )
        self.txtSpeedY.installEventFilter( self )
        self.txtSpeedZ = QLineEdit(str(self.cnc.axis[2].homeSpeed))
        self.txtSpeedZ.setStyleSheet( lineEditStyle )
        self.txtSpeedZ.installEventFilter( self )
        self.txtSpeedA = QLineEdit(str(self.cnc.axis[3].homeSpeed))
        self.txtSpeedA.setStyleSheet( lineEditStyle )
        self.txtSpeedA.installEventFilter( self )
        
        lblHomeSensor = QLabel(self.lang.tr("Sensor"))
        lblHomeSensor.setStyleSheet(labelStyle)
        self.sensorXCombo = createHLCombo()
        if self.cnc.axis[0].homeSensor.sense == 0:
            self.sensorXCombo.setCurrentIndex(0)
        else:
            self.sensorXCombo.setCurrentIndex(1)
        self.sensorXCombo.setStyleSheet(comboStyle)
        self.sensorXCombo.setItemDelegate(itemDelegate)
        
        self.sensorYCombo = createHLCombo()
        if self.cnc.axis[1].homeSensor.sense == 0:
            self.sensorYCombo.setCurrentIndex(0)
        else:
            self.sensorYCombo.setCurrentIndex(1)
        self.sensorYCombo.setStyleSheet(comboStyle)
        self.sensorYCombo.setItemDelegate(itemDelegate)
        
        self.sensorZCombo = createHLCombo()
        if self.cnc.axis[2].homeSensor.sense == 0:
            self.sensorZCombo.setCurrentIndex(0)
        else:
            self.sensorZCombo.setCurrentIndex(1)
        self.sensorZCombo.setStyleSheet(comboStyle)
        self.sensorZCombo.setItemDelegate(itemDelegate)
        
        self.sensorACombo = createHLCombo()
        if self.cnc.axis[3].homeSensor.sense == 0:
            self.sensorACombo.setCurrentIndex(0)
        else:
            self.sensorACombo.setCurrentIndex(1)
        self.sensorACombo.setStyleSheet(comboStyle)
        self.sensorACombo.setItemDelegate(itemDelegate)

        btnOk = borderLessButton(self.lang.tr("save"), "iconOk.png")
        btnOk.clicked.connect(self.saveConfig)
        
        btnCancel = borderLessButton(self.lang.tr("cancel"), "iconCancel.png")
        btnCancel.clicked.connect(self.close)

        grid = QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(lblX, 0, 2)
        grid.addWidget(lblY, 0, 3)
        grid.addWidget(lblZ, 0, 4)
        grid.addWidget(lblA, 0, 5)
        
        grid.addWidget(lblIconHomePos, 1, 0)
        grid.addWidget(lblHomePosition, 1, 1)
        grid.addWidget(self.txtPosX, 1, 2)
        grid.addWidget(self.txtPosY, 1, 3)
        grid.addWidget(self.txtPosZ, 1, 4)
        grid.addWidget(self.txtPosA, 1, 5)

        grid.addWidget(lblIconHomeDir, 2, 0)
        grid.addWidget(lblHomeDirection, 2, 1)
        grid.addWidget(self.dirXCombo, 2, 2)
        grid.addWidget(self.dirYCombo, 2, 3)
        grid.addWidget(self.dirZCombo, 2, 4)
        grid.addWidget(self.dirACombo, 2, 5)

        grid.addWidget(lblIconHomeVel, 3, 0)
        grid.addWidget(lblHomeSpeed, 3, 1)
        grid.addWidget(self.txtSpeedX, 3, 2)
        grid.addWidget(self.txtSpeedY, 3, 3)
        grid.addWidget(self.txtSpeedZ, 3, 4)
        grid.addWidget(self.txtSpeedA, 3, 5)

        grid.addWidget(lblIconHomeSense, 4, 0)
        grid.addWidget(lblHomeSensor, 4, 1)
        grid.addWidget(self.sensorXCombo, 4, 2)
        grid.addWidget(self.sensorYCombo, 4, 3)
        grid.addWidget(self.sensorZCombo, 4, 4)
        grid.addWidget(self.sensorACombo, 4, 5)

        grid.addWidget(btnCancel, 5, 3)
        grid.addWidget(btnOk, 5, 4)
        
        self.setLayout(grid)
        if develPlatform() == True:
            self.setGeometry(50, 50, screenWidth, screenHeight)
        else:
            self.setGeometry(0,0, screenWidth, screenHeight)

    def saveConfig(self):
        # Salvamos solo las cosas que hayan cambiado
        tmpAxis = []
        xAxis = Axis('X')
        yAxis = Axis('Y')
        zAxis = Axis('Z')
        aAxis = Axis('A')
        tmpAxis.append(xAxis)
        tmpAxis.append(yAxis)
        tmpAxis.append(zAxis)
        tmpAxis.append(aAxis)

        # Rellenamos la estrucutra temporal con los datos del form para luego comparar dentro del for
        # -- X --
        tmpAxis[0].homePos = float(self.txtPosX.text())
        tmpAxis[0].homeSpeed = int(self.txtSpeedX.text())
        if self.dirXCombo.currentIndex() == 0:
            tmpAxis[0].homeDir = 1
        else:
            tmpAxis[0].homeDir = -1

        if self.sensorXCombo.currentIndex() == 0:
            tmpAxis[0].homeSensor.sense = 0
        else:
            tmpAxis[0].homeSensor.sense = 1

        # -- Y --
        tmpAxis[1].homePos = float(self.txtPosY.text())
        tmpAxis[1].homeSpeed = int(self.txtSpeedY.text())
        if self.dirYCombo.currentIndex() == 0:
            tmpAxis[1].homeDir = 1
        else:
            tmpAxis[1].homeDir = -1

        if self.sensorYCombo.currentIndex() == 0:
            tmpAxis[1].homeSensor.sense = 0
        else:
            tmpAxis[1].homeSensor.sense = 1

        # -- Z --
        tmpAxis[2].homePos = float(self.txtPosZ.text())
        tmpAxis[2].homeSpeed = int(self.txtSpeedZ.text())
        if self.dirZCombo.currentIndex() == 0:
            tmpAxis[2].homeDir = 1
        else:
            tmpAxis[2].homeDir = -1

        if self.sensorZCombo.currentIndex() == 0:
            tmpAxis[2].homeSensor.sense = 0
        else:
            tmpAxis[2].homeSensor.sense = 1

        # -- A --
        tmpAxis[3].homePos = float(self.txtPosA.text())
        tmpAxis[3].homeSpeed = int(self.txtSpeedA.text())
        if self.dirACombo.currentIndex() == 0:
            tmpAxis[3].homeDir = 1
        else:
            tmpAxis[3].homeDir = -1

        if self.sensorACombo.currentIndex() == 0:
            tmpAxis[3].homeSensor.sense = 0
        else:
            tmpAxis[3].homeSensor.sense = 1

        for i in range(0,4):
            if tmpAxis[i].homePos != self.cnc.axis[i].homePos:
                self.cnc.saveConfig("config.axis["+str(i)+"].HomePosition", tmpAxis[i].homePos)

            if tmpAxis[i].homeSpeed != self.cnc.axis[i].homeSpeed:
                self.cnc.saveConfig("config.axis["+str(i)+"].HomeSpeed", tmpAxis[i].homeSpeed)

            if tmpAxis[i].homeDir != self.cnc.axis[i].homeDir:
                self.cnc.saveConfig("config.axis["+str(i)+"].HomeDir", tmpAxis[i].homeDir)

            if tmpAxis[i].homeSensor.sense != self.cnc.axis[i].homeSensor.sense:
                self.cnc.saveConfig("config.axis["+str(i)+"].HomeActiveLow", tmpAxis[i].homeSensor.sense)

        # Cuando se haya salvado todo salimos
        self.close()
            
