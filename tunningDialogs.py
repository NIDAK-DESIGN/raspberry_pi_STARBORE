# -*- coding: cp1252 -*-
from PySide.QtGui import QDialog, QFont, QPixmap, QGridLayout, QLabel, QLineEdit, QGroupBox, QRadioButton, QHBoxLayout, QPushButton, QWidget
from PySide.QtCore import *
from controls import borderLessButton
from basicFuncs import *
from basicDialogs import dlgInputNumber

class dlgGralParams(QDialog):
    def __init__(self, cnc, parent=None):
        super(dlgGralParams, self).__init__(parent)

        self.cnc = cnc
        self.cnc.readConfig()
        
        # Create widgets
        self.setFont(QFont('SansSerif', 14))
        self.setStyleSheet("QDialog {background-color: #232234;color:#ffffff;}")

        lblArc = QLabel("ARCSYSFACTOR")
        lblArc.setStyleSheet(labelStyle)
        self.txtArc = QLineEdit("")
        self.txtArc.setText(str(self.cnc.arcSysFactor))
        self.txtArc.installEventFilter( self )
        
        lblLED = QLabel("LED REF")
        lblLED.setStyleSheet(labelStyle)
        self.ledGroup = createNIConfigGroup()

        buttons = self.ledGroup.findChildren(QRadioButton)
        if self.cnc.ledRef == 0:
            buttons[0].setChecked(True)
        else:
            buttons[1].setChecked(True)
        
        lblEncoderTimeout = QLabel("ENCODER TIMEOUT")
        lblEncoderTimeout.setStyleSheet(labelStyle)
        self.txtEncoderTimeout = QLineEdit(str(self.cnc.encoderTimeout))
        self.txtEncoderTimeout.installEventFilter( self )
        lblEncTimeoutUnits = QLabel("ms")
        lblEncTimeoutUnits.setStyleSheet(labelStyle)
        
        lblEncoderError = QLabel("ENCODER ERROR")
        lblEncoderError.setStyleSheet(labelStyle)
        self.txtEncoderError = QLineEdit(str(self.cnc.encoderError))
        self.txtEncoderError.installEventFilter( self )
        lblEncErrorUnits = QLabel("%")
        lblEncErrorUnits.setStyleSheet(labelStyle)
        
        lblGreaseAlert = QLabel("AVISO ENGRASE")
        lblGreaseAlert.setStyleSheet(labelStyle)
        self.txtGreaseAlert = QLineEdit(str(self.cnc.avisoEngrase))
        self.txtGreaseAlert.installEventFilter( self )
        lblGreaseAlertUnits = QLabel("h")
        lblGreaseAlertUnits.setStyleSheet(labelStyle)
        
        lblGrease2 = QLabel("INTER. ENGRASE")
        lblGrease2.setStyleSheet(labelStyle)
        self.txtGreaseInterval = QLineEdit(str(self.cnc.autogreaseMinutes))
        self.txtGreaseInterval.installEventFilter( self )
        lblGreaseIntervalUnits = QLabel("min")
        lblGreaseIntervalUnits.setStyleSheet(labelStyle)
        
        lblGrease3 = QLabel("TIEMPO ENGRASE")
        lblGrease3.setStyleSheet(labelStyle)
        self.txtGreaseTime = QLineEdit(str(self.cnc.autogreaseSeconds))
        self.txtGreaseTime.installEventFilter( self )
        lblGreaseTimeUnits = QLabel("s")
        lblGreaseTimeUnits.setStyleSheet(labelStyle)

        self.txtWidgets = [self.txtArc, self.txtEncoderTimeout, self.txtEncoderError,
                           self.txtGreaseAlert, self.txtGreaseInterval, self.txtGreaseTime]
        
        btnOk = borderLessButton("save", "iconOk.png")
        btnOk.clicked.connect(self.handleOk)
        
        btnCancel = borderLessButton("cancel", "iconCancel.png")
        btnCancel.clicked.connect(self.close)

        grid = QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(lblArc, 0, 0)
        grid.addWidget(self.txtArc, 0, 1)
        
        grid.addWidget(lblLED, 1, 0)
        grid.addWidget(self.ledGroup, 1, 1)
        
        grid.addWidget(lblEncoderTimeout, 2, 0)
        grid.addWidget(self.txtEncoderTimeout, 2, 1)
        grid.addWidget(lblEncTimeoutUnits, 2, 2)
        
        grid.addWidget(lblEncoderError, 3, 0)
        grid.addWidget(self.txtEncoderError, 3, 1)
        grid.addWidget(lblEncErrorUnits, 3, 2)

        '''
        grid.addWidget(lblGreaseAlert, 4, 0)
        grid.addWidget(self.txtGreaseAlert, 4, 1)
        grid.addWidget(lblGreaseAlertUnits, 4, 2)
        '''
        
        grid.addWidget(lblGrease2, 5, 0)
        grid.addWidget(self.txtGreaseInterval, 5, 1)
        grid.addWidget(lblGreaseIntervalUnits, 5, 2)
        
        grid.addWidget(lblGrease3, 6, 0)
        grid.addWidget(self.txtGreaseTime, 6, 1)
        grid.addWidget(lblGreaseTimeUnits, 6, 2)
        
        grid.addWidget(btnCancel, 7, 0)
        grid.addWidget(btnOk, 7, 1)
        
        self.setLayout(grid)
        if develPlatform() == True:
            self.setGeometry(50, 50, screenWidth, screenHeight)
        else:
            self.setGeometry(0,0, screenWidth, screenHeight)

    def eventFilter( self, widget, event):
        if event.type() == QEvent.MouseButtonPress:
                          
            dialog = dlgInputNumber(pos=(290,50), widg=widget)
            dialog.show()
                    
            dialog.exec_()

        return QWidget.eventFilter(self, widget, event)
    
    def handleOk(self):

        # Enviamos sólo los comandos de las cosas que hayan cambiado
        # ArcSysFacto
        if float(self.txtArc.text()) != self.cnc.arcSysFactor:
            tmps = "config.system.ArcSysFactor " +self.txtArc.text()
            print("Change param: "+tmps)
            param = "config.system.ArcSysFactor"
            value = self.txtArc.text()
            self.cnc.saveConfig(param, value)

        # LED REF
        buttons = self.ledGroup.findChildren(QRadioButton)
        if buttons[0].isChecked():
            ledRef = 0
        else:
            ledRef = 1
            
        if self.cnc.ledRef != ledRef:
            param = "config.system.LedRef"
            value = str(ledRef)
            print("Change param: "+param+" "+value)
            self.cnc.saveConfig(param, value)

        # ENCODER TIMEOUT
        if int(self.txtEncoderTimeout.text()) != self.cnc.encoderTimeout:
            param = "config.EncoderTimeout"
            value = self.txtEncoderTimeout.text()
            print("Change param: "+param+" "+value)
            self.cnc.saveConfig(param, value)

        # ENCODER ERROR
        value = float(self.txtEncoderError.text())
        if value != self.cnc.encoderError:
            param = "config.EncoderErr"
            print("Change param: "+param+" "+str(value))
            self.cnc.saveConfig(param, value)

        # AVISO ENGRASE
        '''
        value = int(self.txtEncoderError.text())
        if value != self.cnc.encoderError:
            param = "config.EncoderErr"
            print("Change param: "+param+" "+str(value))
            self.cnc.saveConfig(param, value)
        '''

        # INTERVALO ENGRASE
        value = int(self.txtGreaseInterval.text())
        if  value != self.cnc.autogreaseMinutes:
            param = "config.autogreaseMinutes"
            print("Change param: "+param+" "+str(value))
            self.cnc.saveConfig(param, value)

        # TIEMPO ENGRASE
        value = int(self.txtGreaseTime.text())
        if value != self.cnc.autogreaseSeconds:
            param = "config.autogreaseSeconds"
            print("Change param: "+param+" " + str(value))
            self.cnc.saveConfig(param, value)

        self.close()
        
