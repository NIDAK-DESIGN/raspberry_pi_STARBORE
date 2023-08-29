from PySide.QtGui import QDialog, QFont, QGridLayout, QGroupBox, QPixmap, QLabel, QWidget, QHBoxLayout, QVBoxLayout
from PySide.QtCore import *
from controls import borderLessButton
from basicFuncs import *
import time

class dlgInputNumber(QDialog):
    def __init__(self,  widg=None, parent=None, pos=(0,0), frmt=None):
        super(dlgInputNumber, self).__init__(parent)

        if widg is not None:
            self.currValue = widg.text()
            self.widget = widg
        else:
            self.currValue = 0
            self.widget = None

        self.lblFrmt = frmt

        self.strValue = ""
        self.sign = 1

        self.setStyleSheet("QDialog {background-color: #232234;color:#ffffff;}")
        self.setWindowFlags( Qt.FramelessWindowHint )
        
        
        
        # Create widgets
        self.setFont(QFont('SansSerif', 14))

        btnOk = borderLessButton("", "iconOk48.png")
        btnOk.clicked.connect( self.close )

        btnCancel = borderLessButton("", "iconCancel48.png")
        btnCancel.clicked.connect( self.handleCancel )
        
        btn0 = borderLessButton("", "icon0.png")
        btn0.clicked.connect( self.handle0 )
        btn0.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
        btn1 = borderLessButton("", "icon1.png")
        btn1.clicked.connect( self.handle1 )
        btn1.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
        btn2 = borderLessButton("", "icon2.png")
        btn2.clicked.connect( self.handle2 )
        btn2.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
        btn3 = borderLessButton("", "icon3.png")
        btn3.clicked.connect( self.handle3 )
        btn3.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
        btn4 = borderLessButton("", "icon4.png")
        btn4.clicked.connect( self.handle4 )
        btn4.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
        btn5 = borderLessButton("", "icon5.png")
        btn5.clicked.connect( self.handle5 )
        btn5.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
        btn6 = borderLessButton("", "icon6.png")
        btn6.clicked.connect( self.handle6 )
        btn6.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
        btn7 = borderLessButton("", "icon7.png")
        btn7.clicked.connect( self.handle7 )
        btn7.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
        btn8 = borderLessButton("", "icon8.png")
        btn8.clicked.connect( self.handle8 )
        btn8.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
        btn9 = borderLessButton("", "icon9.png")
        btn9.clicked.connect( self.handle9 )
        btn9.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
        btnSign = borderLessButton("", "iconSign.png")
        btnSign.clicked.connect( self.handleSign )
        btnSign.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
        btnDot = borderLessButton("", "iconDot.png")
        btnDot.clicked.connect( self.handleDot )
        btnDot.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnBack = borderLessButton("", "iconDel.png")
        btnBack.clicked.connect( self.handleBack )
        btnBack.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
        keypadGroup = QGroupBox()
        keypadBox = QGridLayout()

        keypadBox.addWidget(btn0, 3, 1)
        keypadBox.addWidget(btn1, 0, 0)
        keypadBox.addWidget(btn2, 0, 1)
        keypadBox.addWidget(btn3, 0, 2)
        keypadBox.addWidget(btn4, 1, 0)
        keypadBox.addWidget(btn5, 1, 1)
        keypadBox.addWidget(btn6, 1, 2)
        keypadBox.addWidget(btn7, 2, 0)
        keypadBox.addWidget(btn8, 2, 1)
        keypadBox.addWidget(btn9, 2, 2)
        keypadBox.addWidget(btnSign, 3, 2)
        keypadBox.addWidget(btnDot, 3, 0)
        keypadBox.addWidget(btnBack, 4,1)

        keypadBox.addWidget(btnOk, 5,2)
        keypadBox.addWidget(btnCancel, 5,0)
        
        keypadGroup.setLayout( keypadBox )        
        
        grid = QGridLayout()
        grid.addWidget(keypadGroup, 0, 0)
        
        self.setLayout(grid)
        if develPlatform() == True:
            self.setGeometry(pos[0], pos[1], 260, 300)
        else:
            self.setGeometry(pos[0],pos[1],260,300)
        
    def delayedClose(self):
        self.close()
        
    def handleCancel(self):
        print("cancel"+str(self.currValue))
        if self.widget:
            self.widget.setText(self.currValue)
        self.close()

        self.closeTimer = QTimer(self)
        self.connect(self.closeTimer, SIGNAL("timeout()"), self.delayedClose)
        self.closeTimer.start(100)
        
    def refreshValue(self):
        if self.widget is not None:
            if self.lblFrmt is None:
                if self.sign == 1:
                    value = "+" + self.strValue
                else:
                    value = "-" + self.strValue
            else:
                if (len(self.strValue) > 0):
                    value = self.lblFrmt.format(self.sign * float(self.strValue))
                else:
                    value = ""
            self.widget.setText(value)
            # self.lblValue.setText( "-"+self.strValue )
            # self.lblValue.setText( "+"+self.strValue )

    def setHint(self, h):
        self.hint = h
        self.lblHint.setText( self.hint )
        
    def setValue(self, v):
        self.strValue = str(v)
        self.refreshValue()
        

    def handle0(self):
        self.strValue += "0"
        self.refreshValue()

    def handle1(self):
        self.strValue += "1"
        self.refreshValue()

    def handle2(self):
        self.strValue += "2"
        self.refreshValue()

    def handle3(self):
        self.strValue += "3"
        self.refreshValue()

    def handle4(self):
        self.strValue += "4"
        self.refreshValue()

    def handle5(self):
        self.strValue += "5"
        self.refreshValue()

    def handle6(self):
        self.strValue += "6"
        self.refreshValue()

    def handle7(self):
        self.strValue += "7"
        self.refreshValue()

    def handle8(self):
        self.strValue += "8"
        self.refreshValue()

    def handle9(self):
        self.strValue += "9"
        self.refreshValue()
        

    def handleDot(self):
        if not "." in self.strValue:
            self.strValue += "."
            self.refreshValue()

    def handleSign(self):
        self.sign *= -1
        self.refreshValue()

    def handleBack(self):
        self.strValue = self.strValue[:-1]
        self.refreshValue()

    def value(self):
        if self.sign == 1:
            return self.strValue
        else:
            return "-"+self.strValue


class dlgInputText(QDialog):
    def __init__(self, widg=None, parent=None, pos=(0, 0), frmt=None):
        super(dlgInputText, self).__init__(parent)

        self.shiftActivated = False

        if (frmt is not None):
            self.lblFrmt = frmt
        else:
            self.lblFrmt = "QLabel {color: white; font-size: 24pt}"

        if (widg is not None):
            self.currValue = widg.text()
            self.widget = widg
        else:
            self.currValue = ""
            lblText = QLabel("")
            lblText.setStyleSheet(self.lblFrmt)
            lblLayout = QHBoxLayout()
            lblLayout.addWidget(lblText)
            lblWidget = QWidget()
            lblWidget.setStyleSheet("QWidget {border-left:1px solid white; border-right:1px solid white; border-top:1px solid white; border-bottom:1px solid white;}")
            lblWidget.setLayout(lblLayout)
            self.widget = lblText


        self.strValue = ""
        self.sign = 1

        self.setStyleSheet("QDialog {background-color: #232234;color:#ffffff; border-left:1px solid white; border-right:1px solid white; border-top:1px solid white; border-bottom:1px solid white}")
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Create widgets
        self.setFont(QFont('SansSerif', 14))

        # Fila de numeros

        btn1 = borderLessButton("", "img/chars/1-32.png")
        btn1.clicked.connect(lambda: self.handleChar("1"))
        btn1.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btn2 = borderLessButton("", "img/chars/2-32.png")
        btn2.clicked.connect(lambda: self.handleChar("2"))
        btn2.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btn3 = borderLessButton("", "img/chars/3-32.png")
        btn3.clicked.connect(lambda: self.handleChar("3"))
        btn3.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btn4 = borderLessButton("", "img/chars/4-32.png")
        btn4.clicked.connect(lambda: self.handleChar("4"))
        btn4.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btn5 = borderLessButton("", "img/chars/5-32.png")
        btn5.clicked.connect(lambda: self.handleChar("5"))
        btn5.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btn6 = borderLessButton("", "img/chars/6-32.png")
        btn6.clicked.connect(lambda: self.handleChar("6"))
        btn6.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btn7 = borderLessButton("", "img/chars/7-32.png")
        btn7.clicked.connect(lambda: self.handleChar("7"))
        btn7.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btn8 = borderLessButton("", "img/chars/8-32.png")
        btn8.clicked.connect(lambda: self.handleChar("8"))
        btn8.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btn9 = borderLessButton("", "img/chars/9-32.png")
        btn9.clicked.connect(lambda: self.handleChar("9"))
        btn9.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btn0 = borderLessButton("", "img/chars/0-32.png")
        btn0.clicked.connect(lambda: self.handleChar("0"))
        btn0.setToolButtonStyle(Qt.ToolButtonIconOnly)

        # Primera fila de letras

        btnQ = borderLessButton("", "img/chars/letter-q-32.png")
        btnQ.clicked.connect(lambda: self.handleChar("Q"))
        btnQ.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnW = borderLessButton("", "img/chars/letter-w-32.png")
        btnW.clicked.connect(lambda: self.handleChar("W"))
        btnW.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnE = borderLessButton("", "img/chars/letter-e-32.png")
        btnE.clicked.connect(lambda: self.handleChar("E"))
        btnE.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnR = borderLessButton("", "img/chars/letter-r-32.png")
        btnR.clicked.connect(lambda: self.handleChar("R"))
        btnR.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnT = borderLessButton("", "img/chars/letter-t-32.png")
        btnT.clicked.connect(lambda: self.handleChar("T"))
        btnT.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnY = borderLessButton("", "img/chars/letter-y-32.png")
        btnY.clicked.connect(lambda: self.handleChar("Y"))
        btnY.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnU = borderLessButton("", "img/chars/letter-u-32.png")
        btnU.clicked.connect(lambda: self.handleChar("U"))
        btnU.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnI= borderLessButton("", "img/chars/letter-i-32.png")
        btnI.clicked.connect(lambda: self.handleChar("I"))
        btnI.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnO = borderLessButton("", "img/chars/letter-o-32.png")
        btnO.clicked.connect(lambda: self.handleChar("O"))
        btnO.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnP = borderLessButton("", "img/chars/letter-p-32.png")
        btnP.clicked.connect(lambda: self.handleChar("P"))
        btnP.setToolButtonStyle(Qt.ToolButtonIconOnly)

        # Segunda fila de letras

        btnA = borderLessButton("", "img/chars/letter-a-32.png")
        btnA.clicked.connect(lambda: self.handleChar("A"))
        btnA.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnS = borderLessButton("", "img/chars/letter-s-32.png")
        btnS.clicked.connect(lambda: self.handleChar("S"))
        btnS.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnD = borderLessButton("", "img/chars/letter-d-32.png")
        btnD.clicked.connect(lambda: self.handleChar("D"))
        btnD.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnF = borderLessButton("", "img/chars/letter-f-32.png")
        btnF.clicked.connect(lambda: self.handleChar("F"))
        btnF.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnG = borderLessButton("", "img/chars/letter-g-32.png")
        btnG.clicked.connect(lambda: self.handleChar("G"))
        btnG.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnH = borderLessButton("", "img/chars/letter-h-32.png")
        btnH.clicked.connect(lambda: self.handleChar("H"))
        btnH.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnJ = borderLessButton("", "img/chars/letter-j-32.png")
        btnJ.clicked.connect(lambda: self.handleChar("J"))
        btnJ.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnK = borderLessButton("", "img/chars/letter-k-32.png")
        btnK.clicked.connect(lambda: self.handleChar("K"))
        btnK.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnL = borderLessButton("", "img/chars/letter-l-32.png")
        btnL.clicked.connect(lambda: self.handleChar("L"))
        btnL.setToolButtonStyle(Qt.ToolButtonIconOnly)

        # Segunda fila de letras

        btnZ = borderLessButton("", "img/chars/letter-z-32.png")
        btnZ.clicked.connect(lambda: self.handleChar("Z"))
        btnZ.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnX = borderLessButton("", "img/chars/letter-x-32.png")
        btnX.clicked.connect(lambda: self.handleChar("X"))
        btnX.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnC = borderLessButton("", "img/chars/letter-c-32.png")
        btnC.clicked.connect(lambda: self.handleChar("C"))
        btnC.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnV = borderLessButton("", "img/chars/letter-v-32.png")
        btnV.clicked.connect(lambda: self.handleChar("V"))
        btnV.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnB = borderLessButton("", "img/chars/letter-b-32.png")
        btnB.clicked.connect(lambda: self.handleChar("B"))
        btnB.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnN = borderLessButton("", "img/chars/letter-n-32.png")
        btnN.clicked.connect(lambda: self.handleChar("N"))
        btnN.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnM = borderLessButton("", "img/chars/letter-m-32.png")
        btnM.clicked.connect(lambda: self.handleChar("M"))
        btnM.setToolButtonStyle(Qt.ToolButtonIconOnly)

        # Botones para rellenar
        btnBlank = borderLessButton("", "img/blank-32.png")
        btnM.setToolButtonStyle(Qt.ToolButtonIconOnly)

        # Otros botones de control

        # btnDot = borderLessButton("", "iconDot.png")
        # btnDot.clicked.connect(self.handleDot)
        # btnDot.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnShift = borderLessButton("", "img/chars/arrow-141-32.png") # 141 / 203
        btnShift.clicked.connect(lambda: self.handleShift(btnShift))
        btnShift.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnUnderscore = borderLessButton("", "img/chars/minus-32.png")
        btnUnderscore.clicked.connect(lambda: self.handleChar("_"))
        btnUnderscore.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnSpace = borderLessButton("", "img/chars/myspace-32.png")
        btnSpace.clicked.connect(self.handleSpace)
        btnSpace.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btnBack = borderLessButton("", "img/chars/delete-3-32.png")
        btnBack.clicked.connect(self.handleBack)
        btnBack.setToolButtonStyle(Qt.ToolButtonIconOnly)


        btnOk = borderLessButton("", "iconOk48.png")
        btnOk.clicked.connect(self.close)

        btnCancel = borderLessButton("", "iconCancel48.png")
        btnCancel.clicked.connect(self.handleCancel)

        # Widgets, etc.

        keypadBox = QGridLayout()

        keypadBox.addWidget(btn1, 0, 0)
        keypadBox.addWidget(btn2, 0, 1)
        keypadBox.addWidget(btn3, 0, 2)
        keypadBox.addWidget(btn4, 0, 3)
        keypadBox.addWidget(btn5, 0, 4)
        keypadBox.addWidget(btn6, 0, 5)
        keypadBox.addWidget(btn7, 0, 6)
        keypadBox.addWidget(btn8, 0, 7)
        keypadBox.addWidget(btn9, 0, 8)
        keypadBox.addWidget(btn0, 0, 9)

        keypadBox.addWidget(btnQ, 1, 0)
        keypadBox.addWidget(btnW, 1, 1)
        keypadBox.addWidget(btnE, 1, 2)
        keypadBox.addWidget(btnR, 1, 3)
        keypadBox.addWidget(btnT, 1, 4)
        keypadBox.addWidget(btnY, 1, 5)
        keypadBox.addWidget(btnU, 1, 6)
        keypadBox.addWidget(btnI, 1, 7)
        keypadBox.addWidget(btnO, 1, 8)
        keypadBox.addWidget(btnP, 1, 9)

        keypadBox.addWidget(btnA, 2, 0)
        keypadBox.addWidget(btnS, 2, 1)
        keypadBox.addWidget(btnD, 2, 2)
        keypadBox.addWidget(btnF, 2, 3)
        keypadBox.addWidget(btnG, 2, 4)
        keypadBox.addWidget(btnH, 2, 5)
        keypadBox.addWidget(btnJ, 2, 6)
        keypadBox.addWidget(btnK, 2, 7)
        keypadBox.addWidget(btnL, 2, 8)

        keypadBox.addWidget(btnZ, 3, 0)
        keypadBox.addWidget(btnX, 3, 1)
        keypadBox.addWidget(btnC, 3, 2)
        keypadBox.addWidget(btnV, 3, 3)
        keypadBox.addWidget(btnB, 3, 4)
        keypadBox.addWidget(btnN, 3, 5)
        keypadBox.addWidget(btnM, 3, 6)

        keypadBox.addWidget(btnShift, 4, 1)
        keypadBox.addWidget(btnUnderscore, 4, 3)
        keypadBox.addWidget(btnSpace, 4, 5)
        keypadBox.addWidget(btnBack, 4, 7)


        keypadGroup = QWidget() # QGroupBox()
        keypadGroup.setLayout(keypadBox)

        # Definicion de    lblText (QLabel), lblLayout (QHBoxLayout), self.lblWidget (QWidget)
        # en el INIT de la Class para definir que objeto actualizar

        ctrlLayout = QHBoxLayout()
        ctrlLayout.addWidget(btnOk)
        ctrlLayout.addWidget(btnCancel)
        ctrlWidget = QWidget()
        ctrlWidget.setLayout(ctrlLayout)

        gralLayout = QVBoxLayout()
        gralLayout.addWidget(keypadGroup)
        gralLayout.addWidget(lblWidget)
        gralLayout.addWidget(ctrlWidget)
        gralWidget = QWidget()
        gralWidget.setLayout(gralLayout)

        self.setLayout(gralLayout)
        if develPlatform() == True:
            self.setGeometry(pos[0], pos[1], 260, 300)
        else:
            self.setGeometry(pos[0], pos[1], 260, 300)

    def handleDot(self):
        if not "." in self.strValue:
            self.strValue += "."
            self.refreshValue()

    def handleSpace(self):
        self.strValue += " "
        self.refreshValue()

    def handleShift(self, btn):
        btnShift = btn
        self.shiftActivated = not  self.shiftActivated


        if (self.shiftActivated):
            btnShift.setIcon(QPixmap("img/chars/arrow-203-32.png"))
        else:
            btnShift.setIcon(QPixmap("img/chars/arrow-141-32.png"))
        self.refreshValue()


    def handleBack(self):
        self.strValue = self.strValue[:-1]
        self.refreshValue()

    def handleCancel(self):
        print("cancel"+str(self.currValue))
        if self.widget is not None:
            self.widget.setText(self.currValue)
        self.close()

        #self.closeTimer = QTimer(self)
        #self.connect(self.closeTimer, SIGNAL("timeout()"), self.delayedClose)
        #self.closeTimer.start(100)

    def refreshValue(self):
        if self.widget is not None:
            self.widget.setText(self.strValue)


    def handleChar(self, charPressed):

        if (self.shiftActivated):
            self.strValue += charPressed.upper()
        else:
            self.strValue += charPressed.lower()

        self.refreshValue()

    def value(self):
        return self.strValue


class dlgMessage(QDialog):
    def __init__(self, message, parent=None, pos=(0, 0), frmt=None):
        super(dlgMessage, self).__init__(parent)

        self.shiftActivated = False

        if (frmt is not None):
            self.lblFrmt = frmt
        else:
            self.lblFrmt = "QLabel {color: white; font-size: 14pt}"

        self.setStyleSheet("QDialog {background-color: #232234;color:#ffffff; border-left:1px solid white; border-right:1px solid white; border-top:1px solid white; border-bottom:1px solid white}")
        #self.setStyleSheet(
        #    "QDialog {background-color: #232234;color:#ffffff;}")
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Create widgets
        self.setFont(QFont('SansSerif', 14))

        lblText = QLabel(message)
        lblText.setStyleSheet(self.lblFrmt)
        lblLayout = QHBoxLayout()
        lblLayout.addWidget(lblText)
        lblWidget = QWidget()
        #lblWidget.setStyleSheet(
        #    "QWidget {border-left:1px solid white; border-right:1px solid white; border-top:1px solid white; border-bottom:1px solid white;}")
        lblWidget.setLayout(lblLayout)

        btnOk = borderLessButton("", "iconOk48.png")
        btnOk.clicked.connect(self.handleOk)

        btnCancel = borderLessButton("", "iconCancel48.png")
        btnCancel.clicked.connect(self.handleCancel)

        # Widgets, etc.
        msgLayout = QHBoxLayout()
        msgLayout.addWidget(lblWidget)
        msgWidget = QWidget()
        msgWidget.setLayout(msgLayout)

        ctrlLayout = QHBoxLayout()
        ctrlLayout.addWidget(btnOk)
        ctrlLayout.addWidget(btnCancel)
        ctrlWidget = QWidget()
        ctrlWidget.setLayout(ctrlLayout)

        gralLayout = QVBoxLayout()
        gralLayout.addWidget(msgWidget)
        gralLayout.addWidget(ctrlWidget)
        gralWidget = QWidget()
        gralWidget.setLayout(gralLayout)

        self.setLayout(gralLayout)
        if develPlatform() == True:
            self.setGeometry(pos[0], pos[1], 260, 300)
        else:
            self.setGeometry(pos[0], pos[1], 260, 300)

    def handleOk(self):
        pass
        self.close()

    def handleCancel(self):
        pass
        self.close()
