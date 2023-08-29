# -*- coding: cp1252 -*-
from PySide import QtCore
from PySide.QtGui import QDialog, QFont, QPixmap, QGridLayout, QLabel, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, \
    QFrame, QImage
from PySide.QtCore import *
from controls import borderLessButton, borderLessLCButton, stdCheckBox, numberLabel
from basicDialogs import dlgInputNumber, dlgInputText, dlgMessage
from coms import CNC
from basicFuncs import *

class dlgTAPEditor(QDialog):

    def __init__(self, cnc, ctrlFile, parent=None):
        super(dlgTAPEditor, self).__init__(parent)

        self.setFont(QFont('SansSerif', 16))
        self.setStyleSheet("QDialog {background-color: #232234;color:#ffffff;}")

        self.cnc = cnc
        self.ctrlFile = ctrlFile
        self.lang = cLanguage()

        # Nombre de fichero a ejecutar al salir
        self.retFilename = ""
        self.retRun = False

        self.axisPageOffset = 0
        self.axisCount = self.ctrlFile.YROW_COUNT / 3 # Valor = 4
        self.showEditButton = False

        # Borrar todos los valores
        self.ctrlFile.setAllReferenceValues(0)
        self.ctrlFile.setAllReferenceDepthValues(1)

                # Common elements
        self.iconEdit = QPixmap("img/iconEdit-8-32.png")
        self.iconEditGrayed = QPixmap("img/iconEditGrayed-8-24.png")
        self.iconTrash = QPixmap("img/iconTrash-2-24.png")
        self.iconTrashGrayed = QPixmap("img/iconTrashGrayed-2-24.png")
        self.iconM1 = QPixmap("img/iconM1-48On.fw.png")
        self.iconM2 = QPixmap("img/iconM2-48On.fw.png")
        self.imgCenter = QPixmap("img/Imagen-Centro.jpg")
        self.iconClone = QPixmap("img/copy-24.png")

        self.allPlug = self.ctrlFile.plug

        if not self.ctrlFile.disablePlug:
            self.ctrlFile.setAllReferencePlugValues(self.allPlug)
        self.clone = self.ctrlFile.clone

        self.lblFormat = "QLabel { background-color:none; border:0; color: #ffffff; font-weight: bold; font-size:14pt;}"
        self.lblFormatSpecial = "QLabel { background-color:none; border:0; margin-top:37; color: #ffffff; font-weight: bold; font-size:14pt;}"

        #
        self.btnM1 = borderLessLCButton("", self.iconM1)
        self.btnM2 = borderLessLCButton("", self.iconM2)

        # Código editado por NIDAK 20191210 Creando componentes para la altura
        self.lblAltura = QLabel("Altura")
        self.lblAltura.setStyleSheet(self.lblFormat)

        # Código editado por NIDAK 20191210 Botón de Borrado
        self.btnAlturaTrash = borderLessLCButton("", self.iconTrash)
        self.btnAlturaTrash.clicked.connect(lambda: self.handleTrashAltura())

        # Código editado por NIDAK 20191210 Caja de texto para poner número
        self.btnAlturaPos = numberLabel(0.0, self.lblFormatSpecial, width=100)
        self.btnAlturaPos.mousePressEvent = lambda event: self.handleInputAltura()

        self.lblAlturaMM = QLabel(" mm ")
        self.lblAlturaMM.setStyleSheet(self.lblFormat)

        # Código editado por NIDAK 20191210 Botón de Asignacion
        self.btnAlturaEdit = borderLessLCButton("", self.iconEdit)
        self.btnAlturaEdit.clicked.connect(lambda: self.handleChangeByAltura())

        # Código editado por NIDAK 20191210 Ubicación en pantalla de los componentes
        preHdrBox = createHBox(
            [self.btnM1, self.lblAltura, self.btnAlturaTrash, self.btnAlturaEdit, self.btnAlturaPos, self.lblAlturaMM, self.btnM2], spacing=20, margins=(0, 0, 0, 0))


        preHdrWidget = QFrame()
        preHdrWidget.setLayout(preHdrBox)
        #preHdrWidget.setFixedHeight(50)
        #preHdrWidget.setStyleSheet("margin: 5px; border-left:5px solid white; border-right:5px solid white; border-top:1px solid white; border-bottom:1px solid white")
        #preHdrWidget.setStyleSheet("margin: 0px; border-left:1px solid white; border-right:1px solid white; border-top:1px solid white; border-bottom:1px solid white")
        preHdrWidget.setStyleSheet("margin: 0px; border-top:1px solid white; border-bottom:1px solid white")
        #preHdrWidget.setStyleSheet("background-color: red")

        # Botones para selección Cola y Tarugo "All"

        #self.lblClone = QLabel(self.lang.tr("Clone") + " ")
        #self.lblClone.setStyleSheet(self.lblFormat)
        self.lblClone = QLabel()
        self.lblClone.setPixmap(self.iconClone)
        self.btnClone = stdCheckBox("", self.clone, size=24)
        self.btnClone.stateChanged.connect(self.handleClone)
        self.btnCloneBis = borderLessLCButton("", self.iconClone)
        self.btnCloneBis.clicked.connect(self.handleCloneBis)


        # if not self.ctrlFile.disablePlug:
        #     self.lblPlug = QLabel(self.lang.tr("Plug") + " ")
        #     self.lblPlug.setStyleSheet(self.lblFormat)
        #     self.btnAPlug = stdCheckBox("", self.allPlug, size=24)
        #     self.btnAPlug.stateChanged.connect(self.handleInputPlugAll)
        #
        #     self.lblGlue = QLabel(self.lang.tr("Glue") + " ")
        #     self.lblGlue.setStyleSheet(self.lblFormat)
        #     self.btnGlue = stdCheckBox("", self.ctrlFile.getPutGlueValue(), size=24)
        #     self.btnGlue.stateChanged.connect(self.handleInputGlue)

        #self.lblTrash = QLabel(self.lang.tr("Trash")+" ")

        self.lblInfo = QLabel("[P1] <= 15mm Agujeros-Profundidad [P2] > 15mm")
        self.lblInfo.setStyleSheet(self.lblFormat)
        self.lblSeparator = QLabel()

        self.lblTrash = QLabel()
        self.lblTrash.setStyleSheet(self.lblFormat)
        self.btnTrash = borderLessLCButton("", self.iconTrash)
        self.btnTrash.clicked.connect(self.handleTrash)

        # Filas Yn sub
        self.lblYA = []
        self.btnYATrash = []
        self.btnYAInput = []
        self.lblYApos = []
        self.lblMMA = []
        self.btnYAPlug = []
        self.lblYADepth = []
        self.yAWidget = []
        self.yABox = []


        for i in range(0, self.axisCount):
            j = i + 1
            # Botón para ingresar entrada YA
            self.lblYA.append(QLabel("Y" + str(self.axisPageOffset + j)))
            self.lblYA[i].setStyleSheet(self.lblFormat)
            btn = borderLessLCButton("", self.iconTrash)
            self.assignConnectHandleTrashY(btn, j, 1)
            self.btnYATrash.append(btn)
            btn = borderLessLCButton("", self.iconEdit)
            self.assignConnectHandleInputY(btn, j, 1)
            self.btnYAInput.append(btn)
            lbl = numberLabel(self.ctrlFile.getReferenceValue(j, 1), self.lblFormat, width=100)
            self.assignMousePressEvent(lbl, j, 1)
            self.lblYApos.append(lbl)
            #self.lblYApos[i].mousePressEvent
            self.lblMMA.append(QLabel(" mm "))
            self.lblMMA[i].setStyleSheet(self.lblFormat)

            if not self.ctrlFile.disablePlug:
                chkBox = stdCheckBox("", self.ctrlFile.getReferencePlugValue(j, 1), size=24)
                self.assignConnectHandleInputYPlug(chkBox, j, 1)
                self.btnYAPlug.append(chkBox)

            lblDepth = numberLabel(self.ctrlFile.getReferenceDepthValue(j, 1), self.lblFormat, numFormat="[P{0:1}]")
            self.assignMousePressEventDepth(lblDepth, j, 1)
            self.lblYADepth.append(lblDepth)

            self.yAWidget.append(QWidget())
            if (self.showEditButton):
                if not self.ctrlFile.disablePlug:
                    hBox = createHBox([self.lblYA[i], self.btnYATrash[i], self.btnYAInput[i], self.lblYApos[i], self.lblYADepth[i], self.lblMMA[i], self.btnYAPlug[i]])
                else:
                    hBox = createHBox([self.lblYA[i], self.btnYATrash[i], self.btnYAInput[i], self.lblYApos[i], self.lblYADepth[i], self.lblMMA[i]])
            else:
                if not self.ctrlFile.disablePlug:
                    hBox = createHBox([self.lblYA[i], self.btnYATrash[i], self.lblYApos[i], self.lblYADepth[i], self.lblMMA[i], self.btnYAPlug[i]])
                else:
                    hBox = createHBox([self.lblYA[i], self.btnYATrash[i], self.lblYApos[i], self.lblYADepth[i], self.lblMMA[i]])

            self.yABox.append(hBox)
            self.yAWidget[i].setLayout(self.yABox[i])

        # Filas Yn sub B
        self.lblYB = []
        self.btnYBTrash = []
        self.btnYBInput = []
        self.lblYBpos = []
        self.lblMMB = []
        self.btnYBPlug = []
        self.lblYBDepth = []
        self.yBWidget = []
        self.yBBox = []

        for i in range(0, self.axisCount):
            j = i + 1
            # Botón para ingresar entrada YB
            self.lblYB.append(QLabel("Y" + str(self.axisPageOffset + j)))
            self.lblYB[i].setStyleSheet(self.lblFormat)
            btn = borderLessLCButton("", self.iconTrash)
            self.assignConnectHandleTrashY(btn, j, 2)
            self.btnYBTrash.append(btn)
            btn = borderLessLCButton("", self.iconEdit)
            self.assignConnectHandleInputY(btn, j, 2)
            self.btnYBInput.append(btn)
            lbl = numberLabel(self.ctrlFile.getReferenceValue(j, 2), self.lblFormat, width=100)
            self.assignMousePressEvent(lbl, j, 2)
            self.lblYBpos.append(lbl)
            self.lblMMB.append(QLabel(" mm "))
            self.lblMMB[i].setStyleSheet(self.lblFormat)

            if not self.ctrlFile.disablePlug:
                chkBox = stdCheckBox("", self.ctrlFile.getReferencePlugValue(j, 2), size=24)
                self.assignConnectHandleInputYPlug(chkBox, j, 2)
                self.btnYBPlug.append(chkBox)

            lblDepth = numberLabel(self.ctrlFile.getReferenceDepthValue(j, 2), self.lblFormat, numFormat="[P{0:1}]")
            self.assignMousePressEventDepth(lblDepth, j, 2)
            self.lblYBDepth.append(lblDepth)

            self.yBWidget.append(QWidget())
            if (self.showEditButton):
                if not self.ctrlFile.disablePlug:
                    hBox = createHBox([self.lblYB[i], self.btnYBTrash[i], self.btnYBInput[i], self.lblYBpos[i], self.lblYBDepth[i], self.lblMMB[i], self.btnYBPlug[i]])
                else:
                    hBox = createHBox(
                        [self.lblYB[i], self.btnYBTrash[i], self.btnYBInput[i], self.lblYBpos[i], self.lblYBDepth[i], self.lblMMB[i]])
            else:
                if not self.ctrlFile.disablePlug:
                    hBox = createHBox([self.lblYB[i], self.btnYBTrash[i], self.lblYBpos[i], self.lblYBDepth[i], self.lblMMB[i], self.btnYBPlug[i]])
                else:
                    hBox = createHBox([self.lblYB[i], self.btnYBTrash[i], self.lblYBpos[i], self.lblYBDepth[i], self.lblMMB[i]])

            self.yBBox.append(hBox)
            self.yBWidget[i].setLayout(self.yBBox[i])

        # Botón para guardar valores
        btnRun = borderLessButton("", "icon32Start.png")
        btnRun.clicked.connect(self.handleRun)

        # Botón para guardar valores
        btnSaveFile = borderLessButton("", "img/iconSave-24.png")
        btnSaveFile.clicked.connect(self.handleSaveFile)

        # Botón para guardar como valores
        btnSaveAsFile = borderLessButton("", "img/iconSave-as-24.png")
        btnSaveAsFile.clicked.connect(self.handleSaveAsFile)

        # Botón para paginar down
        btnDownPage = borderLessButton("", "img/arrow-246-32.png")
        btnDownPage.clicked.connect(lambda: self.handlePaging(1))

        # Botón para paginar Up
        btnUpPage = borderLessButton("", "img/arrow-184-32.png")
        btnUpPage.clicked.connect(lambda: self.handlePaging(-1))

        #btnClose = borderLessButton(self.lang.tr("close"), "img/iconDoor-32.fw.png")
        #btnClose.setToolButtonStyle( Qt.ToolButtonTextBesideIcon )
        btnClose = borderLessButton("", "img/iconDoor-32.fw.png")
        btnClose.clicked.connect(self.handleClose)

        if not self.ctrlFile.disablePlug:
            #hdrBox = createHBox(
            #    [self.lblClone, self.btnClone, self.lblPlug, self.btnAPlug, self.lblGlue, self.btnGlue, self.lblTrash,
            #     self.btnTrash, ], spacing=0, margins=(50, 0, 50, 0), alignment=Qt.AlignVCenter)
            hdrBox = createHBox(
                [self.btnCloneBis, self.btnClone, self.lblInfo, self.lblSeparator, self.btnTrash], spacing=0, margins=(50, 0, 50, 0), alignment=Qt.AlignVCenter)
        else:
            #hdrBox = createHBox(
            #    [self.lblClone, self.btnClone, self.lblTrash,
            #     self.btnTrash, ], spacing=0, margins=(50, 0, 50, 0), alignment=Qt.AlignVCenter)
            hdrBox = createHBox(
                [self.btnCloneBis, self.btnClone,
                 self.btnTrash, ], spacing=0, margins=(50, 0, 50, 0), alignment=Qt.AlignVCenter)

        hdrWidget = QWidget()
        hdrWidget.setLayout(hdrBox)


        # AleGodoy confección de axisBox con widgets de Ejes
        axisABoxWidgets = []
        for i in range(0, self.axisCount):
            axisABoxWidgets.append(self.yAWidget[i])
        axisABox = createVBox(axisABoxWidgets, spacing=0, margins=(0, 0, 0, 0))
        # axisAWidget = QFrame()
        axisAWidget = QWidget()
        axisAWidget.setLayout(axisABox)
        # axisAWidget.setStyleSheet("margin: 0px;")

        axisBBoxWidgets = []
        for i in range(0, self.axisCount):
            axisBBoxWidgets.append(self.yBWidget[i])
        axisBBox = createVBox(axisBBoxWidgets, spacing=0, margins=(0, 0, 0, 0))
        # axisBWidget = QFrame()
        axisBWidget = QWidget()
        axisBWidget.setLayout(axisBBox)
        # axisBWidget.setStyleSheet("margin: 0px; border-top:1px solid white; border-bottom:1px solid white")

        #lblMiddle = QLabel(self.lang.tr("Middle"))
        lblMiddle = QLabel()
        lblMiddle.setScaledContents(True)
        lblMiddle.setPixmap(self.imgCenter)
        lblMiddle.setStyleSheet(self.lblFormat)
        axisMBox = createVBox([lblMiddle], spacing=0, margins=(0, 0, 0, 0))
        #axisMBox.setGeometry(QRect(0,0,100, 150))
        #axisMBox.setAlignment(Qt.AlignCenter)
        axisMWidget = QWidget()
        axisMWidget.setLayout(axisMBox)
        axisMWidget.setFixedWidth(100)
        axisMWidget.setStyleSheet("margin: 0px; border-left:1px solid white; border-right:1px solid white; border-top:1px solid white; border-bottom:1px solid white")

        axisBox = createHBox([axisBWidget, axisMWidget, axisAWidget], spacing=0, margins=(0, 0, 0, 0))
        axisWidget = QWidget()
        axisWidget.setLayout(axisBox)

        cntrlBox = createHBox([btnClose, btnDownPage, btnUpPage, btnRun, btnSaveAsFile], spacing=0, margins=(0, 0, 0, 0))
        cntrlWidget = QWidget()
        cntrlWidget.setLayout(cntrlBox)

        centralBox = createVBox([preHdrWidget, hdrWidget, axisWidget, cntrlWidget], spacing=0, margins=(0, 0, 0, 0))

        #centralWidget = QWidget()
        #centralWidget.setLayout(centralBox)
        # centralWidget.setStyleSheet("margin-bottom: 1px; margin-top: 1px;  border-top:1px solid white; border-bottom:1px solid white")

        self.setLayout(centralBox)

        if develPlatform() == True:
            self.setGeometry(50, 50, screenWidth, screenHeight)
        else:
            self.setGeometry(0,0, screenWidth, screenHeight)

        #
        # self.statusBar().showMessage(self.lang.tr("Ready"))
        # self.statusBar().setStyleSheet("color:white;font-size:10pt;font-weight:bold; margin-top:0px;")

        if self.allPlug:
            for i in range(0, self.axisCount):
                self.btnYAPlug[i].setCheckState(Qt.Checked)
                self.btnYBPlug[i].setCheckState(Qt.Checked)

            self.ctrlFile.setAllReferencePlugValues(True)

        if self.clone:
            for i in range(0, self.axisCount):
                self.lblYApos[i].setText(self.lblYBpos[i].text())
                self.lblYADepth[i].setText(self.lblYBDepth[i].text())
                self.btnYAInput[i].setIcon(self.iconEditGrayed)
                self.btnYAInput[i].setEnabled(False)
                self.btnYATrash[i].setIcon(self.iconTrashGrayed)
                self.btnYATrash[i].setEnabled(False)
                if not self.ctrlFile.disablePlug:
                    self.btnYAPlug[i].blockSignals(True)
                    self.btnYAPlug[i].setChecked(self.btnYAPlug[i].isChecked())
                    self.btnYAPlug[i].blockSignals(False)
                    self.btnYAPlug[i].setEnabled(False)

            self.ctrlFile.cloneReferenceValues()
            self.ctrlFile.cloneReferencePlugValues()
            self.ctrlFile.cloneReferenceDepthValues()

    def handleClose(self):
        self.close()

    # Codigo editado por NIDAK 20191210 Evento para escribir numero
    # seleccionado en altura por encima de los 128 mm
    def handleInputAltura(self):
        dialog = dlgInputNumber(pos=(290, 50), widg=None, frmt="{:+6.2f}")
        dialog.show()
        dialog.exec_()
        value = dialog.value()

        self.btnAlturaPos.setText("+0.00")

        if (value is not ""):
            if (float(value) <= 128 or float(value) >= 760):
                #wdg.setText('+0.00')
                userInfo = QMessageBox.warning(self, "VERTIMAQ-CNC", "<font color='#ffffff'>" +
                    self.lang.tr("Incorrect value. Enter greater than 128 and less than 760."), QMessageBox.Ok)
                return
            else:
                self.btnAlturaPos.setText("+" + value)

    # Codigo editado por NIDAK 20191210 Evento para borrar altura
    def handleTrashAltura(self):
        msgBox = QMessageBox()
        msgBox.setInformativeText(self.lang.tr("Do you really want to delete the height value?"))
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.No)
        ret = msgBox.exec_()

        if (ret == QMessageBox.Yes ):
            print("Borrando altura")
            self.btnAlturaPos.setText("+0.00")
            self.lblYBpos[0].setText("+0.00")
            self.lblYApos[0].setText("+0.00")
            self.lblYBpos[1].setText("+0.00")
            self.lblYApos[1].setText("+0.00")
            self.lblYBpos[2].setText("+0.00")
            self.lblYApos[2].setText("+0.00")
            self.btnClone.setChecked(False)
            self.btnYAPlug[0].setChecked(False)
            self.btnYAPlug[1].setChecked(False)
            self.btnYAPlug[2].setChecked(False)
            self.btnYAPlug[3].setChecked(False)
            self.btnAPlug.setChecked(False)
            self.btnGlue.setChecked(False)

        # Devolver resultado de MessageBox por si hay que realizar alguna acción adicional
        return ret

    # Codigo editado por NIDAK 20191210 Evento para
    # escribir 64 mm, altura/2 y altura - 64
    def handleChangeByAltura(self):

        height = self.btnAlturaPos.text()

        if height == "" or float(height) <= 128:
            return

        middle = float(height)/2
        rest = float(height) - 64

        self.lblYBpos[0].setText("+64.00")
        self.lblYApos[0].setText("+64.00")

        self.handleInputAlturaAxis(1, 2, "+64.00")
        self.handleInputAlturaAxis(1, 1, "+64.00")

        self.lblYBpos[1].setText("+" + str(middle))
        self.lblYApos[1].setText("+" + str(middle))

        self.handleInputAlturaAxis(2, 2, "+" + str(middle))
        self.handleInputAlturaAxis(2, 1, "+" + str(middle))

        self.lblYBpos[2].setText("+" + str(rest))
        self.lblYApos[2].setText("+" + str(rest))

        self.handleInputAlturaAxis(3, 2, "+" + str(rest))
        self.handleInputAlturaAxis(3, 1, "+" + str(rest))

        self.btnClone.setChecked(True)

        if not self.ctrlFile.disablePlug:
            self.btnYAPlug[0].setChecked(True)
            self.btnYAPlug[1].setChecked(True)
            self.btnYAPlug[2].setChecked(True)
            self.btnYAPlug[3].setChecked(True)
            self.btnAPlug.setChecked(True)
            self.btnGlue.setChecked(True)

    # Codigo editado por NIDAK 20191210 Evento que valida y
    # salva similar al siguiente
    def handleInputAlturaAxis(self, row, col, value):
        refRow = self.axisPageOffset * self.axisCount + row

        if (self.ctrlFile.isReferenceEditable(refRow,col)):
            if (col == 1):
                wdg = self.lblYApos[row - 1]
                oldValue = self.lblYApos[row - 1].text()
            elif (col == 2):
                wdg = self.lblYBpos[row - 1]
                oldValue = self.lblYBpos[row - 1].text()

            if (value is not ""):

                valCode = self.ctrlFile.validateReferenceValue(refRow, col, float(value))
                if (valCode == 0): # Valor válido
                    self.ctrlFile.setReferenceValue(refRow, col, float(value))
                    if self.clone:
                        self.ctrlFile.setReferenceValue(refRow, self.alternateCol(col), float(value))
                        self.refreshAxisData(self.alternateCol(col))

                elif (valCode == 1): # Valor 0 entre adyacentes no nulos
                    ret  = self.handleTrashY(row, col)
                    if (ret == QMessageBox.No):
                        if (col == 1):
                            self.lblYApos[row - 1].setText(oldValue)
                        elif (col == 2):
                            self.lblYBpos[row - 1].setText(oldValue)

                elif (valCode == 2):
                    pos = self.ctrlFile.findInsertPosReference(col, float(value))
                    self.ctrlFile.insertReferenceValue(pos, refRow, col, float(value))
                    self.refreshAxisData(col)
                    if self.clone:
                        self.refreshAxisData(self.alternateCol(col))

                elif (valCode == 3):
                    pos = self.ctrlFile.findReplacePosReference(refRow, col, float(value))
                    self.ctrlFile.replaceReferenceValue(pos, refRow, col, float(value))
                    self.refreshAxisData(col)
                    if self.clone:
                        self.refreshAxisData(self.alternateCol(col))

                else:
                    userInfo = QMessageBox.question(self, "VERTIMAQ-CNC", self.lang.tr("Skipping values."),
                                                    QMessageBox.Ok)
        else:
            dialog = dlgMessage(self.lang.tr("Field not editable."))
            dialog.open()
            dialog.exec_()

            # userInfo = QMessageBox.question(self, "VERTIMAQ-CNC", , QMessageBox.Ok)

    # AleGodoy Pruebas
    def handleInputY(self, row, col):
        refRow = self.axisPageOffset * self.axisCount + row
        if (self.ctrlFile.isReferenceEditable(refRow,col)):
            if (col == 1):
                wdg = self.lblYApos[row - 1]
                oldValue = self.lblYApos[row - 1].text()
            elif (col == 2):
                wdg = self.lblYBpos[row - 1]
                oldValue = self.lblYBpos[row - 1].text()

            dialog = dlgInputNumber(pos=(290, 50), widg=wdg, frmt="{:+6.2f}")
            dialog.show()
            dialog.exec_()
            value = dialog.value()

            if (value is not ""):

                #Codigo editado por NIDAK 20191122
                #Se encuesta el valor obtenido del dialogo InputNumber (caja para introducir lso dígitos)
                #Para valores menores o igual a 10 y mayores de 760 se devuelve mensaje de Valor incorrecto, se cambia a valor inicial +0.00
                #Y no se hace mas nada en el método
                if (float(value) <= 10 or float(value) >= 700):
                    wdg.setText('+0.00')
                    userInfo = QMessageBox.warning(self, "VERTIMAQ-CNC","<font color='#ffffff'>"+self.lang.tr("Incorrect value. Enter greater than 10 and less than 760."),
                                         QMessageBox.Ok)
                    return

                valCode = self.ctrlFile.validateReferenceValue(refRow, col, float(value))
                if (valCode == 0): # Valor válido
                    self.ctrlFile.setReferenceValue(refRow, col, float(value))
                    if self.clone:
                        self.ctrlFile.setReferenceValue(refRow, self.alternateCol(col), float(value))
                        self.refreshAxisData(self.alternateCol(col))

                elif (valCode == 1): # Valor 0 entre adyacentes no nulos
                    ret  = self.handleTrashY(row, col)
                    if (ret == QMessageBox.No):
                        if (col == 1):
                            self.lblYApos[row - 1].setText(oldValue)
                        elif (col == 2):
                            self.lblYBpos[row - 1].setText(oldValue)

                elif (valCode == 2):
                    pos = self.ctrlFile.findInsertPosReference(col, float(value))
                    self.ctrlFile.insertReferenceValue(pos, refRow, col, float(value))
                    self.refreshAxisData(col)
                    if self.clone:
                        self.refreshAxisData(self.alternateCol(col))

                elif (valCode == 3):
                    pos = self.ctrlFile.findReplacePosReference(refRow, col, float(value))
                    self.ctrlFile.replaceReferenceValue(pos, refRow, col, float(value))
                    self.refreshAxisData(col)
                    if self.clone:
                        self.refreshAxisData(self.alternateCol(col))

                else:
                    userInfo = QMessageBox.question(self, "VERTIMAQ-CNC", self.lang.tr("Skipping values."),
                                                    QMessageBox.Ok)
        else:
            dialog = dlgMessage(self.lang.tr("Field not editable."))
            dialog.open()
            dialog.exec_()

            # userInfo = QMessageBox.question(self, "VERTIMAQ-CNC", , QMessageBox.Ok)

    def handleTrashY(self, row, col):
        refRow = self.axisPageOffset * self.axisCount + row
        msgBox = QMessageBox()
        msgBox.setInformativeText(self.lang.tr("Do you really want to delete this row?"))
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.No)
        ret = msgBox.exec_()
        if (ret == QMessageBox.Yes ):
            print ("Borrando fila " + str(row))
            self.trashRowCol(row, col)

            if self.clone:
                altCol = self.alternateCol(col)
                self.trashRowCol(row, altCol)

            self.ctrlFile.delReferenceValue(refRow, col)
            self.ctrlFile.delReferencePlugValue(refRow, col)

        # Devolver resultado de MessageBox por si hay que realizar alguna acción adicional
        return ret

    def trashRowCol(self, row, col):

        lblYpos = None
        btnYPlug = None

        if col == 1:
            lblYpos = self.lblYApos
            btnYPlug = self.btnYAPlug
        elif col == 2:
            lblYpos = self.lblYBpos
            btnYPlug = self.btnYBPlug

        for i in range(row - 1, self.axisCount - 1):
            lblYpos[i].setText(lblYpos[i + 1].text())
            btnYPlug[i].blockSignals(True)
            btnYPlug[i].setChecked(btnYPlug[i + 1].isChecked())
            btnYPlug[i].blockSignals(False)
        lblYpos[self.axisCount - 1].formatText(
            self.ctrlFile.getReferenceValue((self.axisPageOffset + 1) * self.axisCount + 1, col))
        btnYPlug[self.axisCount - 1].blockSignals(True)
        btnYPlug[self.axisCount - 1].setChecked(
            self.ctrlFile.getReferencePlugValue((self.axisPageOffset + 1) * self.axisCount + 1, col))
        btnYPlug[self.axisCount - 1].blockSignals(False)

    def handleTrash(self):
        msgBox = QMessageBox()
        msgBox.setInformativeText(self.lang.tr("Do you really want to delete all rows?"))
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.No)
        ret = msgBox.exec_()
        if (ret == QMessageBox.Yes):
            self.trashAll()

    def trashAll(self):
        print ("Borrando todas las filas ")

        for i in range(0, self.axisCount):
            self.lblYApos[i].formatText(0)
            self.lblYBpos[i].formatText(0)
            self.lblYADepth[i].formatText(1)
            self.lblYBDepth[i].formatText(1)
            if not self.ctrlFile.disablePlug:
                self.btnYAPlug[i].blockSignals(True)
                if self.allPlug:
                    self.btnYAPlug[i].setCheckState(Qt.Checked)
                else:
                    self.btnYAPlug[i].setCheckState(Qt.Unchecked)
                self.btnYAPlug[i].blockSignals(False)
                self.btnYBPlug[i].blockSignals(True)
                if self.allPlug:
                    self.btnYBPlug[i].setCheckState(Qt.Checked)
                else:
                    self.btnYBPlug[i].setCheckState(Qt.Unchecked)
                self.btnYBPlug[i].blockSignals(False)

        self.ctrlFile.setAllReferenceValues(0)
        self.ctrlFile.setAllReferenceDepthValues(1)

        if not self.ctrlFile.disablePlug:
            self.ctrlFile.setAllReferencePlugValues(self.allPlug)

    def handleInputGlue(self):
        self.ctrlFile.switchPutGlueValue()

    # Control de Tarugos

    def handleInputYPlug(self, row, col):
        refRow = self.axisPageOffset * self.axisCount + row
        self.ctrlFile.switchReferencePlugValue(refRow, col)

        if self.clone:
            rowNdx = row - 1
            if col == 1:
                self.btnYBPlug[rowNdx].blockSignals(True)
                self.btnYBPlug[rowNdx].setChecked(self.btnYAPlug[rowNdx].isChecked())
                self.btnYBPlug[rowNdx].blockSignals(False)

            elif col == 2:
                self.btnYAPlug[rowNdx].blockSignals(True)
                self.btnYAPlug[rowNdx].setChecked(self.btnYBPlug[rowNdx].isChecked())
                self.btnYAPlug[rowNdx].blockSignals(False)


    def handleInputPlugAll(self):
        self.allPlug = not self.allPlug
        if (self.allPlug):
            for i in range(0, self.axisCount):
                self.btnYAPlug[i].setCheckState(Qt.Checked)
                self.btnYBPlug[i].setCheckState(Qt.Checked)

            self.ctrlFile.setAllReferencePlugValues(True)
        else:
            for i in range(0, self.axisCount):
                self.btnYAPlug[i].setCheckState(Qt.Unchecked)
                self.btnYBPlug[i].setCheckState(Qt.Unchecked)

            self.ctrlFile.setAllReferencePlugValues(False)

    def handleInputYDepth(self, row, col):
        refRow = self.axisPageOffset * self.axisCount + row

        if (self.ctrlFile.isReferenceEditable(refRow,col)):
            rowNdx = row - 1
            if col == 1:
                self.lblYADepth[rowNdx].formatText(self.ctrlFile.nextDepthValue(int(self.lblYADepth[rowNdx].text()[2:3])))
                if self.clone:
                    self.lblYBDepth[rowNdx].setText(self.lblYADepth[rowNdx].text())
            else:
                self.lblYBDepth[rowNdx].formatText(self.ctrlFile.nextDepthValue(int(self.lblYBDepth[rowNdx].text()[2:3])))

            self.ctrlFile.switchReferenceDepthValue(refRow, col)

            if self.clone:
                self.ctrlFile.setReferenceDepthValue(refRow, 2, self.ctrlFile.getReferenceDepthValue(refRow, 1))
        else:
            userInfo = QMessageBox.question(self, "VERTIMAQ-CNC", self.lang.tr("Field not editable."), QMessageBox.Ok)

    def handleClone(self):
        self.clone = not self.clone
        self.ctrlFile.clone = self.clone

        if (self.clone):
            for i in range(0, self.axisCount):
                self.lblYApos[i].setText(self.lblYBpos[i].text())
                self.lblYADepth[i].setText(self.lblYBDepth[i].text())
                self.btnYAInput[i].setIcon(self.iconEditGrayed)
                self.btnYAInput[i].setEnabled(False)
                self.btnYATrash[i].setIcon(self.iconTrashGrayed)
                self.btnYATrash[i].setEnabled(False)
                if not self.ctrlFile.disablePlug:
                    self.btnYAPlug[i].blockSignals(True)
                    self.btnYAPlug[i].setChecked(self.btnYAPlug[i].isChecked())
                    self.btnYAPlug[i].blockSignals(False)
                    self.btnYAPlug[i].setEnabled(False)

            self.ctrlFile.cloneReferenceValues()
            self.ctrlFile.cloneReferencePlugValues()
            self.ctrlFile.cloneReferenceDepthValues()
        else:
            for i in range(0, self.axisCount):
                self.btnYAInput[i].setIcon(self.iconEdit)
                self.btnYAInput[i].setEnabled(True)
                self.btnYATrash[i].setIcon(self.iconTrash)
                self.btnYATrash[i].setEnabled(True)
                if not self.ctrlFile.disablePlug:
                    self.btnYAPlug[i].setEnabled(True)

    def handleCloneBis(self):
        self.btnClone.setChecked(not self.clone)

    def buildArray(self, exitTwoCol=False):
        array = []
        for i in range(0, 3):
            ref = float(self.lblYBpos[i].text().replace("+", ""))
            if ref == 0.00:
                continue
            p = str(self.lblYBDepth[i].text()).replace("[", "").replace("]", "")
            emptyRowR = []
            emptyRowR.append(ref)
            emptyRowR.append(p)
            emptyRowR.append('1')
            array.append(emptyRowR)

        if exitTwoCol:
            if self.clone:
                for i in range(3, -1, -1):
                    ref = float(self.lblYBpos[i].text().replace("+", ""))
                    if ref == 0.00:
                        continue
                    p = str(self.lblYBDepth[i].text()).replace("[", "").replace("]", "")
                    emptyRowR = []
                    emptyRowR.append(ref)
                    emptyRowR.append(p)
                    emptyRowR.append('2')
                    array.append(emptyRowR)
            else:
                for i in range(3, -1, -1):
                    ref = float(self.lblYApos[i].text().replace("+", ""))
                    if ref == 0.00:
                        continue
                    p = str(self.lblYADepth[i].text()).replace("[", "").replace("]", "")
                    emptyRowR = []
                    emptyRowR.append(ref)
                    emptyRowR.append(p)
                    emptyRowR.append('2')
                    array.append(emptyRowR)
        else:
            for i in range(0, 3):
                ref = float(self.lblYApos[i].text().replace("+", ""))
                if ref == 0.00:
                    continue
                p = str(self.lblYADepth[i].text()).replace("[", "").replace("]", "")
                emptyRowR = []
                emptyRowR.append(ref)
                emptyRowR.append(p)
                emptyRowR.append('2')
                array.append(emptyRowR)

        return array

    def handleRun(self):
        self.ctrlFile.writeFile()
        #self.ctrlFile.generateCodeFile()

        a = float(self.lblYApos[0].text().replace("+", ""))
        b = float(self.lblYBpos[0].text().replace("+", ""))
        exitM2 = a > 0.00
        exitM1 = b > 0.00
        array = self.buildArray(exitM2 and exitM1);
        if self.retFilename == '':
            self.retFilename = None
        self.ctrlFile.generateCodeFileEditor(self.retFilename, array, exitM1, exitM2)

        self.retRun = True
        self.retFilename = self.ctrlFile.lastSavedTAPFile
        self.close()

    def handleSaveFile(self):
        self.ctrlFile.writeFile()
        #self.ctrlFile.generateCodeFile

        a = float(self.lblYApos[0].text().replace("+", ""))
        b = float(self.lblYBpos[0].text().replace("+", ""))
        exitM2 = a > 0.00
        exitM1 = b > 0.00
        array = self.buildArray(exitM2 and exitM1);
        if self.retFilename == '':
            self.retFilename = None
        self.ctrlFile.generateCodeFileEditor(self.retFilename, array, exitM1, exitM2)

        self.retFilename = self.ctrlFile.lastSavedTAPFile
        dialog = dlgMessage(self.lang.tr("TAP file generated."))
        dialog.open()
        dialog.exec_()

    def handleSaveAsFile(self):
        #dialog = dlgInputText(pos=(290, 50), widg=wdg, frmt="{:+6.2f}")
        dialog = dlgInputText(pos=(290, 50))
        dialog.show()
        dialog.exec_()
        value = dialog.value()
        if (value is not ""):
            value = value + ".tap"
            self.ctrlFile.writeFile()
            #self.ctrlFile.generateCodeFile(value)

            a = float(self.lblYApos[0].text().replace("+", ""))
            b = float(self.lblYBpos[0].text().replace("+", ""))
            exitM2 = a > 0.00
            exitM1 = b > 0.00
            array = self.buildArray(exitM2 and exitM1);
            self.ctrlFile.generateCodeFileEditor(value, array, exitM1, exitM2)

            self.retFilename = self.ctrlFile.lastSavedTAPFile
            dialog = dlgMessage(self.lang.tr("TAP file generated."))
            dialog.open()
            dialog.exec_()

        #self.ctrlFile.writeFile()
        #self.ctrlFile.generateCodeFile()

    def handlePaging(self, offset):
        if ((self.axisPageOffset + offset) >= 0 and (self.axisPageOffset + offset) * self.axisCount < self.ctrlFile.YROW_COUNT):
            self.axisPageOffset += offset

        for i in range(0, self.axisCount):
            j = i + 1
            self.lblYA[i].setText("Y" + str(self.axisPageOffset * self.axisCount + j))
            self.lblYApos[i].formatText(self.ctrlFile.getReferenceValue(self.axisPageOffset * self.axisCount + j, 1))
            self.lblYADepth[i].formatText(self.ctrlFile.getReferenceDepthValue(self.axisPageOffset * self.axisCount + j, 1))
            if not self.ctrlFile.disablePlug:
                self.btnYAPlug[i].blockSignals(True)
                self.btnYAPlug[i].setChecked(self.ctrlFile.getReferencePlugValue(self.axisPageOffset * self.axisCount + j, 1))
                self.btnYAPlug[i].blockSignals(False)

        for i in range(0, self.axisCount):
            j = i + 1
            self.lblYB[i].setText("Y" + str(self.axisPageOffset * self.axisCount + j))
            self.lblYBpos[i].formatText(self.ctrlFile.getReferenceValue(self.axisPageOffset * self.axisCount + j, 2))
            self.lblYBDepth[i].formatText(self.ctrlFile.getReferenceDepthValue(self.axisPageOffset * self.axisCount + j, 2))
            if not self.ctrlFile.disablePlug:
                self.btnYBPlug[i].blockSignals(True)
                self.btnYBPlug[i].setChecked(self.ctrlFile.getReferencePlugValue(self.axisPageOffset * self.axisCount + j, 2))
                self.btnYBPlug[i].blockSignals(False)

        self.axisPaging = False

    def assignConnectHandleInputY(self, btn, row, col):
        if (col == 1):
            if (row == 1):
                btn.clicked.connect(lambda: self.handleInputY(1, 1))
            elif (row == 2):
                btn.clicked.connect(lambda: self.handleInputY(2, 1))
            elif (row == 3):
                btn.clicked.connect(lambda: self.handleInputY(3, 1))
            elif (row == 4):
                btn.clicked.connect(lambda: self.handleInputY(4, 1))
            elif (row == 5):
                btn.clicked.connect(lambda: self.handleInputY(5, 1))
            elif (row == 6):
                btn.clicked.connect(lambda: self.handleInputY(6, 1))
            else:
                userInfo = QMessageBox.question(self, "VERTIMAQ-CNC", self.lang.tr("Contact programmer"), QMessageBox.Ok)
                print ("Error: assignConnectHandleInputY[" + str(row) +"]["+ str(col) + "]")
        elif (col == 2):
            if (row == 1):
                btn.clicked.connect(lambda: self.handleInputY(1, 2))
            elif (row == 2):
                btn.clicked.connect(lambda: self.handleInputY(2, 2))
            elif (row == 3):
                btn.clicked.connect(lambda: self.handleInputY(3, 2))
            elif (row == 4):
                btn.clicked.connect(lambda: self.handleInputY(4, 2))
            elif (row == 5):
                btn.clicked.connect(lambda: self.handleInputY(5, 2))
            elif (row == 6):
                btn.clicked.connect(lambda: self.handleInputY(6, 2))
            else:
                userInfo = QMessageBox.question(self, "VERTIMAQ-CNC", self.lang.tr("Contact programmer"), QMessageBox.Ok)
                print ("Error: assignConnectHandleInputY[" + str(row) +"]["+ str(col) + "]")
        else:
            userInfo = QMessageBox.question(self, "VERTIMAQ-CNC", self.lang.tr("Contact programmer"), QMessageBox.Ok)
            print ("Error: assignConnectHandleInputY[" + str(row) +"]["+ str(col) + "]")

    def assignMousePressEvent(self, lbl, row, col):
        if (col == 1):
            if (row == 1):
                lbl.mousePressEvent = lambda event: self.handleInputY(1, 1)
            elif (row == 2):
                lbl.mousePressEvent = lambda event: self.handleInputY(2, 1)
            elif (row == 3):
                lbl.mousePressEvent = lambda event: self.handleInputY(3, 1)
            elif (row == 4):
                lbl.mousePressEvent = lambda event: self.handleInputY(4, 1)
            elif (row == 5):
                lbl.mousePressEvent = lambda event: self.handleInputY(5, 1)
            elif (row == 6):
                lbl.mousePressEvent = lambda event: self.handleInputY(6, 1)
            else:
                userInfo = QMessageBox.question(self, "VERTIMAQ-CNC", self.lang.tr("Contact programmer"), QMessageBox.Ok)
                print ("Error: assignConnectHandleInputYPlug[" + str(row) +"]["+ str(col) + "]")
        elif (col == 2):
            if (row == 1):
                lbl.mousePressEvent = lambda event: self.handleInputY(1, 2)
            elif (row == 2):
                lbl.mousePressEvent = lambda event: self.handleInputY(2, 2)
            elif (row == 3):
                lbl.mousePressEvent = lambda event: self.handleInputY(3, 2)
            elif (row == 4):
                lbl.mousePressEvent = lambda event: self.handleInputY(4, 2)
            elif (row == 5):
                lbl.mousePressEvent = lambda event: self.handleInputY(5, 2)
            elif (row == 6):
                lbl.mousePressEvent = lambda event: self.handleInputY(6, 2)
            else:
                userInfo = QMessageBox.question(self, "VERTIMAQ-CNC", self.lang.tr("Contact programmer"), QMessageBox.Ok)
                print ("Error: assignConnectHandleInputYPlug[" + str(row) +"]["+ str(col) + "]")
        else:
            userInfo = QMessageBox.question(self, "VERTIMAQ-CNC", self.lang.tr("Contact programmer"), QMessageBox.Ok)
            print ("Error: assignConnectHandleInputYPlug[" + str(row) +"]["+ str(col) + "]")

    def assignMousePressEventDepth(self, lbl, row, col):
        if (col == 1):
            if (row == 1):
                lbl.mousePressEvent = lambda event: self.handleInputYDepth(1, 1)
            elif (row == 2):
                lbl.mousePressEvent = lambda event: self.handleInputYDepth(2, 1)
            elif (row == 3):
                lbl.mousePressEvent = lambda event: self.handleInputYDepth(3, 1)
            elif (row == 4):
                lbl.mousePressEvent = lambda event: self.handleInputYDepth(4, 1)
            elif (row == 5):
                lbl.mousePressEvent = lambda event: self.handleInputYDepth(5, 1)
            elif (row == 6):
                lbl.mousePressEvent = lambda event: self.handleInputYDepth(6, 1)
            else:
                userInfo = QMessageBox.question(self, "VERTIMAQ-CNC", self.lang.tr("Contact programmer"), QMessageBox.Ok)
                print ("Error: assignConnectHandleInputYPlug[" + str(row) +"]["+ str(col) + "]")
        elif (col == 2):
            if (row == 1):
                lbl.mousePressEvent = lambda event: self.handleInputYDepth(1, 2)
            elif (row == 2):
                lbl.mousePressEvent = lambda event: self.handleInputYDepth(2, 2)
            elif (row == 3):
                lbl.mousePressEvent = lambda event: self.handleInputYDepth(3, 2)
            elif (row == 4):
                lbl.mousePressEvent = lambda event: self.handleInputYDepth(4, 2)
            elif (row == 5):
                lbl.mousePressEvent = lambda event: self.handleInputYDepth(5, 2)
            elif (row == 6):
                lbl.mousePressEvent = lambda event: self.handleInputYDepth(6, 2)
            else:
                userInfo = QMessageBox.question(self, "VERTIMAQ-CNC", self.lang.tr("Contact programmer"), QMessageBox.Ok)
                print ("Error: assignConnectHandleInputYPlug[" + str(row) +"]["+ str(col) + "]")
        else:
            userInfo = QMessageBox.question(self, "VERTIMAQ-CNC", self.lang.tr("Contact programmer"), QMessageBox.Ok)
            print ("Error: assignConnectHandleInputYPlug[" + str(row) +"]["+ str(col) + "]")

    def assignConnectHandleTrashY(self, btn, row, col):
        if (col == 1):
            if (row == 1):
                btn.clicked.connect(lambda: self.handleTrashY(1, 1))
            elif (row == 2):
                btn.clicked.connect(lambda: self.handleTrashY(2, 1))
            elif (row == 3):
                btn.clicked.connect(lambda: self.handleTrashY(3, 1))
            elif (row == 4):
                btn.clicked.connect(lambda: self.handleTrashY(4, 1))
            elif (row == 5):
                btn.clicked.connect(lambda: self.handleTrashY(5, 1))
            elif (row == 6):
                btn.clicked.connect(lambda: self.handleTrashY(6, 1))
            else:
                userInfo = QMessageBox.question(self, "VERTIMAQ-CNC", self.lang.tr("Contact programmer"), QMessageBox.Ok)
                print ("Error: assignConnectHandleTrashY[" + str(row) +"]["+ str(col) + "]")
        elif (col == 2):
            if (row == 1):
                btn.clicked.connect(lambda: self.handleTrashY(1, 2))
            elif (row == 2):
                btn.clicked.connect(lambda: self.handleTrashY(2, 2))
            elif (row == 3):
                btn.clicked.connect(lambda: self.handleTrashY(3, 2))
            elif (row == 4):
                btn.clicked.connect(lambda: self.handleTrashY(4, 2))
            elif (row == 5):
                btn.clicked.connect(lambda: self.handleTrashY(5, 2))
            elif (row == 6):
                btn.clicked.connect(lambda: self.handleTrashY(6, 2))
            else:
                userInfo = QMessageBox.question(self, "VERTIMAQ-CNC", self.lang.tr("Contact programmer"), QMessageBox.Ok)
                print ("Error: assignConnectHandleTrashY[" + str(row) +"]["+ str(col) + "]")
        else:
            userInfo = QMessageBox.question(self, "VERTIMAQ-CNC", self.lang.tr("Contact programmer"), QMessageBox.Ok)
            print ("Error: assignConnectHandleTrashY [" + str(row) +"]["+ str(col) + "]")

    def assignConnectHandleInputYPlug(self, chkBox, row, col):
        if (col == 1):
            if (row == 1):
                chkBox.stateChanged.connect(lambda: self.handleInputYPlug(1, 1))
            elif (row == 2):
                chkBox.stateChanged.connect(lambda: self.handleInputYPlug(2, 1))
            elif (row == 3):
                chkBox.stateChanged.connect(lambda: self.handleInputYPlug(3, 1))
            elif (row == 4):
                chkBox.stateChanged.connect(lambda: self.handleInputYPlug(4, 1))
            elif (row == 5):
                chkBox.stateChanged.connect(lambda: self.handleInputYPlug(5, 1))
            elif (row == 6):
                chkBox.stateChanged.connect(lambda: self.handleInputYPlug(6, 1))
            else:
                userInfo = QMessageBox.question(self, "VERTIMAQ-CNC", self.lang.tr("Contact programmer"), QMessageBox.Ok)
                print ("Error: assignConnectHandleInputYPlug[" + str(row) +"]["+ str(col) + "]")
        elif (col == 2):
            if (row == 1):
                chkBox.stateChanged.connect(lambda: self.handleInputYPlug(1, 2))
            elif (row == 2):
                chkBox.stateChanged.connect(lambda: self.handleInputYPlug(2, 2))
            elif (row == 3):
                chkBox.stateChanged.connect(lambda: self.handleInputYPlug(3, 2))
            elif (row == 4):
                chkBox.stateChanged.connect(lambda: self.handleInputYPlug(4, 2))
            elif (row == 5):
                chkBox.stateChanged.connect(lambda: self.handleInputYPlug(5, 2))
            elif (row == 6):
                chkBox.stateChanged.connect(lambda: self.handleInputYPlug(6, 2))
            else:
                userInfo = QMessageBox.question(self, "VERTIMAQ-CNC", self.lang.tr("Contact programmer"), QMessageBox.Ok)
                print ("Error: assignConnectHandleInputYPlug[" + str(row) +"]["+ str(col) + "]")
        else:
            userInfo = QMessageBox.question(self, "VERTIMAQ-CNC", self.lang.tr("Contact programmer"), QMessageBox.Ok)
            print ("Error: assignConnectHandleInputYPlug[" + str(row) +"]["+ str(col) + "]")

    def refreshAxisData(self, row):

        if (row == 1):
            lblYPos = self.lblYApos
            btnYPlug = self.btnYAPlug
        else:
            lblYPos = self.lblYBpos
            btnYPlug = self.btnYBPlug

        for i in range(0, self.axisCount):
            j = i + 1
            lblYPos[i].formatText(self.ctrlFile.getReferenceValue(self.axisPageOffset * self.axisCount + j, row))
            if not self.ctrlFile.disablePlug:
                btnYPlug[i].blockSignals(True)
                btnYPlug[i].setChecked(self.ctrlFile.getReferencePlugValue(self.axisPageOffset * self.axisCount + j, row))
                btnYPlug[i].blockSignals(False)

    def alternateCol(self, col):
        altCol = {
            1: 2,
            2: 1,
        }

        return altCol.get(col, -1)


def createVBox(items, spacing=None, margins=None):
    vbox = QVBoxLayout()
    if (spacing is not None):
        vbox.setSpacing(spacing)
    if (margins is not None):
        vbox.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
    for w in items:
        vbox.addWidget(w)

    return vbox


def createHBox(items, spacing=None, margins=None, alignment=None ):
    hbox = QHBoxLayout()
    if (spacing is not None):
        hbox.setSpacing(spacing)
    if (margins is not None):
        hbox.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
    if alignment is not None:
        hbox.setAlignment(alignment)

    for w in items:
        hbox.addWidget(w)

    return hbox
