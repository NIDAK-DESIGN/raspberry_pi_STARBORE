from PySide.QtGui import QDialog, QFont, QPixmap, QGridLayout, QLabel, QLineEdit, QGroupBox, QRadioButton, QPushButton, QWidget, QComboBox, QScrollArea, QVBoxLayout
from PySide.QtGui import QStyledItemDelegate
from PySide.QtCore import *
from controls import borderLessButton
from basicFuncs import *
from basicDialogs import dlgInputNumber

class dlgMotorTunning(QDialog):
    def __init__(self, cnc, parent=None):
        super(dlgMotorTunning, self).__init__(parent)

        self.cnc = cnc

        self.cnc.readConfig()

        self.lang = cLanguage()
        
        # Create widgets
        self.setFont(QFont('SansSerif', 14))
        self.setStyleSheet("QDialog {background-color: #232234;color:#ffffff;}")

        lblSteps = QLabel(self.lang.tr("Resolution"))
        lblSteps.setStyleSheet(labelStyle)
        self.txtStepsX = QLineEdit( '%.4f' % self.cnc.axis[0].resolution)
        self.txtStepsX.setStyleSheet( lineEditStyle )
        self.txtStepsX.installEventFilter( self )
        self.txtStepsY = QLineEdit('%.4f ' % self.cnc.axis[1].resolution)
        self.txtStepsY.setStyleSheet( lineEditStyle )
        self.txtStepsY.installEventFilter( self )
        self.txtStepsZ = QLineEdit( '%.4f ' % self.cnc.axis[2].resolution)
        self.txtStepsZ.setStyleSheet( lineEditStyle )
        self.txtStepsZ.installEventFilter( self )
        self.txtStepsA = QLineEdit('%.4f ' % self.cnc.axis[3].resolution)
        self.txtStepsA.setStyleSheet( lineEditStyle )
        self.txtStepsA.installEventFilter( self )
        
        lblSpeed = QLabel(self.lang.tr("Speed"))
        lblSpeed.setStyleSheet(labelStyle)
        self.txtSpeedX = QLineEdit(str(self.cnc.axis[0].maxSpeed))
        self.txtSpeedX.setStyleSheet( lineEditStyle )
        self.txtSpeedX.installEventFilter( self )
        self.txtSpeedY = QLineEdit(str(self.cnc.axis[1].maxSpeed))
        self.txtSpeedY.setStyleSheet( lineEditStyle )
        self.txtSpeedY.installEventFilter( self )
        self.txtSpeedZ = QLineEdit(str(self.cnc.axis[2].maxSpeed))
        self.txtSpeedZ.setStyleSheet( lineEditStyle )
        self.txtSpeedZ.installEventFilter( self )
        self.txtSpeedA = QLineEdit(str(self.cnc.axis[3].maxSpeed))
        self.txtSpeedA.setStyleSheet( lineEditStyle )
        self.txtSpeedA.installEventFilter( self )
        
        lblAccel = QLabel(self.lang.tr("Accel."))
        lblAccel.setStyleSheet(labelStyle)
        self.txtAccelX = QLineEdit(str(self.cnc.axis[0].acceleration))
        self.txtAccelX.setStyleSheet( lineEditStyle )
        self.txtAccelX.installEventFilter( self )
        self.txtAccelY = QLineEdit(str(self.cnc.axis[1].acceleration))
        self.txtAccelY.setStyleSheet( lineEditStyle )
        self.txtAccelY.installEventFilter( self )
        self.txtAccelZ = QLineEdit(str(self.cnc.axis[2].acceleration))
        self.txtAccelZ.setStyleSheet( lineEditStyle )
        self.txtAccelZ.installEventFilter( self )
        self.txtAccelA = QLineEdit(str(self.cnc.axis[3].acceleration))
        self.txtAccelA.setStyleSheet( lineEditStyle )
        self.txtAccelA.installEventFilter( self )
        
        lblAxis = QLabel("Type")
        lblAxis.setStyleSheet(labelStyle)
        self.comboTypeX = QComboBox()
        self.comboTypeX.setStyleSheet(comboStyle)
        self.comboTypeY = QComboBox()
        self.comboTypeY.setStyleSheet(comboStyle)
        self.comboTypeZ = QComboBox()
        self.comboTypeZ.setStyleSheet(comboStyle)
        self.comboTypeA = QComboBox()
        self.comboTypeA.setStyleSheet(comboStyle)
        i=0
        for item in [self.comboTypeX, self.comboTypeY, self.comboTypeZ, self.comboTypeA]:
            item.addItem("Linear")
            item.addItem("Angular")

            if self.cnc.axis[i].linear == True:
                self.comboTypeX.setCurrentIndex(0)
            else:
                self.comboTypeX.setCurrentIndex(1)


        lblJogFast = QLabel(self.lang.tr("Jog Fast"))
        lblJogFast.setStyleSheet(labelStyle)
        self.txtJogFastX = QLineEdit(str(self.cnc.axis[0].jogFastSpeed))
        self.txtJogFastX.setStyleSheet( lineEditStyle )
        self.txtJogFastX.installEventFilter( self )
        self.txtJogFastY = QLineEdit(str(self.cnc.axis[1].jogFastSpeed))
        self.txtJogFastY.setStyleSheet( lineEditStyle )
        self.txtJogFastY.installEventFilter( self )
        self.txtJogFastZ = QLineEdit(str(self.cnc.axis[2].jogFastSpeed))
        self.txtJogFastZ.setStyleSheet( lineEditStyle )
        self.txtJogFastZ.installEventFilter( self )
        self.txtJogFastA = QLineEdit(str(self.cnc.axis[3].jogFastSpeed))
        self.txtJogFastA.setStyleSheet( lineEditStyle )
        self.txtJogFastA.installEventFilter( self )

        lblJogSlow = QLabel(self.lang.tr("Jog Slow"))
        lblJogSlow.setStyleSheet(labelStyle)
        self.txtJogSlowX = QLineEdit(str(self.cnc.axis[0].jogSlowSpeed))
        self.txtJogSlowX.setStyleSheet( lineEditStyle )
        self.txtJogSlowX.installEventFilter( self )
        self.txtJogSlowY = QLineEdit(str(self.cnc.axis[1].jogSlowSpeed))
        self.txtJogSlowY.setStyleSheet( lineEditStyle )
        self.txtJogSlowY.installEventFilter( self )
        self.txtJogSlowZ = QLineEdit(str(self.cnc.axis[2].jogSlowSpeed))
        self.txtJogSlowZ.setStyleSheet( lineEditStyle )
        self.txtJogSlowZ.installEventFilter( self )
        self.txtJogSlowA = QLineEdit(str(self.cnc.axis[3].jogSlowSpeed))
        self.txtJogSlowA.setStyleSheet( lineEditStyle )
        self.txtJogSlowA.installEventFilter( self )
        
        lblStepS = QLabel(self.lang.tr("Step Sense"))
        lblStepS.setStyleSheet(labelStyle)
        lblDirS = QLabel(self.lang.tr("Dir. Sense"))
        lblDirS.setStyleSheet(labelStyle)
        self.comboStepX = QComboBox()
        self.comboStepY = QComboBox()
        self.comboStepZ = QComboBox()
        self.comboStepA = QComboBox()
        self.comboDirX = QComboBox()
        self.comboDirY = QComboBox()
        self.comboDirZ = QComboBox()
        self.comboDirA = QComboBox()
        combos = [self.comboStepX, self.comboStepY, self.comboStepZ, self.comboStepA, self.comboDirX, self.comboDirY, self.comboDirZ, self.comboDirA]
        i = 0
        for item in combos:
            item.addItem("0")
            item.addItem("1")
            item.addItem("OFF")

            if i < 4:
                if self.cnc.axis[i].stepOutput.sense <= 2:
                    item.setCurrentIndex(self.cnc.axis[i].stepOutput.sense)
            else:
                if self.cnc.axis[i-4].dirOutput.sense == 0:
                    item.setCurrentIndex(0)
                else:
                    if self.cnc.axis[i-4].dirOutput.sense == 1:
                        item.setCurrentIndex(1)
                    else:
                        item.setCurrentIndex(2)

            i += 1

        itemDelegate = QStyledItemDelegate()
        
        self.comboStepX.setStyleSheet(comboStyle)
        self.comboStepX.setItemDelegate(itemDelegate)
        self.comboStepY.setStyleSheet(comboStyle)
        self.comboStepY.setItemDelegate(itemDelegate)
        self.comboStepZ.setStyleSheet(comboStyle)
        self.comboStepZ.setItemDelegate(itemDelegate)
        self.comboStepA.setStyleSheet(comboStyle)
        self.comboStepA.setItemDelegate(itemDelegate)

        self.comboDirX.setStyleSheet(comboStyle)
        self.comboDirX.setItemDelegate(itemDelegate)
        self.comboDirY.setStyleSheet(comboStyle)
        self.comboDirY.setItemDelegate(itemDelegate)
        self.comboDirZ.setStyleSheet(comboStyle)
        self.comboDirZ.setItemDelegate(itemDelegate)
        self.comboDirA.setStyleSheet(comboStyle)
        self.comboDirA.setItemDelegate(itemDelegate)
                        
        lblPulseW = QLabel(self.lang.tr("Pulse width"))
        lblPulseW.setStyleSheet(labelStyle)
        self.txtPulseWX = QLineEdit(str(self.cnc.axis[0].pulseWidth))
        self.txtPulseWX.setStyleSheet( lineEditStyle )
        self.txtPulseWX.installEventFilter( self )
        self.txtPulseWY = QLineEdit(str(self.cnc.axis[1].pulseWidth))
        self.txtPulseWY.setStyleSheet( lineEditStyle )
        self.txtPulseWY.installEventFilter( self )
        self.txtPulseWZ = QLineEdit(str(self.cnc.axis[2].pulseWidth))
        self.txtPulseWZ.setStyleSheet( lineEditStyle )
        self.txtPulseWZ.installEventFilter( self )
        self.txtPulseWA = QLineEdit(str(self.cnc.axis[3].pulseWidth))
        self.txtPulseWA.setStyleSheet( lineEditStyle )
        self.txtPulseWA.installEventFilter( self )
        
        lblDirW = QLabel(self.lang.tr("Dir. width"))
        lblDirW.setStyleSheet(labelStyle)
        self.txtDirWX = QLineEdit(str(self.cnc.axis[0].dirWidth))
        self.txtDirWX.setStyleSheet( lineEditStyle )
        self.txtDirWX.installEventFilter( self )
        self.txtDirWY = QLineEdit(str(self.cnc.axis[1].dirWidth))
        self.txtDirWY.setStyleSheet( lineEditStyle )
        self.txtDirWY.installEventFilter( self )
        self.txtDirWZ = QLineEdit(str(self.cnc.axis[2].dirWidth))
        self.txtDirWZ.setStyleSheet( lineEditStyle )
        self.txtDirWZ.installEventFilter( self )
        self.txtDirWA = QLineEdit(str(self.cnc.axis[3].dirWidth))
        self.txtDirWA.setStyleSheet( lineEditStyle )
        self.txtDirWA.installEventFilter( self )
        
        lblEncoder = QLabel(self.lang.tr("Encoder"))
        lblEncoder.setStyleSheet(labelStyle)
        self.txtEncoderX = QLineEdit('%.3f ' % self.cnc.axis[0].encoder)
        self.txtEncoderX.setStyleSheet( lineEditStyle )
        self.txtEncoderX.installEventFilter( self )
        self.txtEncoderY = QLineEdit('%.3f ' % self.cnc.axis[1].encoder)
        self.txtEncoderY.setStyleSheet( lineEditStyle )
        self.txtEncoderY.installEventFilter( self )
        self.txtEncoderZ = QLineEdit('%.3f ' % self.cnc.axis[2].encoder)
        self.txtEncoderZ.setStyleSheet( lineEditStyle )
        self.txtEncoderZ.installEventFilter( self )
        self.txtEncoderA = QLineEdit('%.3f ' % self.cnc.axis[3].encoder)
        self.txtEncoderA.setStyleSheet( lineEditStyle )
        self.txtEncoderA.installEventFilter( self )

        lblX = QLabel()
        lblX.setPixmap(QPixmap("iconInputX"))
        lblY = QLabel()
        lblY.setPixmap(QPixmap("iconInputY"))
        lblZ = QLabel()
        lblZ.setPixmap(QPixmap("iconInputZ"))
        lblA = QLabel()
        lblA.setPixmap(QPixmap("iconInputA"))

        self.txtWidgets = [self.txtStepsX, self.txtStepsY, self.txtStepsZ, self.txtStepsA,
                          self.txtSpeedX, self.txtSpeedY, self.txtSpeedZ, self.txtSpeedA,
                          self.txtAccelX, self.txtAccelY, self.txtAccelZ, self.txtAccelA,
                          self.txtJogFastX, self.txtJogFastY, self.txtJogFastZ, self.txtJogFastA,
                          self.txtJogSlowX, self.txtJogSlowY, self.txtJogSlowZ, self.txtJogSlowA,
                          self.txtPulseWX, self.txtPulseWY, self.txtPulseWZ, self.txtPulseWA,
                          self.txtDirWX, self.txtDirWY, self.txtDirWZ, self.txtDirWA,
                          self.txtEncoderX, self.txtEncoderY, self.txtEncoderZ, self.txtEncoderA]

        self.combos = [self.comboStepX, self.comboStepY, self.comboStepZ, self.comboStepA,
                       self.comboDirX, self.comboDirY, self.comboDirZ, self.comboDirA]
        
        btnOk = borderLessButton( self.lang.tr("save"), "iconOk.png")
        btnOk.clicked.connect(self.handleOk)
        
        btnCancel = borderLessButton( self.lang.tr("cancel"), "iconCancel.png")
        btnCancel.clicked.connect(self.close)
                
        grid = QGridLayout()
        grid.setSpacing(2)

        grid.addWidget(lblX, 0, 1)
        grid.addWidget(lblY, 0, 2)
        grid.addWidget(lblZ, 0, 3)
        grid.addWidget(lblA, 0, 4)
        
        grid.addWidget(lblSteps, 1, 0)
        grid.addWidget(self.txtStepsX, 1, 1)
        grid.addWidget(self.txtStepsY, 1, 2)
        grid.addWidget(self.txtStepsZ, 1, 3)
        grid.addWidget(self.txtStepsA, 1, 4)
        
        grid.addWidget(lblSpeed, 2, 0)
        grid.addWidget(self.txtSpeedX, 2, 1)
        grid.addWidget(self.txtSpeedY, 2, 2)
        grid.addWidget(self.txtSpeedZ, 2, 3)
        grid.addWidget(self.txtSpeedA, 2, 4)
        
        grid.addWidget(lblAccel, 3, 0)
        grid.addWidget(self.txtAccelX, 3, 1)
        grid.addWidget(self.txtAccelY, 3, 2)
        grid.addWidget(self.txtAccelZ, 3, 3)
        grid.addWidget(self.txtAccelA, 3, 4)

        '''
        grid.addWidget(lblAxis, 3, 0)
        grid.addWidget(comboTypeX, 3, 1)
        grid.addWidget(comboTypeY, 3, 2)
        grid.addWidget(comboTypeZ, 3, 3)
        grid.addWidget(comboTypeA, 3, 4)
        '''
        
        grid.addWidget(lblJogFast, 4, 0)
        grid.addWidget(self.txtJogFastX, 4, 1)
        grid.addWidget(self.txtJogFastY, 4, 2)
        grid.addWidget(self.txtJogFastZ, 4, 3)
        grid.addWidget(self.txtJogFastA, 4, 4)

        grid.addWidget(lblJogSlow, 5, 0)
        grid.addWidget(self.txtJogSlowX, 5, 1)
        grid.addWidget(self.txtJogSlowY, 5, 2)
        grid.addWidget(self.txtJogSlowZ, 5, 3)
        grid.addWidget(self.txtJogSlowA, 5, 4)
        
        grid.addWidget(lblStepS, 6, 0)
        grid.addWidget(self.comboStepX, 6, 1)
        grid.addWidget(self.comboStepY, 6, 2)
        grid.addWidget(self.comboStepZ, 6, 3)
        grid.addWidget(self.comboStepA, 6, 4)
        
        grid.addWidget(lblDirS, 7, 0)
        grid.addWidget(self.comboDirX, 7, 1)
        grid.addWidget(self.comboDirY, 7, 2)
        grid.addWidget(self.comboDirZ, 7, 3)
        grid.addWidget(self.comboDirA, 7, 4)
        
        grid.addWidget(lblPulseW, 8, 0)
        grid.addWidget(self.txtPulseWX, 8, 1)
        grid.addWidget(self.txtPulseWY, 8, 2)
        grid.addWidget(self.txtPulseWZ, 8, 3)
        grid.addWidget(self.txtPulseWA, 8, 4)
        
        grid.addWidget(lblDirW, 9, 0)
        grid.addWidget(self.txtDirWX, 9, 1)
        grid.addWidget(self.txtDirWY, 9, 2)
        grid.addWidget(self.txtDirWZ, 9, 3)
        grid.addWidget(self.txtDirWA, 9, 4)
        
        grid.addWidget(lblEncoder, 10, 0)
        grid.addWidget(self.txtEncoderX, 10, 1)
        grid.addWidget(self.txtEncoderY, 10, 2)
        grid.addWidget(self.txtEncoderZ, 10, 3)
        grid.addWidget(self.txtEncoderA, 10, 4)
        
        grid.addWidget(btnCancel, 11, 2)
        grid.addWidget(btnOk, 11, 3)

        self.setLayout(grid)
        
        if develPlatform() == True:
            self.setGeometry(50, 50, screenWidth, screenHeight)
        else:
            self.setGeometry(0,0, screenWidth, screenHeight)

    def handleOk(self):

        for i in range(0,4):
            value = float(self.txtWidgets[i].text())
            if self.cnc.axis[i].resolution != value:
                print("Cambio res "+str(i))
                param = "config.axis["+str(i)+"].StepsByUnit"
                self.cnc.saveConfig(param, str(value))

            value = int( self.txtWidgets[4+i].text() )
            if self.cnc.axis[i].maxSpeed != value:
                print("Cambio speed "+str(i))
                param = "config.axis["+str(i)+"].Speed"
                self.cnc.saveConfig(param, str(value))

            value = int( self.txtWidgets[8+i].text())
            if self.cnc.axis[i].acceleration != value:
                print("Cambio accel "+str(i))
                param = "config.axis["+str(i)+"].Acceleration"
                self.cnc.saveConfig(param, str(value))
                
            value = int( self.txtWidgets[12+i].text() )
            if self.cnc.axis[i].jogFastSpeed != value:
                print("Cambio jog fast "+str(i))
                param = "config.axis["+str(i)+"].JogFastSpeed"
                self.cnc.saveConfig(param, str(value))

            value = int( self.txtWidgets[16+i].text() )
            if self.cnc.axis[i].jogSlowSpeed != value:
                print("Cambio jog slow "+str(i))
                param = "config.axis["+str(i)+"].JogSlowSpeed"
                self.cnc.saveConfig(param, str(value))

            value = int( self.txtWidgets[20+i].text() )
            if self.cnc.axis[i].pulseWidth != value:
                print("Cambio pulse width "+str(i))
                param = "config.axis["+str(i)+"].PulseWidth"
                self.cnc.saveConfig(param, str(value))

            value = int( self.txtWidgets[24+i].text() )
            if self.cnc.axis[i].dirWidth != value:
                print("Cambio dir width "+str(i))
                param = "config.axis["+str(i)+"].DirectionWidth"
                self.cnc.saveConfig(param, str(value))

            value = float( self.txtWidgets[28+i].text() )
            if self.cnc.axis[i].encoder != value:
                print("Cambio encoder "+str(i))
                param = "config.axis["+str(i)+"].Encoder"
                self.cnc.saveConfig(param, str(value))

            value = self.combos[i].currentIndex()
            if self.cnc.axis[i].stepOutput.sense  != value:
                print("Cambio step sense "+str(i))
                param = "config.axis["+str(i)+"].StepActiveLow"
                self.cnc.saveConfig(param, str(value))

            value = self.combos[4+i].currentIndex()
            if self.cnc.axis[i].dirOutput.sense  != value:
                print("Cambio dir sense "+str(i))
                param = "config.axis["+str(i)+"].DirActiveLow"
                self.cnc.saveConfig(param, str(value))

        self.close()
        
    def eventFilter( self, widget, event):
        if event.type() == QEvent.MouseButtonPress:

            if widget in self.txtWidgets:
                col = self.txtWidgets.index(widget) % 4
                print("col:"+str(col))
                if col == 0:
                    xpos = 290
                else:
                    if col == 1:
                        xpos = 400
                    else:
                        if col == 2:
                            xpos = 190
                        else:
                            xpos = 350
                            
                dialog = dlgInputNumber(pos=(xpos,50), widg=widget)
                dialog.setModal(True)
                dialog.show()
                    
                dialog.exec_()
                #widget.setText( dialog.value() )

        return QWidget.eventFilter(self, widget, event)
